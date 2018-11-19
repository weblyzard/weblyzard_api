#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Nov 15, 2018

'''
import unittest

from pprint import pprint

from weblyzard_api.client import MEDMON_API_URL

from weblyzard_api.client.ontogene import Oger
from weblyzard_api.client.recognize import Recognize
from weblyzard_api.client.jeremia import Jeremia


class TestOGER(unittest.TestCase):
    def setUp(self):
        url =  MEDMON_API_URL
        print(url)
        
        self.client = Oger(url)
        
        self.service_is_online = self.client.is_online()
        if not self.service_is_online:
            print('WARNING: Webservice is offline --> not executing all tests!!')
            self.IS_ONLINE = False
            return

        version = self.client.get_version()
        print(version)
        
    def test_status(self):
        self.assertTrue(self.client.status())
        

if __name__ == '__main__':
    unittest.main()