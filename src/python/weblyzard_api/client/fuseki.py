#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
This module provides a class that provides some convenience methods
to access a fuseki triplestore.
'''

import datetime
import hashlib
import io
import json
import os
import socket
import time

from SPARQLWrapper import SPARQLWrapper, JSON


class FusekiWrapper(object):
    '''
    provides methods to easily interface fuseki or other triple stores.
    '''

    NAMESPACES = {
        'http://weblyzard.com/skb/lexicon/': '',
        'http://weblyzard.com/skb/property/': 'skbprop',
        'http://lemon-model.net/lemon#': 'lemon',
        'http://www.w3.org/2000/01/rdf-schema#': 'rdfs',
        'http://www.w3.org/1999/02/22-rdf-syntax-ns#': 'rdf',
        'http://www.w3.org/2004/02/skos/core#': 'skos',
        'http://purl.org/dc/elements/1.1/': 'dc',
        'http://www.lexinfo.net/ontology/2.0/lexinfo#': 'lexinfo',
        'http://purl.org/dc/terms/': 'dct',
        'http://www.w3.org/2001/XMLSchema#': 'xsd',
        'http://www.w3.org/ns/prov#': 'prov',
        'http://id.loc.gov/vocabulary/iso639-1/': 'lang',
    }
    PREFIXES = '\n'.join(['PREFIX {value}: <{key}>'.format(value=value,
                                                           key=key) \
                          for key, value in NAMESPACES.iteritems()])

    def __init__(self, sparql_endpoint, debug=False):
        self.debug_ = debug
        if 'query' in sparql_endpoint:
            self.query_endpoint = sparql_endpoint
            self.update_endpoint = sparql_endpoint.replace('query', 'update')
        elif 'update' in sparql_endpoint:
            self.update_endpoint = sparql_endpoint
            self.query_endpoint = sparql_endpoint.replace('update', 'query')
        else:
            sparql_endpoint = sparql_endpoint[:-1] if sparql_endpoint.endswith('/') \
                                                   else sparql_endpoint
            self.update_endpoint = '/'.join([sparql_endpoint, 'update'])
            self.query_endpoint = '/'.join([sparql_endpoint, 'query'])
        self.update_wrapper = SPARQLWrapper(self.update_endpoint)
        self.update_wrapper.method = 'POST'
        self.update_wrapper.setReturnFormat(JSON)
        self.update_wrapper.setTimeout(600000000)

        self.query_wrapper = SPARQLWrapper(self.query_endpoint)
        self.query_wrapper.setReturnFormat(JSON)
        self.query_wrapper.setTimeout(600000000)

        self.uri_cache = set()

    def debug(self, string_):
        if self.debug_:
            print(string_)

    def fix_uri(self, o):
        '''
        If a uri is only the full ury, i.e. not prefixed, it needs
        to be enclosed in angled brackets.
        '''
        if isinstance(o, tuple) and len(o) == 3:
            return((self.fix_uri(o[0]), self.fix_uri(o[1]), self.fix_uri(o[2])))
        elif isinstance(o, str) or isinstance(o, unicode):
            if o.startswith('http'):
                return u'<{}>'.format(o)
            else:
                return o

    def is_uri(self, value):
        '''
        Check if the value is a URI or not.
        '''
        if isinstance(value, int):
            return False
        elif isinstance(value, str) or isinstance(value, unicode):
            for prefix in self.NAMESPACES.values():
                if value.startswith(prefix):
                    return True
            if value.startswith('<http') and value[-1:] == '>':
                return True
            return False

    def execute_query(self, query, caching=False, on_fly_json_decoding=False):
        def parse_and_yield(result):
            '''
            This is a hacky JSON parser that allows to parse the JSON
            response without parsing it all at once, but result line by
            result line.
            '''
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
                filename = 'query_cache/{}.json'.format(hashlib.md5(query).hexdigest())
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
            print('socket error, waiting and retrying')
            time.sleep(5)
            for row in self.execute_query(query=query):
                yield row

    def run_query(self, query, no_prefix=False, batch_size=None,
                  order_by_stmt=None, caching=False):
        '''
        Run the given query and return the result's bindings.

        :param query: The SPARQL query to run.
        '''
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

    def run_update(self, query, no_prefix=False):
        '''
        Run the given update query on the update endpoint.

        :param query: The query (insert, update) to run.
        '''
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
            print('socket error, waiting and retrying')
            time.sleep(5)
            self.run_update(query=query, no_prefix=True)

    def exists(self, uri):
        '''
        Check if a given URI is already in the store.
        '''
        if uri in self.uri_cache:
            return True
        query = u'''
        SELECT ?p WHERE {{
          {{ <{x}> ?p ?o. }} UNION {{?s ?p <{x}> }} .
        }}
        LIMIT 1
        '''.format(x=uri)
        result = list(self.run_query(query=query))
        if len(result) > 0:
            self.uri_cache.add(uri)
            return True
        else:
            return False

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

    def get_new_URI(self, base_uri):
        '''
        Get a new URI that does not yet exist in the RDF graph. It appends
        numerical, increasing suffixes to the base_uri until it finds a free
        URI.
        '''
        candidate_uri = base_uri
        if candidate_uri not in self.uri_cache and not self.exists(candidate_uri):
            return candidate_uri
        else:
            suffix = 1
            candidate_uri = u'{}_{}'.format(base_uri, suffix)
            while not(candidate_uri not in self.uri_cache and not self.exists(candidate_uri)):
                if candidate_uri not in self.uri_cache:
                    self.uri_cache.add(candidate_uri)
                suffix += 1
                candidate_uri = u'{}_{}'.format(base_uri, suffix)
            return candidate_uri

    def insert_triples(self, triple_list):
        slice_size = 250
        lower = 0
        num_triples = len(triple_list)
        upper = min(slice_size, num_triples)
        while upper > lower:
            sub_list = triple_list[lower:upper]
            # make sure that no blank node triples get sliced into different
            # sublists
            for t in triple_list[upper:]:
                if t[0][:2] == '_:':
                    sub_list.append(t)
                    upper += 1
                else:
                    break
            sub_list = [self.fix_uri(t) for t in sub_list]
            triples = '.\n'.join([' '.join(triple) for triple in sub_list])
            query = u"""
            INSERT DATA {{
              {triples}
            }}
            """.format(triples=triples)
            lower = upper
            upper = min(num_triples, upper + slice_size)
            self.run_update(query=query)
        [self.uri_cache.add(t[0]) for t in triple_list]
        [self.uri_cache.add(t[2]) for t in triple_list if self.is_uri(t[2])]

    def insert_triple(self, s, p, o):
        triple = ' '.join([self.fix_uri(s), self.fix_uri(p), self.fix_uri(o)])
        query = u"""
        INSERT DATA {{
          {triple}
        }}
        """.format(triple=triple)
        self.run_update(query=query)
        self.uri_cache.add(s)
        if self.is_uri(o):
            self.uri_cache.add(o)
