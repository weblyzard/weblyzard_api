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

    # DOCS = [{'id': content_id,
    #          'body': 'Donald Trump and Barack Obama are presidents in the United States. Vienna is the capital of Austria, Berlin is the capital of Germany. Linz also is in Austria" {}'.format(
    #              content_id),
    #          'title': 'Hello "world" more ',
    #          'format': 'text/html',
    #          'header': {}} for content_id in range(1000, 1020)]

    DOCS = [{'id': 12,
             'body': 'Donald Trump and Barack Obama are presidents in the United States.',
             'title': 'US news',
             'format': 'text/plain',
             'header': {}},
            {'id': 12,
             'body': 'The photo was taken in the grounds of Windsor Castle in March, according to the royal family Twitter account.',
             'title': 'UK news',
             'format': 'text/plain',
             'header': {}},
            {'id': 12,
             'body': 'Toymaker Mattel has also announced a Barbie doll in the monarch\'s likeness to celebrate the jubilee.',
             'title': 'UK news',
             'format': 'text/plain',
             'header': {}},
            {'id': 12,
             'body': 'Ahead of his grandmother turning 96, Harry commented that \"after a certain age you get bored of birthdays.\"',
             'title': 'UK news',
             'format': 'text/plain',
             'header': {}},
            {'id': 12,
             'body': 'Elon Musk says he has lined up $46.5 billion in financing to buy Twitter, and he\'s trying to negotiate an agreement with the company.',
             'title': 'Tech news',
             'format': 'text/plain',
             'header': {}},
            {'id': 12,
             'body': 'The Taiwanese government is investigating a local TV news station after it aired alarming false reports of a Chinese invasion against the self-ruled island.',
             'title': 'Taiwan news',
             'format': 'text/plain',
             'header': {}},

    ]

    def setUp(self):
        service_url = os.getenv('JEREMIA_NG_SERVICE_URL', 'http://jeremia.prod.i.weblyzard.net:8443')
        self.client = JeremiaNg(url=service_url)

    def test_single_document_processing(self):
        """Test submitting a single document."""
        print('submitting document...')

        for doc in self.DOCS:
            result = self.client.submit_document(doc)

            from pprint import pprint
            print(result)
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

    def test_token_annotations(self):
        text = "Der Mensch besitzt gücklicherweise ein Herz"
        doc = {'id': 1001,
               'body': text,
               'title': 'Dependency-Check',
               'format': 'text/html',
               'header': {}}
        print('submitting document...')
        result = self.client.submit_document(doc)
        tokens = [token for token in result['partitions']['TOKEN']]
        print(tokens)
        # check part of speech tagging
        pos = [token['pos'] for token in tokens]
        assert pos == ['ART', 'NN', 'VVFIN', 'ADV', 'ART', 'NN']
        # check correct indices (including title + 1 offset)
        starts = [token['start'] - len(doc['title']) - 1 for token in tokens]
        ends = [token['end'] - len(doc['title']) - 1 for token in tokens]
        assert [text[slice(*char_range)] for char_range in zip(starts, ends)] == text.split()

        # check dependency: articles as dependents of their
        # respective nouns (dependency type 'det'), first noun phrase as subject
        # (nsubj) of verb, second noun phrase as direct object (dobj) of verb,
        # adverb as modifier of verb ('advmod')
        parents = [token['dependency']['parent'] for token in tokens]
        assert parents == [1, 2, -1, 2, 5, 2]
        # current result 19-08-14:  [-1, 2, 3,  0, 3, 6]
        dependeny_labels = [token['dependency']['label'] for token in tokens]
        assert dependeny_labels == ['det', 'nsubj', 'ROOT', 'advmod', 'det', 'dobj']
        # current 19-08-14: ['null', 'det', 'nsubj', 'ROOT', 'advmod', 'det']


if __name__ == '__main__':
    unittest.main()
