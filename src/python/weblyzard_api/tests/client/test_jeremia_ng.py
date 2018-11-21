#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 22, 2018

.. codeauthor:: Max Göbel <goebel@weblyzard.com>
'''
import unittest

from weblyzard_api.client.jeremia_ng import JeremiaNg


class JeremiaTest(unittest.TestCase):

    DOCS = [{'id': content_id,
             'body': 'Donald Trump and Barack Obama are presidents in the United States. Vienna is the capital of Austria, Berlin is the capital of Germany. Linz also is in Austria" {}'.format(content_id),
             'title': 'Hello "world" more ',
             'format': 'text/html',
             'header': {}} for content_id in xrange(1000, 1020)]

    def setUp(self):
        service_url = 'localhost:63001'
        self.client = JeremiaNg(url=service_url)

    def test_single_document_processing(self):
        """Test submitting a single document."""
        print('submitting document...')
        result = self.client.submit_document(self.DOCS[0])

        from pprint import pprint
        pprint(result)
        self.assertTrue(result != "")


if __name__ == '__main__':
    unittest.main()
