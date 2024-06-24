import logging
from pprint import pprint

from weblyzard_api.client.triplestore import TriplestoreWrapper2

logger = logging.getLogger(__name__)


class QleverWrapper(TriplestoreWrapper2):
    """
    Built upon the SPARQLWrapper for accessing Qlever.
    """

    def __init__(self, sparql_endpoint, debug=False):
        super().__init__(sparql_endpoint=sparql_endpoint,
                         debug=debug)

    @staticmethod
    def from_config(host, port, dataset: str):
        return QleverWrapper(sparql_endpoint=f'{host}:{port}/{dataset}',
                             debug=False)


def test_qlever_queries():
    qlever_wrapper = QleverWrapper(sparql_endpoint='https://qlever.cs.uni-freiburg.de/api/wikidata')
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

    bindings = qlever_wrapper.run_query(query)
    for result in qlever_wrapper.group_bindings(bindings):
        pprint(result)

    assert(qlever_wrapper.exists(uri='http://www.wikidata.org/entity/Q76'))
