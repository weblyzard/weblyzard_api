#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import unittest

import mock
import pytest
from weblyzard_api.client.skb_rest_client import SKBRESTClient


class MockResponse:

    def __init__(self, json_data, text, status_code):
        self.json_data = json_data
        self.text = text
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestSKBRESTClientTranslations(unittest.TestCase):

    def setUp(self):
        url = 'http://skb-rest-translation.prod.i.weblyzard.net:8443'  # prod
        # url = 'http://localhost:5000'
        self.skb_client = SKBRESTClient(url)

    def test_translations_request(self):
        expected_translations = {'knall': 'bang', 'falle': 'trap', 'fall': 'case'}
        for source in expected_translations:
            result = self.skb_client.translate(term=source,
                                               source='de',
                                               target='en')
            assert(result[0] == expected_translations[source])
            assert(result[1] == 'en')

    @mock.patch('weblyzard_api.client.skb_rest_client.requests.get')
    def test_title_translations_request(self, mock_get):
        source = "Die schmerzhaften, aber sehr selten tödlichen Folgen eines" \
        "Witwenbisses gehen auf die besondere Struktur der Latrotoxine zurück"
        expected_translation = "The painful but very rarely fatal consequences" \
        "of a widow's bite are due to the special structure of the latrotoxins"

        mock_get.return_value = MockResponse(text=expected_translation,
                                             json_data=None,
                                             status_code=200)

        result = self.skb_client.title_translate(client='google',
                                                 text=source,
                                                 source='de',
                                                 target='en')
        assert(result[0] == expected_translation)
        assert(result[1] == 'en')


