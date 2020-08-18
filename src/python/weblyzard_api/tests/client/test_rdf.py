# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest

from weblyzard_api.client.rdf import (
    prefix_uri, replace_prefix, parse_language_tagged_string,
    NORMALIZED_NAMESPACE)


@pytest.mark.parametrize(
    "uri,prefixed",
    [
        ('http://weblyzard.com/skb/entity/agent/derstandard/sperl',
         'http://weblyzard.com/skb/entity/agent/derstandard/sperl'),
        ('http://weblyzard.com/skb/entity/agent/derstandard',
         'agent:derstandard'),
        ('http://weblyzard.com/skb/entity/xyz',
         'skbentity:xyz'),
        ('http://example.com/something',
         'http://example.com/something'),
        ('http://www.wikidata.org/prop/statement/my_statement',
         'ps:my_statement'),
        ('http://dbpedia.org/ontology/building/house',
         'dbo:building/house'),
        ('http://dbpedia.org/ontology/building/house',
         'dbo:building/house'),
        ('http://sws.geonames.org/130758/',
         'geonames:130758/')
    ])
def test_replace_prefix(uri, prefixed):
    result = replace_prefix(uri=prefixed)
    assert result == uri


@pytest.mark.parametrize('value,expected',
                         [('test@en', ('test', 'en')),
                          ('test@eng', ('test', 'eng')),
                          ('test@en-us', ('test', 'en-us')),
                          ('fabian.fischer@modul.ac.at',
                           ('fabian.fischer@modul.ac.at', None)),
                          ('@xy', ('@xy', None))
                          ])
def test_parse_single_string(value, expected):
    assert parse_language_tagged_string(value) == expected


@pytest.mark.parametrize(
    "uri,prefixed",
    [
        # agent:derstandard/sperl is not a valid URI
        ('http://weblyzard.com/skb/entity/agent/derstandard/sperl',
         'http://weblyzard.com/skb/entity/agent/derstandard/sperl'),
        # agent:derstandard should be used instead of skbentity: prefix
        ('http://weblyzard.com/skb/entity/agent/derstandard',
         'agent:derstandard'),
        ('http://weblyzard.com/skb/entity/xyz',
         'skbentity:xyz'),
        # no prefix configured for this namespace, return unchanged
        ('http://example.com/something',
         'http://example.com/something'),
        # do not replace partial prefix dbo:building/house
        ('http://dbpedia.org/ontology/building/house',
         'http://dbpedia.org/ontology/building/house'),
        # replace if / at the end
        ('http://sws.geonames.org/130758/',
         'geonames:130758/')
    ])
def test_prefix_uri(uri, prefixed):
    result = prefix_uri(uri=uri)
    assert result == prefixed


@pytest.mark.parametrize(
    "uri,partially_prefixed",
    [
        # # replace partial prefix
        ('http://weblyzard.com/skb/entity/agent/derstandard/sperl',
         'agent:derstandard/sperl'),
        # agent:derstandard should be used instead of skbentity: prefix
        ('http://weblyzard.com/skb/entity/agent/derstandard',
         'agent:derstandard'),
        # replace partial prefix
        ('http://weblyzard.com/skb/entity/xyz/abc',
         'skbentity:xyz/abc'),
        # no prefix configured for this namespace, return unchanged
        ('http://example.com/something',
         'http://example.com/something'),
        # replace partial prefix
        ('http://dbpedia.org/ontology/building/house',
         'dbo:building/house'),
        # replace if / at the end
        ('http://sws.geonames.org/130758/',
         'geonames:130758/')
    ])
def test_partial_prefix_uri(uri, partially_prefixed):
    result = prefix_uri(uri=uri, allow_partial=True)
    assert result == partially_prefixed


def test_normalized_namespace():
    # hardcoded mapping from uris encountered on the web to namespace
    assert NORMALIZED_NAMESPACE['https://www.wikidata.org/wiki/Q42'] == 'http://www.wikidata.org/entity/Q42'
    # default replacement of https->http
    assert NORMALIZED_NAMESPACE['https://en.wikipedia.org/wiki/Longyearbyen'] == 'http://en.wikipedia.org/wiki/Longyearbyen'
    # no replacement: non-matching strings and non-strings
    assert NORMALIZED_NAMESPACE['abchttps'] == 'abchttps'
    assert NORMALIZED_NAMESPACE[1] == 1
    assert prefix_uri('https://www.wikidata.org/wiki/Q42') == 'wd:Q42'
