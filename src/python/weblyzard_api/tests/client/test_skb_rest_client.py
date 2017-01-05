# #! /usr/bin/env python
# # -*- coding: utf-8 -*-
# import unittest
# 
# from weblyzard_api.client.skb_rest_client import SKBRESTClient
# from wl_core_ng.models.documents_batch import MatviewDocumentsBatch
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
# if __name__ == '__main__':
#     unittest.main()