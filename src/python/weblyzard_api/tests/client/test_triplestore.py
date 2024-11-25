import unittest
from os import getenv
from pprint import pprint

from weblyzard_api.client.triplestore import TriplestoreWrapper2
from weblyzard_api.client.triplestore.blazegraph import BlazegraphWrapper
from weblyzard_api.client.triplestore.fuseki import FusekiWrapper
from weblyzard_api.client.triplestore.qlever import QleverWrapper

FUSEKI_ENDPOINT = 'http://fuseki-lod.prod.i.weblyzard.net:8443/wikidata.20190603'
class TriplestoreTestFuseki(unittest.TestCase):
    #FUSEKI_ENDPOINT = getenv('FUSEKI_ENDPOINT')
    if not FUSEKI_ENDPOINT:
        raise ValueError("No Fuseki query service endpoint set!")
    fuseki_wrapper = FusekiWrapper(sparql_endpoint=FUSEKI_ENDPOINT, debug=True)

    def test_fuseki_query(self):
        query = '''
        PREFIX wd: <http://www.wikidata.org/entity/> 
        SELECT ?uri ?label ?country ?headquarters_location WHERE {
                  ?uri rdfs:label ?label;
                    wdt:P279 wd:Q43229;
                    wdt:P17 ?country.
                  OPTIONAL { ?uri wdt:P159 ?headquarters_location. }
                }
        LIMIT 1000
        '''

        for row in self.fuseki_wrapper.run_query(query):
            pprint(row)

    def test_fuseki_exists(self):
        assert (self.fuseki_wrapper.exists(uri='http://www.wikidata.org/entity/Q76'))

    def test_ask(self):
        assert (self.fuseki_wrapper.ask(query='ASK WHERE {{ wd:Q128660 wdt:P17 wd:Q40 }}'))


class TriplestoreTestBlazegraph(unittest.TestCase):
    # official wikidata endpoint
    blazegraph_wrapper = BlazegraphWrapper(f'https://query.wikidata.org/sparql')
    #blazegraph_wrapper = BlazegraphWrapper(f'http://78.142.140.80:9999/bigdata/namespace/wdq')


    def test_query(self):
        query = '''
                    PREFIX wd: <http://www.wikidata.org/entity/> 
                    SELECT ?uri ?label ?country ?headquarters_location WHERE {
                              ?uri rdfs:label ?label;
                                wdt:P279 wd:Q43229;
                                wdt:P17 ?country.
                              OPTIONAL { ?uri wdt:P159 ?headquarters_location. }
                              FILTER(((LANG(?label)) = "en") || ((LANG(?label)) = "de"))
                            }
                    LIMIT 1000
                    '''
        bindings = self.blazegraph_wrapper.run_query(query)
        for result in self.blazegraph_wrapper.group_bindings(bindings):
            pprint(result)
            assert (all(k in result.keys() for k in ['uri', 'label', 'country']))
            assert (all(value.split('@')[1] in ['de', 'en'] for value in result['label']))

    def test_value_from_grouped_bindings(self):
        query = '''
                PREFIX wd: <http://www.wikidata.org/entity/> 
                SELECT ?uri ?label ?country ?headquarters_location WHERE {
                        VALUES ?uri {wd:Q18214700}
                          ?uri rdfs:label ?label;
                            wdt:P279 wd:Q43229;
                            wdt:P17 ?country.
                          OPTIONAL { ?uri wdt:P159 ?headquarters_location. }
                          FILTER(((LANG(?label)) = "en") || ((LANG(?label)) = "de"))
                        }
                LIMIT 100
                '''
        bindings = self.blazegraph_wrapper.run_query(query)
        for result in self.blazegraph_wrapper.group_bindings(bindings):
            assert (self.blazegraph_wrapper.get_value_from_grouped_bindings(result, field='label', language='de')
                    in "Öffentliche Einrichtung" )
            assert (self.blazegraph_wrapper.get_value_from_grouped_bindings(result, field='label')
                    is None)  # no non-specified language value
            assert (self.blazegraph_wrapper.get_value_from_grouped_bindings(result, field='country', language='de')
                    == "http://www.wikidata.org/entity/Q31")  # defaults to non-specified language
            assert (self.blazegraph_wrapper.get_value_from_grouped_bindings(result, field='country')
                    == "http://www.wikidata.org/entity/Q31")


    def test_exists(self):
        assert (self.blazegraph_wrapper.exists(uri='http://www.wikidata.org/entity/Q76'))

    def test_ask(self):
        assert (self.blazegraph_wrapper.ask(query='ASK WHERE {{ wd:Q128660 wdt:P17 wd:Q40 }}'))


class TriplestoreTestQlever(unittest.TestCase):
    # official qlever endpoint
    qlever_wrapper = QleverWrapper(sparql_endpoint='https://qlever.cs.uni-freiburg.de/api/wikidata')

    def test_query(self):
        query = '''
                PREFIX wd: <http://www.wikidata.org/entity/> 
                SELECT ?uri ?label ?country ?headquarters_location WHERE {
                          ?uri rdfs:label ?label;
                            wdt:P279 wd:Q43229;
                            wdt:P17 ?country.
                          OPTIONAL { ?uri wdt:P159 ?headquarters_location. }
                          FILTER((LANG(?label)) = "en")
                        }
                LIMIT 1000
                '''

        bindings = self.qlever_wrapper.run_query(query)
        for result in self.qlever_wrapper.group_bindings(bindings):
            pprint(result)
            assert (all(k in result.keys() for k in ['uri', 'label', 'country']))
            assert (all(value.split('@')[1] == "en" for value in result['label']))

    def test_exists(self):
        assert (self.qlever_wrapper.exists(uri='http://www.wikidata.org/entity/Q76'))

def test_ts_wrapper_get_deduplicated_prefixes():
    query = '''
        PREFIX wd: <http://www.wikidata.org/entity/>
        SELECT ?class WHERE {
            VALUES ?class { geonames:2779469 wd:Q76 wd:Q5}
            ?class rdfs:label ?label.
            ?class gn:parentFeature* ?class .
            .
    	}
        '''

    ts_wrapper = TriplestoreWrapper2(sparql_endpoint='dummy')

    assert('PREFIX wd: <http://www.wikidata.org/entity/>' not in ts_wrapper.remove_duplicate_prefixes(query))
    assert(ts_wrapper.remove_duplicate_prefixes(query,
                                                prefixes='PREFIX wd: <http://www.wikidata.org/entity/>\n'
                                                         'PREFIX geonames: <http://sws.geonames.org/>')
           == 'PREFIX geonames: <http://sws.geonames.org/>')

def test_ts_wrapper_get_only_used_prefixes():
    query = '''
    SELECT ?class WHERE {
        VALUES ?class { geonames:2779469 wd:Q76 wd:Q5}
        ?class rdfs:label ?label.
        ?class gn:parentFeature* ?class .
        .
	}
    '''
    ts_wrapper = TriplestoreWrapper2(sparql_endpoint='dummy')
    assert(ts_wrapper.retrieve_only_used_prefixes(query)
           == 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
              'PREFIX wd: <http://www.wikidata.org/entity/>\n'
              'PREFIX geonames: <http://sws.geonames.org/>\n'
              'PREFIX gn: <http://www.geonames.org/ontology#>'
              )