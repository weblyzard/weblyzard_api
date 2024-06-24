import unittest
from os import getenv
from pprint import pprint

from weblyzard_api.client.triplestore.blazegraph import BlazegraphWrapper
from weblyzard_api.client.triplestore.fuseki import FusekiWrapper
from weblyzard_api.client.triplestore.qlever import QleverWrapper


class TriplestoreTestFuseki(unittest.TestCase):
    FUSEKI_ENDPOINT = getenv('FUSEKI_ENDPOINT')
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
