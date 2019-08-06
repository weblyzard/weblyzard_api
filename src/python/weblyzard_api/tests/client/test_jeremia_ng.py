#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 22, 2018

.. codeauthor:: Max Göbel <goebel@weblyzard.com>
'''
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
import os
import unittest

from weblyzard_api.client.jeremia_ng import JeremiaNg


class JeremiaTest(unittest.TestCase):

    DOCS = [{'id': content_id,
             'body': 'Donald Trump and Barack Obama are presidents in the United States. Vienna is the capital of Austria, Berlin is the capital of Germany. Linz also is in Austria" {}'.format(
                 content_id),
             'title': 'Hello "world" more ',
             'format': 'text/html',
             'header': {}} for content_id in xrange(1000, 1020)]
    def setUp(self):
        service_url = os.getenv('JEREMIA_NG_SERVICE_URL', 'localhost:63001')
        self.client = JeremiaNg(url=service_url)


    def test_single_document_processing(self):
        """Test submitting a single document."""
        print('submitting document...')
        result = self.client.submit_document(self.DOCS[0])

        from pprint import pprint
        pprint(result)
        self.assertTrue(result != "")

    def test_dutch_string(self):
        dutch_string = 'Bioscoopjournaals waarin Nederlandse onderwerpen van een bepaalde week worden gepresenteerd. Transport per vrachtauto van een 25 meter lange en 2,5 meter hoge ketel van de grens bij Nijmegen naar een kalkzandsteenfabriek bij Vuren bij Gorkum.'
        doc = {'id': 1000,
               'body': dutch_string,
               'title': 'Hallo wereld',
               'format': 'text/html',
               'header': {}}
        print('submitting document...')
        result = self.client.submit_document(doc)
        tockens = set([tocken['pos'] for tocken in result['partitions']['TOKEN']])
        assert 'VNW|pers|pron|obl|red|3|ev|masc' not in tockens
        from pprint import pprint
        pprint(result)
        assert result['lang'] == 'NL'


if __name__ == '__main__':
    unittest.main()
