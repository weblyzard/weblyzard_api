from __future__ import print_function
from __future__ import unicode_literals

import logging
from pprint import pprint

from weblyzard_api.client.triplestore import TriplestoreWrapper2

logger = logging.getLogger(__name__)


class BlazegraphWrapper(TriplestoreWrapper2):
    """
    Built upon the SPARQLWrapper for accessing blazegraph.
    """
    def __init__(self, sparql_endpoint, debug=False):
        super().__init__(sparql_endpoint=sparql_endpoint,
                         debug=debug)

    @staticmethod
    def from_config(host, port):
        path = 'bigdata/namespace/wdq/sparql'
        return BlazegraphWrapper(sparql_endpoint=f'{host}:{port}/{path}',
                                 debug=False)

    # @staticmethod
    # def get_wikidata_sparql_endpoint() -> str:
    #     """
    #     Get the current blazegraph SPARQL endpoint.
    #     TODO: move to a environment variable or parameter
    #     """
    #     host = 'http://78.142.140.80'
    #     port = 9999
    #     path = 'bigdata/namespace/wdq/sparql'
    #     sparql_endpoint = '{}:{}/{}'.format(host, port, path)
    #     return sparql_endpoint


def test_blazegraph_queries():
    blazegraph_wrapper = BlazegraphWrapper.from_config()
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

    bindings = blazegraph_wrapper.run_query(query)
    for result in blazegraph_wrapper.group_bindings(bindings):
        pprint(result)

    assert(blazegraph_wrapper.exists(uri='http://www.wikidata.org/entity/Q76'))
    assert(blazegraph_wrapper.ask(query='ASK WHERE {{ wd:Q128660 wdt:P17 wd:Q40 }}'))
