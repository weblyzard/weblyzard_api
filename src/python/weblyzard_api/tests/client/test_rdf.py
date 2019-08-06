# -*- coding: utf-8 -*-

import pytest

from weblyzard_api.client.rdf import (
    prefix_uri, replace_prefix, parse_language_tagged_string)


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
    ])
def test_replace_prefix(uri, prefixed):
    namespaces = {
        'http://weblyzard.com/skb/entity/': 'skbentity',
        'http://weblyzard.com/skb/entity/agent/': 'agent',
    }
    result = replace_prefix(uri=prefixed, namespaces=namespaces)
    assert result == uri


@pytest.mark.parametrize('value,expected',
                         [('test@en', ('test', 'en')),
                          ('test@eng', ('test', 'eng')),
                          ('test@en-us', ('test', 'en-us')),
                          ('fabian.fischer@modul.ac.at', ('fabian.fischer@modul.ac.at', None)),
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
    ])
def test_prefix_uri(uri, prefixed):
    namespaces = {
        'http://weblyzard.com/skb/entity/': 'skbentity',
        'http://weblyzard.com/skb/entity/agent/': 'agent',
    }
    result = prefix_uri(uri=uri, namespaces=namespaces)
    assert result == prefixed
