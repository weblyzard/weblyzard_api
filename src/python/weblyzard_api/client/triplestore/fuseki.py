#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
This module provides a class that provides some convenience methods
to access a fuseki triplestore.
'''
from __future__ import print_function
from __future__ import unicode_literals

from builtins import object
import hashlib
import io
import json
import os
import socket
import logging
from pprint import pprint
from typing import List, Tuple

from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib.term

from weblyzard_api.client.rdf import PREFIXES, NAMESPACES
from weblyzard_api.client.triplestore import _retry_with_backoff, TriplestoreWrapper1, TIMEOUT, USER_AGENT

logger = logging.getLogger(__name__)


class FusekiWrapper(TriplestoreWrapper1):
    """
    Provides methods to easily interface fuseki or other triple stores.
    """

    def __init__(self, sparql_endpoint, debug=False):
        super().__init__(sparql_endpoint=sparql_endpoint,
                         debug=debug)

        # set query/update endpoint accordingly
        if 'query' in sparql_endpoint:
            self.query_endpoint = sparql_endpoint
            self.update_endpoint = sparql_endpoint.replace('query', 'update')
        elif 'update' in sparql_endpoint:
            self.update_endpoint = sparql_endpoint
            self.query_endpoint = sparql_endpoint.replace('update', 'query')
        else:
            sparql_endpoint = sparql_endpoint[:-1] if sparql_endpoint.endswith('/') else sparql_endpoint
            self.update_endpoint = '/'.join([sparql_endpoint, 'update'])
            self.query_endpoint = '/'.join([sparql_endpoint, 'query'])

    def variable_to_python(self, variable_dict, add_language_tag=False):
        """
        Convert a given variable_dict to the closest python representation.
        :param variable_dict: The dict representing the variable.
        :type variable_dict: `dict`
        :param add_language_tag: If a language-tagged string literal should \
                be language-tagged (and wrapped in double quotes).
        :type add_language_tag: `bool`
        :rtype: `object`
        """
        if variable_dict['type'] == 'uri':
            return variable_dict['value']
        elif variable_dict['type'] == 'literal':
            if variable_dict.get('xml:lang', False):
                if add_language_tag:
                    return u'"{}"@{}'.format(
                        variable_dict['value'],
                        variable_dict['xml:lang']
                    )
                else:
                    return variable_dict['value']
            elif variable_dict.get('datatype', False):
                datatype = variable_dict['datatype']
                uri_ref = rdflib.term.URIRef(datatype)
                mapping_function = rdflib.term._toPythonMapping.get(
                    uri_ref, None)
                if mapping_function is None:
                    return variable_dict['value']
                else:
                    return mapping_function(variable_dict['value'])
            else:
                try:
                    return int(variable_dict['value'])
                except ValueError:
                    pass
                try:
                    return float(variable_dict['value'])
                except ValueError:
                    return variable_dict['value']
        else:
            return variable_dict['value']

    @_retry_with_backoff
    def execute_query(self, query, caching=False, on_fly_json_decoding=False):

        def parse_and_yield(result):
            """
            This is a hacky JSON parser that allows to parse the JSON
            response without parsing it all at once, but result line by
            result line.
            """
            row = ''
            in_bindings = False
            for line in result:
                if in_bindings:
                    if line.startswith('      }'):
                        yield json.loads(''.join([row, '}']))
                        row = ''
                    else:
                        row = '\n'.join([row, line])
                if '"bindings"' in line:
                    in_bindings = True

        try:
            self.query_wrapper.setQuery(query)
            self.debug(u'running the following query against {endpoint}\n{query}'.format(
                query=query,
                endpoint=self.query_endpoint))
            if caching:
                filename = 'query_cache/{}.json'.format(
                    hashlib.md5(query).hexdigest())
                if not os.path.isfile(filename):
                    result = self.query_wrapper.query()
                    with open(filename, 'ab') as f:
                        f.writelines(result)
                    print('written result to cache file')
                else:
                    print('file dump found, not querying triplestore')
                with io.open(filename, 'rb') as f:
                    for r in parse_and_yield(f):
                        yield r
            else:
                if on_fly_json_decoding:
                    for r in parse_and_yield(self.query_wrapper.query()):
                        yield r
                else:
                    res = self.query_wrapper.query().convert()
                    for r in res['results']['bindings']:
                        yield r
        except socket.error as e:
            logger.warning(
                f'socket error {self.query_endpoint}: {e}', exc_info=True)
            raise e

    def run_query(self, query, no_prefix=False, batch_size=None,
                  order_by_stmt=None, caching=False):
        """
        Run a given query and return the result's bindings.
        :param no_prefix: if True does not inject all PREFIX values
        :param batch_size: controls LIMIT and OFFSET in batch queries
        :param order_by_stmt: accepts and ORDER BY query part for batch updates
        :param caching: caches to a file (?)
        :param query: the SPARQL query to run.
        """
        if not no_prefix:
            query = u'{}{}'.format(self.PREFIXES, query)
        if batch_size:
            assert order_by_stmt is not None
            query = u'{}\n{}'.format(query, order_by_stmt)
        if batch_size:
            last_batch = -1
            offset = 0
            while last_batch < offset:
                last_batch = offset
                batch_query = '{}\nLIMIT {}\nOFFSET {}'.format(
                    query,
                    batch_size,
                    offset)
                for row in self.execute_query(batch_query,
                                              caching=caching):
                    offset += 1
                    yield row
        else:
            for row in self.execute_query(query, caching=caching):
                yield row

    @_retry_with_backoff
    def run_update(self, query, no_prefix=False):
        """
        Run a given update query against the update endpoint.
        :param no_prefix: if True does not inject all PREFIX values
        :param query: The query (insert, update) to run.
        """
        if not no_prefix:
            query = u'{}{}'.format(self.PREFIXES, query)
        self.debug(u'running the following update query against {endpoint}\n{query}'.format(
            query=query,
            endpoint=self.update_endpoint))
        if self.debug_:
            print("Not running update query due to debug being set")
            return
        try:
            self.update_wrapper.setQuery(query)
            self.update_wrapper.query()
        except socket.error as e:
            logger.warning(
                f'socket error {self.query_endpoint}: {e}', exc_info=True)
            raise e

    def get_new_uri(self, base_uri):
        """
        Get a new URI that does not yet exist in the RDF graph. It appends
        numerical, increasing suffixes to the base_uri until it finds a free
        URI.
        """
        candidate_uri = base_uri
        if candidate_uri not in self.uri_cache and not self.exists(candidate_uri):
            return candidate_uri
        else:
            suffix = 1
            candidate_uri = u'{}_{}'.format(base_uri, suffix)
            while not (candidate_uri not in self.uri_cache and not self.exists(candidate_uri)):
                if candidate_uri not in self.uri_cache:
                    self.uri_cache.add(candidate_uri)
                suffix += 1
                candidate_uri = u'{}_{}'.format(base_uri, suffix)
            return candidate_uri

    def insert_triples(self, triple_list: List[Tuple], graph_name: str = None) -> None:
        """
        Add triples to the Fuseki dataset.
        :param triple_list: List of triple tuples (s, p, o)
        :param graph_name: if provided, adds to that named GRAPH
        """
        slice_size = 250
        lower = 0
        num_triples = len(triple_list)
        upper = min(slice_size, num_triples)
        while upper > lower:
            sub_list = triple_list[lower:upper]
            # make sure that no blank node triples get sliced into different sublists
            for t in triple_list[upper:]:
                if t[0][:2] == '_:':
                    sub_list.append(t)
                    upper += 1
                else:
                    break
            sub_list = [self.fix_uri(t) for t in sub_list]
            triples = '.\n'.join([' '.join(triple) for triple in sub_list])
            if graph_name:
                query_body = f"""
                graph <{graph_name}>
                    {{
                      {triples}
                    }}
            """
            else:
                query_body = triples

            query = u"""
            INSERT DATA {{
              {query_body}
            }}
            """.format(query_body=query_body)
            lower = upper
            upper = min(num_triples, upper + slice_size)
            self.run_update(query=query)
        [self.uri_cache.add(t[0]) for t in triple_list]
        [self.uri_cache.add(t[2]) for t in triple_list if self.is_uri(t[2])]

    def insert_triple(self, s, p, o, graph_name=None) -> None:
        """
        Adds a single triple, consisting of s, p, o to the Fuseki dataset.
        :param s: subject
        :param p: predicate
        :param o: object
        :param graph_name: if provided, adds to that named GRAPH
        """
        triple = ' '.join([self.fix_uri(s), self.fix_uri(p), self.fix_uri(o)])
        if graph_name:
            query_body = f"""
            graph <{graph_name}> 
                {{ 
                  {triple}
                }}
        """
        else:
            query_body = triple
        query = u"""
        INSERT DATA {{
        {query_body}
        }}
        """.format(query_body=query_body)

        self.run_update(query=query)
        self.uri_cache.add(s)
        if self.is_uri(o):
            self.uri_cache.add(o)
