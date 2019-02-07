#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Nov 15, 2018

'''
import unittest

from pprint import pprint

from weblyzard_api.client import OGER_API_URL

from weblyzard_api.client.ontogene import OgerClient
from weblyzard_api.client.recognize import Recognize
from weblyzard_api.client.jeremia import Jeremia


class TestOGER(unittest.TestCase):
    def setUp(self):
        url =  OGER_API_URL    
        print(url)    
        self.client = OgerClient(url)
    
    def test_raise_exception_if_service_urls_is_array(self):
        with self.assertRaises(Exception) as context:
            OgerClient(['http://localhost:8080', 'http://localhost:8081'])
        self.assertTrue('Oger url cannot be an array' in context.exception)
    
    def test_status(self):
        self.assertTrue(self.client.status())
        
    def test_annotate_text(self):
        docid='99999999'
        #doctext='Cancer, also called malignancy, is an abnormal growth of cells.'
        doctext='Alzheimer\'s disease (AD), also referred to simply as Alzheimer\'s, is a chronic neurodegenerative disease that usually starts slowly and worsens over time.'
        response = self.client.annotate_text(docid, doctext)
        assert len(response), 'No items found for {}'.format(docid)
    
if __name__ == '__main__':
    unittest.main()