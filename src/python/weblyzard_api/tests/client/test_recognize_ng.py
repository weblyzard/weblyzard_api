#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2016

.. codeauthor: max goebel <mcgoebel@gmail.com>
'''
from __future__ import print_function
from __future__ import unicode_literals
import unittest

from weblyzard_api.client.recognize.ng import Recognize


class TestRecognizeNg(unittest.TestCase):

    SERVICE_URL = 'localhost:63007/rest'
    PROFILE_NAME = 'wl_full_international_en'
    DOCUMENTS = [{u'annotations': [],
                  u'content': u'Hello "world" more \nDonald Trump and Barack Obama are presidents in the United States. Vienna is the capital of Austria, Berlin is the capital of Germany. Linz also is in Austria" 1000',
                  u'format': u'text/html',
                  u'header': {},
                  u'id': u'1000',
                  u'lang': u'EN',
                  u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C06650B80E6ED',
                  u'partitions': {u'BODY': [{u'@type': u'CharSpan',
                                             u'end': 184,
                                             u'start': 20}],
                                  u'LINE': [{u'@type': u'CharSpan', u'end': 19, u'start': 0},
                                            {u'@type': u'CharSpan',
                                             u'end': 184,
                                             u'start': 20}],
                                  u'SENTENCE': [{u'@type': u'SentenceCharSpan',
                                                 u'end': 18,
                                                 u'id': u'26d2d0113429b0dc98352c2b5fd842a1',
                                                 u'semOrient': 0.0,
                                                 u'significance': 0.0,
                                                 u'start': 0},
                                                {u'@type': u'SentenceCharSpan',
                                                 u'end': 86,
                                                 u'id': u'ddbe82fc058d01f347dda640aa123e76',
                                                 u'semOrient': 0.0,
                                                 u'significance': 0.0,
                                                 u'start': 20},
                                                {u'@type': u'SentenceCharSpan',
                                                 u'end': 154,
                                                 u'id': u'aef32ea74929a8ff3828e6285da0f915',
                                                 u'semOrient': 0.0,
                                                 u'significance': 0.0,
                                                 u'start': 87},
                                                {u'@type': u'SentenceCharSpan',
                                                 u'end': 184,
                                                 u'id': u'94ae0254cdd4396fb2adbfea90676563',
                                                 u'semOrient': 0.0,
                                                 u'significance': 0.0,
                                                 u'start': 155}],
                                  u'TITLE': [{u'@type': u'CharSpan', u'end': 19, u'start': 0}],
                                  u'TOKEN': [{u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'null',
                                                              u'parent': -1},
                                              u'end': 5,
                                              u'pos': u'UH',
                                              u'start': 0},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NMOD',
                                                              u'parent': 3},
                                              u'end': 7,
                                              u'pos': u"'",
                                              u'start': 6},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'SUFFIX',
                                                              u'parent': 1},
                                              u'end': 12,
                                              u'pos': u'NN',
                                              u'start': 7},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'ROOT',
                                                              u'parent': 0},
                                              u'end': 13,
                                              u'pos': u"'",
                                              u'start': 12},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'SUFFIX',
                                                              u'parent': 3},
                                              u'end': 18,
                                              u'pos': u'RBR',
                                              u'start': 14},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'null',
                                                              u'parent': -1},
                                              u'end': 26,
                                              u'pos': u'NNP',
                                              u'start': 20},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NAME',
                                                              u'parent': 2},
                                              u'end': 32,
                                              u'pos': u'NNP',
                                              u'start': 27},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'SBJ',
                                                              u'parent': 6},
                                              u'end': 36,
                                              u'pos': u'CC',
                                              u'start': 33},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'COORD',
                                                              u'parent': 2},
                                              u'end': 43,
                                              u'pos': u'NNP',
                                              u'start': 37},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NAME',
                                                              u'parent': 5},
                                              u'end': 49,
                                              u'pos': u'NNP',
                                              u'start': 44},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'CONJ',
                                                              u'parent': 3},
                                              u'end': 53,
                                              u'pos': u'VBP',
                                              u'start': 50},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'ROOT',
                                                              u'parent': 0},
                                              u'end': 64,
                                              u'pos': u'NNS',
                                              u'start': 54},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'PRD',
                                                              u'parent': 6},
                                              u'end': 67,
                                              u'pos': u'IN',
                                              u'start': 65},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'LOC',
                                                              u'parent': 7},
                                              u'end': 71,
                                              u'pos': u'DT',
                                              u'start': 68},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NMOD',
                                                              u'parent': 11},
                                              u'end': 78,
                                              u'pos': u'NNP',
                                              u'start': 72},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NMOD',
                                                              u'parent': 11},
                                              u'end': 85,
                                              u'pos': u'NNPS',
                                              u'start': 79},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'PMOD',
                                                              u'parent': 8},
                                              u'end': 86,
                                              u'pos': u'.',
                                              u'start': 85},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'null',
                                                              u'parent': -1},
                                              u'end': 93,
                                              u'pos': u'NNP',
                                              u'start': 87},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'SBJ',
                                                              u'parent': 2},
                                              u'end': 96,
                                              u'pos': u'VBZ',
                                              u'start': 94},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'ROOT',
                                                              u'parent': 0},
                                              u'end': 100,
                                              u'pos': u'DT',
                                              u'start': 97},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NMOD',
                                                              u'parent': 4},
                                              u'end': 108,
                                              u'pos': u'NN',
                                              u'start': 101},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'PRD',
                                                              u'parent': 2},
                                              u'end': 111,
                                              u'pos': u'IN',
                                              u'start': 109},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NMOD',
                                                              u'parent': 4},
                                              u'end': 119,
                                              u'pos': u'NNP',
                                              u'start': 112},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'PMOD',
                                                              u'parent': 5},
                                              u'end': 120,
                                              u'pos': u',',
                                              u'start': 119},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'P', u'parent': 9},
                                              u'end': 127,
                                              u'pos': u'NNP',
                                              u'start': 121},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'SBJ',
                                                              u'parent': 9},
                                              u'end': 130,
                                              u'pos': u'VBZ',
                                              u'start': 128},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'DEP',
                                                              u'parent': 14},
                                              u'end': 134,
                                              u'pos': u'DT',
                                              u'start': 131},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NMOD',
                                                              u'parent': 11},
                                              u'end': 142,
                                              u'pos': u'NN',
                                              u'start': 135},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'PRD',
                                                              u'parent': 9},
                                              u'end': 145,
                                              u'pos': u'IN',
                                              u'start': 143},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NMOD',
                                                              u'parent': 11},
                                              u'end': 153,
                                              u'pos': u'NNP',
                                              u'start': 146},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'PMOD',
                                                              u'parent': 12},
                                              u'end': 154,
                                              u'pos': u'.',
                                              u'start': 153},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'null',
                                                              u'parent': -1},
                                              u'end': 159,
                                              u'pos': u'NNP',
                                              u'start': 155},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'SBJ',
                                                              u'parent': 3},
                                              u'end': 164,
                                              u'pos': u'RB',
                                              u'start': 160},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'ADV',
                                                              u'parent': 3},
                                              u'end': 167,
                                              u'pos': u'VBZ',
                                              u'start': 165},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'ROOT',
                                                              u'parent': 0},
                                              u'end': 170,
                                              u'pos': u'IN',
                                              u'start': 168},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'LOC-PRD',
                                                              u'parent': 3},
                                              u'end': 178,
                                              u'pos': u'NNP',
                                              u'start': 171},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'HMOD',
                                                              u'parent': 7},
                                              u'end': 179,
                                              u'pos': u"'",
                                              u'start': 178},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'SUFFIX',
                                                              u'parent': 5},
                                              u'end': 184,
                                              u'pos': u'CD',
                                              u'start': 180}]}}]

    def setUp(self):
        self.available_profiles = []
        self.client = Recognize(self.SERVICE_URL)
        self.service_is_online = self.client.is_online()
        if not self.service_is_online:
            print('WARNING: Webservice is offline --> not executing all tests!!')
            self.IS_ONLINE = False
            return

    def test_available_profiles(self):
        profiles = self.client.list_profiles()
        assert len(profiles) > 0

#     def test_search_text(self):
#         text = 'Vienna is the capital of Austria, Berlin is the capital of Germany. Linz also is in Austria'
#         result = self.client.search_text(
#             self.PROFILE_NAME, lang='en', text=text)
#         assert len(result) == 6

    def test_annotate_document(self):
        for document in self.DOCUMENTS:
            result = self.client.search_document(profile_name=self.PROFILE_NAME,
                                                 document=document, limit=0)
            annotations = result['annotations']
            from pprint import pprint
            pprint(annotations)

            assert len(annotations) > 0


if __name__ == '__main__':
    unittest.main()
