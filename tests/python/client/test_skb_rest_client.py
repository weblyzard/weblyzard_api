#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from weblyzard_api.client.skb_rest_client import SKBRESTClient

class TestSKBRESTClient(unittest.TestCase):
    
    pass
    #mcg: commented out until mock provided for skb
#     def test_translations_request(self):
#         base_url = 'http://localhost:5002'
#         client = SKBRESTClient(base_url)        
#         expected_translations = {'knall': 'pop', 'falle': 'trap', 'fall': 'case'}
#         for source in expected_translations:
#             result = client.translate(client='google',
#                                       term=source,
#                                       source='de',
#                                       target='en')
#             assert(result[0] == expected_translations[source])
#             assert(result[1] == 'en')


if __name__ == '__main__':
    unittest.main()