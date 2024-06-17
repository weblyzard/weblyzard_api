import socket
from _collections import defaultdict
import logging
from pprint import pprint
from typing import Generator

from SPARQLWrapper import SPARQLWrapper2, JSON
from weblyzard_api.client.rdf import PREFIXES

logger = logging.getLogger(__name__)


class BlazegraphWrapper(object):
    """
    Built upon the SPARQLWrapper for accessing blazegraph.
    """

    PREFIXES = PREFIXES

    def __init__(self, sparql_endpoint, debug=False):
        self.debug_ = debug
        self.query_endpoint = sparql_endpoint

        # use SPARQLWrapper2
        self.query_wrapper = SPARQLWrapper2(self.query_endpoint)
        self.query_wrapper.method = 'GET'
        self.query_wrapper.setReturnFormat(JSON)
        self.query_wrapper.setTimeout(600000000)

        self.uri_cache = set()

    def debug(self, string_):
        if self.debug_:
            print(string_)

    @staticmethod
    def from_config():
        return BlazegraphWrapper(sparql_endpoint=BlazegraphWrapper.get_wikidata_sparql_endpoint(),
                                 debug=False)

    @staticmethod
    def get_wikidata_sparql_endpoint() -> str:
        """
        Get the current blazegraph SPARQL endpoint.
        TODO: move to a environment variable or parameter
        """
        host = 'http://78.142.140.80'
        port = 9999
        path = 'bigdata/namespace/wdq/sparql'
        sparql_endpoint = '{}:{}/{}'.format(host, port, path)
        return sparql_endpoint

    def _set_query_method(self, query: str):
        """
        Switch to POST if the query is too long.
        """
        if len(query) > 500:  # not sure if this is the correct cutoff
            self.query_wrapper.method = 'POST'

    def remove_duplicate_prefixes(self, query: str) -> str:
        """ 
        Remove duplicate prefix declarations from the query that cause
        a `QueryBadFormed` Error for Blazegraph.
        """
        prefixes = "\n".join([prefix for prefix in self.PREFIXES.split("\n")
                              if prefix not in query])
        return prefixes

    def run_query(self, query, no_prefix=False):
        """ 
        Run a given query and return the result's bindings.
        :param query: The SPARQL query to run.
        :param no_prefix: if True does not inject all PREFIX values
        """
        self._set_query_method(query)
        if not no_prefix:
            prefixes = self.remove_duplicate_prefixes(query)
            query = f'{prefixes}{query}'
        self.query_wrapper.setQuery(query)
        self.debug(f'running the following query against {self.query_endpoint}\n{query}')

        res = self.query_wrapper.query()
        for binding in res.bindings:
            yield binding

    @staticmethod
    def group_bindings(bindings, key: str = 'uri') -> Generator:
        """
        Group a query result's bindings, using `key` as a grouping indicator.
        Result bindings need to be ordered by `key` var for grouping.
        :param bindings: a query result's bindings
        :param key: the query var by which the results are grouped
        """
        uri = None
        result = defaultdict(set)
        for row in bindings:
            if uri and row[key].value != uri:
                # return as single value or set of values
                yield result
                result = defaultdict(set)

            uri = row[key].value
            for row_key, row_value in row.items():
                if row_value.lang:
                    value = f'{row_value.value}@{row_value.lang}'
                else:
                    value = f'{row_value.value}'
                result[row_key].add(value)
        yield result

    @staticmethod
    def group_all_bindings(bindings) -> dict:
        """
        Group all bindings of the query result.
        To use with queries that return different values for one entity, e.g.
        entity (jairo) enrichment queries.
        :param bindings: query result bindings
        """
        result = defaultdict(list)
        for row in bindings:
            for row_key, row_value in row.items():
                if row_value.lang:
                    value = f'{row_value.value}@{row_value.lang}'
                else:
                    value = f'{row_value.value}'
                if value not in result[row_key]:
                    result[row_key].append(value)
        return result

    def ask(self, query: str, no_prefix: bool = False) -> bool:
        """
        Run a given ask query against the query endpoint.
        :param query: the ask query to run
        :param no_prefix: do not preface with rdf PREFIXES
        """
        if not no_prefix:
            query = f'{self.PREFIXES}{query}'
        self.debug(f'running the following ask query against {self.query_endpoint}\n{query}')
        try:
            self.query_wrapper.setQuery(query)
            res = self.query_wrapper.query().convert()
            return res["boolean"]
        except socket.error as e:
            logger.warning(
                f'socket error {self.query_endpoint}: {e}', exc_info=True)
            raise e

    def exists(self, uri) -> bool:
        """ Check if a given URI is already in the store.
        :param uri:
        """
        if uri in self.uri_cache:
            return True
        query = f'''
                SELECT ?p WHERE {{
                  {{ <{uri}> ?p ?o. }} UNION {{?s ?p <{uri}> }} .
                }}
                LIMIT 1
        '''
        result = list(self.run_query(query=query))
        if len(result) > 0:
            self.uri_cache.add(uri)
            return True
        else:
            return False


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

    print(blazegraph_wrapper.exists(uri='http://www.wikidata.org/entity/Q76'))
    print(blazegraph_wrapper.ask(query='ASK WHERE {{ wd:Q128660 wdt:P17 wd:Q40 }}'))