class TestSKBRESTClientEntities(unittest.TestCase):

    def setUp(self):
        self.skb_client = SKBRESTClient(url=os.getenv(
            'WL_SKB_UNITTEST_URL', 'http://localhost:5000'))

    def test_clean_keyword_data(self):
        kw_annotation = {
            "topEntityId": "energy",
            "confidence": 786.2216230656553,
            "entities": [{
                "surfaceForm": "energy",
                "start": 112,
                "end": 118,
                "sentence": 0
            }],
            "grounded": True,
            "scoreName": "CONFIDENCE x OCCURENCE",
            "entityType": "GemetEntity",
            "score": 786.22,
            "key": "http://www.eionet.europa.eu/gemet/concept/2712",
            "provenance": "en.gemet",
            "properties": {
                "definition": "The capacity to do work; involving thermal energy (heat), radiant energy (light), kinetic energy (motion) or chemical energy; measured in joules."
            },
            "preferredName": "energy"
        }
        cleaned = self.skb_client.clean_keyword_data(kw_annotation)
        assert cleaned == {
            "entityType": "GemetEntity",
            "uri": "http://www.eionet.europa.eu/gemet/concept/2712",
            "provenance": "en.gemet",
            "preferredName": "energy"
        }

        kw_annotation = {
            "confidence": 0.0,
            "grounded": True,
            "entityType": "NonEntityKeyword",
            "score": 0.0,
            "key": "http://weblyzard.com/skb/keyword/en/noun/equator",
            "provenance": "save_skb_entities",
            "preferredName": "equator"
        }
        cleaned = self.skb_client.clean_keyword_data(kw_annotation)
        assert cleaned == {
            "entityType": "NonEntityKeyword",
            "uri": "http://weblyzard.com/skb/keyword/en/noun/equator",
            "provenance": "save_skb_entities",
            "preferredName": "equator@en",
            "lexinfo:partOfSpeech": "noun"
        }

        # missing pos
        kw_annotation = {
            "entityType": "NonEntityKeyword",
            "key": "http://weblyzard.com/skb/keyword/fr/privé",
            "provenance": "save_skb_entities",
            "preferredName": "privé"
        }
        cleaned = self.skb_client.clean_keyword_data(kw_annotation)
        assert cleaned == {
            "entityType": "NonEntityKeyword",
            "uri": "http://weblyzard.com/skb/keyword/fr/privé",
            "provenance": "save_skb_entities",
            "preferredName": "privé@fr",
        }

        # missing lang
        kw_annotation = {
            "entityType": "NonEntityKeyword",
            "key": "http://weblyzard.com/skb/keyword/solo",
            "provenance": "save_skb_entities",
            "preferredName": "solo"
        }
        cleaned = self.skb_client.clean_keyword_data(kw_annotation)
        assert cleaned == {
            "entityType": "NonEntityKeyword",
            "uri": "http://weblyzard.com/skb/keyword/solo",
            "provenance": "save_skb_entities",
            "preferredName": "solo",
        }

    def test_save_keyword(self):
        kw_annotation = {
            "topEntityId": "energy",
            "confidence": 786.2216230656553,
            "entities": [{
                "surfaceForm": "energy",
                "start": 112,
                "end": 118,
                "sentence": 0
            }],
            "grounded": True,
            "scoreName": "CONFIDENCE x OCCURENCE",
            "entityType": "GemetEntity",
            "score": 786.22,
            "key": "http://www.eionet.europa.eu/gemet/concept/2712",
            "profileName": "en.gemet",
            "properties": {
                "definition": "The capacity to do work; involving thermal energy (heat), radiant energy (light), kinetic energy (motion) or chemical energy; measured in joules."
            },
            "preferredName": "energy"
        }
        kw_annotation['provenance'] = 'kw_test_workflow_20191022'
        assert(self.skb_client.save_doc_kw_skb(kw_annotation) ==
               'http://www.eionet.europa.eu/gemet/concept/2712')

    def test_save_entity(self):
        entity_data = {
            u"publisher": u"You Don't Say",
            u"title": u"Hello, world!",
            u"url": u"http://www.youdontsayaac.com/hello-world-2/",
            u"charset": u"UTF-8",
            u"thumbnail": u"https://s0.wp.com/i/blank.jpg",
            u"locale": u"en_US",
            u"last_modified": u"2014-07-15T18:46:42+00:00",
            u"page_type": u"article",
            u"published_date": u"2014-07-15T18:46:42+00:00",
            # @ at the beginning of values not allowed as it is reserved for language tags
            # u"twitter_site": u"@mfm_Kay",
            u"twitter_card": u"summary"
        }
        try:
            response = self.skb_client.save_entity(entity_dict=entity_data)
            assert False  # entityType must be set -> assertion error must be raised
        except AssertionError:
            assert True
        entity_data['entityType'] = 'AgentEntity'
        try:
            response = self.skb_client.save_entity_batch(
                entity_list=entity_data)
            assert False  # provenance must be set -> assertion error must be raised
        except AssertionError:
            assert True
        entity_data['provenance'] = 'agent_test_workflow_20191022'
        response = self.skb_client.save_entity(entity_dict=entity_data)
        assert response == 'http://weblyzard.com/skb/entity/agent/you_don_t_say'
        # Getting entity
        result = self.skb_client.get_entity(
            uri="http://weblyzard.com/skb/entity/agent/you_don_t_say")
        entity_type = entity_data.pop(u'entityType')
        provenance = entity_data.pop(u'provenance')  # provenance not returned
        assert entity_type in result[u'entityType']
        for k, v in entity_data.items():
            assert k in list(result['properties'].keys())
            assert v in result['properties'][k]['values']
        result = self.skb_client.get_entity(
            uri="agent:you_don_t_say")
        assert entity_type in result[u'entityType']
        for k, v in entity_data.items():
            assert k in list(result['properties'].keys())
            assert v in result['properties'][k]['values']
        result = self.skb_client.get_entity_by_property(
            property_name='url',
            property_value='http://www.youdontsayaac.com/hello-world-2/',
            entity_type='AgentEntity')
        assert isinstance(result, list)
        assert len(result) == 1
        assert entity_type in result[0][u'entityType']
        for k, v in entity_data.items():
            assert k in list(result[0]['properties'].keys())
            assert v in result[0]['properties'][k]['values']
        result = self.skb_client.get_entity_by_property(
            property_value='http://www.youdontsayaac.com/hello-world-2/')
        assert isinstance(result, list)
        assert len(result) == 1
        for k, v in entity_data.items():
            assert k in list(result[0]['properties'].keys())
            assert v in result[0]['properties'][k]['values']

    def test_save_entity_batch(self):
        entity_data = [{
            u"publisher": u"You Don't Say",
            u"title": u"Hello, world!",
            u"url": u"http://www.youdontsayaac.com/hello-world-2/",
            u"charset": u"UTF-8",
            u"thumbnail": u"https://s0.wp.com/i/blank.jpg",
            u"locale": u"en_US",
            u"last_modified": u"2014-07-15T18:46:42+00:00",
            u"page_type": u"article",
            u"published_date": u"2014-07-15T18:46:42+00:00",
            # @ at the beginning of values not allowed as it is reserved for language tags
            # u"twitter_site": u"twitter@mfm_Kay",
            u"twitter_card": u"summary"
        }]
        try:
            response = self.skb_client.save_entity_batch(
                entity_list=entity_data)
            assert False  # entityType must be set -> assertion error must be raised
        except AssertionError:
            assert True
        entity_data[0]['entityType'] = 'AgentEntity'
        try:
            response = self.skb_client.save_entity_batch(
                entity_list=entity_data)
            assert False  # provenance must be set -> assertion error must be raised
        except AssertionError:
            assert True
        entity_data[0]['provenance'] = 'agent_test_workflow_20191022'
        response = self.skb_client.save_entity_batch(entity_list=entity_data)
        assert(response['data'][0]['message'] in ['success', 'skipped'])
        assert response['data'][0]['uri'] == 'http://weblyzard.com/skb/entity/agent/you_don_t_say'
        # Getting entity
        result = self.skb_client.get_entity(
            uri="http://weblyzard.com/skb/entity/agent/you_don_t_say")
        entity_type = entity_data[0].pop(u'entityType')
        provenance = entity_data[0].pop(
            u'provenance')  # provenance not returned
        assert entity_type in result[u'entityType']
        for k, v in entity_data[0].items():
            assert k in list(result['properties'].keys())
            assert v in result['properties'][k]['values']
        result = self.skb_client.get_entity(
            uri="agent:you_don_t_say")
        for k, v in entity_data[0].items():
            assert k in list(result['properties'].keys())
            assert v in result['properties'][k]['values']
        result = self.skb_client.get_entity_by_property(
            property_name='url',
            property_value='http://www.youdontsayaac.com/hello-world-2/',
            entity_type='AgentEntity')
        assert isinstance(result, list)
        assert len(result) == 1
        for k, v in entity_data[0].items():
            assert k in list(result[0]['properties'].keys())
            assert v in result[0]['properties'][k]['values']
        result = self.skb_client.get_entity_by_property(
            property_value='http://www.youdontsayaac.com/hello-world-2/')
        assert isinstance(result, list)
        assert len(result) == 1
        for k, v in entity_data[0].items():
            assert k in list(result[0]['properties'].keys())
            assert v in result[0]['properties'][k]['values']


if __name__ == '__main__':
    unittest.main()
