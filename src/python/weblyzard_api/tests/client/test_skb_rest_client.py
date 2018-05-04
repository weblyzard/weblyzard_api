#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
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


class TestSKBKeywords(unittest.TestCase):

    def test_save_keyword(self):
        skb_client = SKBRESTClient(url=os.getenv('WL_SKB_UNITTEST_URL'))
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
        assert(skb_client.save_doc_kw_skb(kw_annotation) == 'Done')


if __name__ == '__main__':
    unittest.main()
