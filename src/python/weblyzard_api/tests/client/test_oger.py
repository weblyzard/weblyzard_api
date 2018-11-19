#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Nov 15, 2018

'''
import unittest

from pprint import pprint

from weblyzard_api.client import OGER_API_URL

from weblyzard_api.client.ontogene import Oger
from weblyzard_api.client.recognize import Recognize
from weblyzard_api.client.jeremia import Jeremia


class TestOGER(unittest.TestCase):
    def setUp(self):
        url =  OGER_API_URL
        print(url)
        
        self.client = Oger(url)
        
        self.service_is_online = self.client.is_online()
        if not self.service_is_online:
            print('WARNING: Webservice is offline --> not executing all tests!!')
            self.IS_ONLINE = False
            return

    def test_version(self):
        version = self.client.get_version()
        print(version)
        self.assertTrue(version)
    
    
    def test_status(self):
        self.assertTrue(self.client.status())
        
    #'''
    def test_fetch_path(self):
        response = self.client.fetch_document(docid='21436587')
        self.assertTrue(response)
    #'''
    
    def test_upload(self):
        docid='99999999'
        doctext='Cancer, also called malignancy, is an abnormal growth of cells. '
        response = self.client.upload_document(docid, doctext)
        self.assertTrue(response)
        #'''
    
if __name__ == '__main__':
    unittest.main()