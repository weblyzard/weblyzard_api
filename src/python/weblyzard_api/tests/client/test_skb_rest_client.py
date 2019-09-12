#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import pytest
import unittest


from weblyzard_api.client.skb_rest_client import SKBRESTClient
#
#
# class TestSKBRESTClient(unittest.TestCase):
#
#     def test_translations_request(self):
#         batch = MatviewDocumentsBatch(matview_name='weblyzard_test',
#                                       limit=10,
#                                       with_keywords=False)
#
#         batch.prepare()
#         config = batch.config
#         base_url = config.get('service_url', 'translate_title')
#         client = SKBRESTClient(base_url)
#         expected_translations = {'knall': 'pop', 'falle': 'trap', 'fall': 'case'}
#         for source in expected_translations:
#             result = client.translate(client='google',
#                                       term=source,
#                                       source='de',
#                                       target='en')
#             assert(result[0] == expected_translations[source])
#             assert(result[1] == 'en')
#
#     def test_title_translations_request(self):
#         batch = MatviewDocumentsBatch(matview_name='weblyzard_test',
#                                       limit=10,
#                                       with_keywords=False)
#
#         batch.prepare()
#         config = batch.config
#         base_url = config.get('service_url', 'translate_title')
#         client = SKBRESTClient(base_url)
#         expected_translations = {'knall': 'pop', 'falle': 'trap', 'fall': 'case'}
#         for source in expected_translations:
#             result = client.title_translate(client='google',
#                                       term=source,
#                                       source='de',
#                                       target='en')
#             assert(result[0] == expected_translations[source])
#             assert(result[1] == 'en')
#


class TestSKBEntities(unittest.TestCase):
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
            u"twitter_site": u"@mfm_Kay",
            u"twitter_card": u"summary"
        }
        try:
            response = self.skb_client.save_entity(entity_dict=entity_data)
            assert False  # entityType must be set -> assertion error must be raised
        except AssertionError:
            assert True
        entity_data['entityType'] = 'AgentEntity'
        response = self.skb_client.save_entity(entity_dict=entity_data)
        assert response == 'http://weblyzard.com/skb/entity/agent/you_don_t_say'
        # Getting entity
        result = self.skb_client.get_entity(
            uri="http://weblyzard.com/skb/entity/agent/you_don_t_say")
        entity_data[u'provenance'] = None
        assert result == entity_data
        result = self.skb_client.get_entity(
            uri="agent:you_don_t_say")
        assert result == entity_data
        result = self.skb_client.get_entity_by_property(
            property_name='url',
            property_value='http://www.youdontsayaac.com/hello-world-2/',
            entity_type='AgentEntity')
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] == entity_data
        result = self.skb_client.get_entity_by_property(
            property_value='http://www.youdontsayaac.com/hello-world-2/')
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] == entity_data

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
            u"twitter_site": u"@mfm_Kay",
            u"twitter_card": u"summary"
        }]
        try:
            response = self.skb_client.save_entity_batch(
                entity_list=entity_data)
            assert False  # entityType must be set -> assertion error must be raised
        except AssertionError:
            assert True
        entity_data[0]['entityType'] = 'AgentEntity'
        response = self.skb_client.save_entity_batch(entity_list=entity_data)
        assert response == [
            'http://weblyzard.com/skb/entity/agent/you_don_t_say', ]
        # Getting entity
        result = self.skb_client.get_entity(
            uri="http://weblyzard.com/skb/entity/agent/you_don_t_say")
        entity_data[0][u'provenance'] = None
        assert result == entity_data[0]
        result = self.skb_client.get_entity(
            uri="agent:you_don_t_say")
        assert result == entity_data[0]
        result = self.skb_client.get_entity_by_property(
            property_name='url',
            property_value='http://www.youdontsayaac.com/hello-world-2/',
            entity_type='AgentEntity')
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] == entity_data[0]
        result = self.skb_client.get_entity_by_property(
            property_value='http://www.youdontsayaac.com/hello-world-2/')
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] == entity_data[0]


if __name__ == '__main__':
    unittest.main()
