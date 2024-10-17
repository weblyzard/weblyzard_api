import logging
import socket
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Generator

from SPARQLWrapper import SPARQLWrapper2, JSON, SPARQLWrapper

from weblyzard_api.client.rdf import PREFIXES, NAMESPACES

logger = logging.getLogger(__name__)


USER_AGENT = "Mozilla/5.0 (compatible; ecoresearchSparlClient/0.9; +http://www.ecoresearch.net)"
TIMEOUT = 600000000

def _retry_with_backoff(decorated):  # @NoSelf
    def decorator(*args, **kwargs):
        max_retries = 8  # 2^(max_retries+1) seconds until error
        num_retries = 0
        retry_delay = 1
        success = False
        while (not success) and num_retries < max_retries:
            try:
                return decorated(*args, **kwargs)
                success = True
            except Exception as e:
                logger.warning(
                    f'retrying {decorated.__name__} in {retry_delay} seconds...')
                time.sleep(retry_delay)
                num_retries = num_retries + 1
                retry_delay = retry_delay * 2
        # last try without catching the exception
        return decorated(*args, **kwargs)

    return decorator


class AbstractTriplestoreWrapper(ABC):

    PREFIXES = PREFIXES

    def __init__(self, sparql_endpoint, debug=False):
        self.debug_ = debug
        self.uri_cache = set()

        self.query_endpoint = sparql_endpoint
        self.update_endpoint = sparql_endpoint
        self.query_wrapper = None
        self.update_wrapper = None

    def debug(self, string_):
        if self.debug_:
            print(string_)

    def remove_duplicate_prefixes(self, query: str) -> str:
        """
        Remove duplicate prefix declarations from the query that can cause
        a `QueryBadFormed` Error.
        """
        prefixes = "\n".join([prefix for prefix in self.PREFIXES.split("\n")
                              if prefix not in query])
        return prefixes

    def fix_uri(self, o):
        """
        If a uri is only the full uri, i.e. not prefixed, it needs
        to be enclosed in angled brackets.
        If a value is not a str it needs to be converted.
        """

        if isinstance(o, tuple) and len(o) == 3:
            return self.fix_uri(o[0]), self.fix_uri(o[1]), self.fix_uri(o[2])
        elif isinstance(o, (str, bytes)):
            if isinstance(o, bytes):
                o = o.decode('utf-8')
            if o.startswith('http'):
                o = u'<{}>'.format(o)
            return o
        else:
            return str(o)

    def is_uri(self, value):
        """
        Check if the value is a URI or not.
        """
        if isinstance(value, int):
            return False
        elif isinstance(value, (str, bytes)):
            if isinstance(value, bytes):
                value = value.decode('utf-8')
            for prefix in list(NAMESPACES.values()):
                if value.startswith(prefix):
                    return True
            if value.startswith('<http') and value[-1:] == '>':
                return True
            return False

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

    @abstractmethod
    def run_query(self, query, no_prefix=False):
        pass

    @abstractmethod
    def run_update(self, query, no_prefix=False):
        pass


class TriplestoreWrapper1(AbstractTriplestoreWrapper):
    """
    Uses SPARQLWrapper.SPARQLWrapper
    Query results are returned as dictionaries with `type` and `value`.

    > {'uri': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q155004'},
       'occupation': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q82955'}}
    """

    def __init__(self, sparql_endpoint, debug=False):
        super().__init__(sparql_endpoint=sparql_endpoint,
                         debug=debug)

        # init for updates
        self.update_wrapper = SPARQLWrapper(self.update_endpoint)
        self.update_wrapper.method = 'POST'
        self.update_wrapper.setReturnFormat(JSON)
        self.update_wrapper.setTimeout(TIMEOUT)

        # init for query
        self.query_wrapper = SPARQLWrapper(self.query_endpoint, agent=USER_AGENT)
        self.query_wrapper.method = 'GET'
        self.query_wrapper.setReturnFormat(JSON)
        self.query_wrapper.setTimeout(TIMEOUT)

    def populate_uri_cache(self):
        query = u'''
        SELECT ?s ?o WHERE {{
          {{ ?s ?p ?o. }} .
        }}
        '''
        result = self.run_query(query=query)
        for row in result:
            if row['s']['type'] == 'uri':
                self.uri_cache.add(row['s']['value'])
            if row['o']['type'] == 'uri':
                self.uri_cache.add(row['o']['value'])


class TriplestoreWrapper2(AbstractTriplestoreWrapper):
    """
    Uses SPARQLWrapper.SPARQLWrapper2
    Query results are returned as SPARQLWrapper.Value items.

    > {'uri': Value(uri:'http://www.wikidata.org/entity/Q1875721'),
       'label': Value(literal:'Luftlandepioniere'),
       'country': Value(uri:'http://www.wikidata.org/entity/Q183')}

    """
    def __init__(self, sparql_endpoint, debug=False):
        super().__init__(sparql_endpoint=sparql_endpoint,
                         debug=debug)

        # only query implemented!
        self.query_wrapper = SPARQLWrapper2(self.query_endpoint)
        self.query_wrapper.method = 'GET'
        self.query_wrapper.setReturnFormat(JSON)
        self.query_wrapper.setTimeout(TIMEOUT)

    def _set_query_method(self, query: str):
        """
        Switch to POST if the query is too long.
        """
        if len(query) > 500:  # not sure if this is the correct cutoff
            self.query_wrapper.method = 'POST'

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

    def run_update(self, query, no_prefix=False):
        raise NotImplementedError

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

    @staticmethod
    def get_value_from_grouped_bindings(grouped_bindings: dict, field: str, language: str = None) -> Optional[str]:
        lang_agnostic_value = None
        for value in list(grouped_bindings.get(field, [])):
            try:
                value, lang = parse_language_tagged_string(value)
                if language is not None and lang == language:
                    return value
                if not lang:
                    lang_agnostic_value = value
            except ValueError:
                pass  # can not be parsed
        return lang_agnostic_value
