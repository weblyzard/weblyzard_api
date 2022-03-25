#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Part-of-speech (POS) tagging service

.. codeauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''
from __future__ import print_function
from __future__ import unicode_literals
import unittest

from weblyzard_api.client import RESTClient
from weblyzard_api.client import (
    WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS)


class POS(RESTClient):

    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER,
                 pwd=WEBLYZARD_API_PASS):
        '''
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        '''
        RESTClient.__init__(self, url, usr, pwd)

    def pos_tagging(self, text, lang):
        """ tags the following text using the given language dictionary 

        :returns: the corresponding ANNIE compatible annotations
        """
        return self.execute("pos-tagging", None, {'text': text, 'lang': lang})


class POSTest(unittest.TestCase):

    def test_POS(self):
        p = POS()
        print(p.pos_tagging('Guten Tag Herr Mayer!', 'de'))


if __name__ == '__main__':
    unittest.main()
