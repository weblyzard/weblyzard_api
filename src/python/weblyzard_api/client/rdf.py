#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


NAMESPACES = {
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#': 'rdf',
    'http://www.w3.org/2000/01/rdf-schema#': 'rdfs',
    'http://www.w3.org/2001/XMLSchema#': 'xsd',
    'http://www.w3.org/2002/07/owl#': 'owl',
    'http://www.w3.org/2004/02/skos/core#': 'skos',
    'http://www.w3.org/ns/prov#': 'prov',
    'http://purl.org/dc/elements/1.1/': 'dc',
    'http://purl.org/dc/terms/': 'dct',
    'http://schema.org/description': 'schema',
    # lexical namespaces
    'http://lemon-model.net/lemon#': 'lemon',
    'http://www.lexinfo.net/ontology/2.0/lexinfo#': 'lexinfo',
    'http://id.loc.gov/vocabulary/iso639-1/': 'lang',
    # wikidata, dbpedia, geo
    'http://dbpedia.org/ontology/': 'dbo',
    'http://www.opengis.net/ont/geosparql#': 'geo',
    'http://www.wikidata.org/prop/direct/': 'wdt',
    'http://www.wikidata.org/entity/': 'wd',
    'http://sws.geonames.org': 'gn',
    # weblyzard namespaces
    'http://weblyzard.com/skb/lexicon/': 'skblex',
    'http://weblyzard.com/skb/property/': 'skbprop',
    'http://weblyzard.com/skb/entity/': 'skbentity',
    'http://weblyzard.com/skb/entity/agent/': 'agent',
    # weblyzard keywords per language
    'http://weblyzard.com/skb/keyword/en#': 'skbkwen',
    'http://weblyzard.com/skb/keyword/de#': 'skbkwde',
    'http://weblyzard.com/skb/keyword/fr#': 'skbkwfr',
    'http://weblyzard.com/skb/keyword/es#': 'skbkwes',
    'http://weblyzard.com/skb/keyword/it#': 'skbkwit',
    'http://weblyzard.com/skb/keyword/pt#': 'skbkwpt',
    'http://weblyzard.com/skb/keyword/zh#': 'skbkwzh',
    'http://weblyzard.com/skb/keyword/ru#': 'skbkwru',
    'http://weblyzard.com/skb/keyword/ar#': 'skbkwar',
    'http://weblyzard.com/skb/keyword/nl#': 'skbkwnl',
}

PREFIXES = '\n'.join(['PREFIX {value}: <{key}>'.format(value=value,
                                                       key=key) \
                      for key, value in NAMESPACES.items()])


def prefix_uri(uri, namespaces=None):
    '''
    Replaces a sub-path from the uri with the most specific prefix as defined
    in the namespaces.

    :param uri: The URI to modify.
    :type uri: str
    :param namespaces: A mapping of namespace to prefix (without ':').
    :type namespaces: `dict`
    :returns: The modified URI if applicable
    :rtype: str
    '''
    if namespaces is None:
        namespaces = NAMESPACES
    if not uri.startswith('http'):
        return uri
    # replace most specific/longest prefix, hence sorted
    for namespace in sorted(list(namespaces.keys()), key=len, reverse=True):
        if namespace in uri:
            replaced = uri.replace(namespace, '{}:'.format(namespaces[namespace]))
            if '/' in replaced or '#' in replaced:
                # slashes or hashes in prefixed URIs not allowed
                continue
            else:
                return replaced
    return uri


def replace_prefix(uri, namespaces=None):
    '''
    Replaces a prefix with the full namespace path.

    :param uri: The URI to modify.
    :type uri: str
    :param namespaces: A mapping of namespace to prefix (without ':').
    :type namespaces: `dict`
    :returns: The modified URI if applicable
    :rtype: str
    '''
    if namespaces is None:
        namespaces = NAMESPACES
    for namespace, prefix in namespaces.items():
        if prefix in uri:
            return uri.replace('{}:'.format(prefix), namespace)
    return uri