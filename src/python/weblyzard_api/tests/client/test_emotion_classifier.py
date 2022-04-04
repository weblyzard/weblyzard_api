#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on April 22, 2021

@author: jakob <jakob.steixner@modul.ac.at>
'''

from os import getenv
import unittest
import pytest

from weblyzard_api.client.emotion_classifier_client import EmotionClassifierClient

from weblyzard_api.model.document import Document
from weblyzard_api.xml_content import XMLContent

@pytest.fixture
def client():
    webservice_url = getenv('WL_TEST_OPINION_MINING', 'http://emotion-classifier.prod.i.weblyzard.net:8443')
    # webservice_url = getenv('WL_TEST_OPINION_MINING', 'http://localhost:5000')
    if webservice_url is None:
        return
    client = EmotionClassifierClient(url=webservice_url)
    return client


class TestOpinionClient(object):
    def test_wl_document(self, client):
        json =  {'id': '192292',
 'format': 'html/text',
 'lang': 'EN',
 'nilsimsa': '5782914100084A0E35812C84048A54D50148B808C9457217DFA810C04084C2C4',
 'header': {},
 'content': 'I am very relieved about how easy this was.',
 'partitions': {'BODY': [{'@type': 'CharSpan', 'start': 0, 'end': 43}],
  'LINE': [{'@type': 'CharSpan', 'start': 0, 'end': 43}],
  'SENTENCE': [{'@type': 'SentenceCharSpan',
    'start': 0,
    'end': 43,
    'id': 'e0c99f54a11c056fc552a9587463407f'}],
  'TOKEN': [{'@type': 'TokenCharSpan',
    'start': 0,
    'end': 1,
    'pos': 'PRP',
    'dependency': {'parent': 1, 'label': 'SBJ'}},
   {'@type': 'TokenCharSpan',
    'start': 2,
    'end': 4,
    'pos': 'VBP',
    'dependency': {'parent': -1, 'label': 'ROOT'}},
   {'@type': 'TokenCharSpan',
    'start': 5,
    'end': 9,
    'pos': 'RB',
    'dependency': {'parent': 3, 'label': 'AMOD'}},
   {'@type': 'TokenCharSpan',
    'start': 10,
    'end': 18,
    'pos': 'JJ',
    'dependency': {'parent': 1, 'label': 'PRD'}},
   {'@type': 'TokenCharSpan',
    'start': 19,
    'end': 24,
    'pos': 'IN',
    'dependency': {'parent': 3, 'label': 'AMOD'}},
   {'@type': 'TokenCharSpan',
    'start': 25,
    'end': 28,
    'pos': 'WRB',
    'dependency': {'parent': 8, 'label': 'PRD'}},
   {'@type': 'TokenCharSpan',
    'start': 29,
    'end': 33,
    'pos': 'JJ',
    'dependency': {'parent': 5, 'label': 'AMOD'}},
   {'@type': 'TokenCharSpan',
    'start': 34,
    'end': 38,
    'pos': 'DT',
    'dependency': {'parent': 8, 'label': 'SBJ'}},
   {'@type': 'TokenCharSpan',
    'start': 39,
    'end': 42,
    'pos': 'VBD',
    'dependency': {'parent': 4, 'label': 'PMOD'}},
   {'@type': 'TokenCharSpan',
    'start': 42,
    'end': 43,
    'pos': '.',
    'dependency': {'parent': 1, 'label': 'P'}}],
  'FRAGMENT': []},
 'annotations': []}

        document = Document.from_dict(json)
        print(document.content_type)
        result = client.get_emotions(content=document.to_dict(),
                                     content_format='json')
        print(result)
        document = Document.from_dict(dict_=result['content'])
        document_polarity = result['polarity']
        assert result['sentiment_values']
        assert result['sentiment_values']['calmness_anger-full'] > 0.5
        assert document_polarity > 0.5

        print('successfully run test against endpoint {}'.format(
            client.get_service_urls()
        ))
