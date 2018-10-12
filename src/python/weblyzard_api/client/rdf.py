#! /usr/bin/env python
# -*- coding: utf-8 -*-

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
    'http://sws.geonames.org': 'geonames',
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
