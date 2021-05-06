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
from wl_core_ng.analyzers.emotion_classifier import EmotionClassifier

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
        json =  """{
  "id": "192292",
  "format": "html/text",
  "lang": "EN",
  "nilsimsa": "3F0F7C39387A290C62792ABD3FDB1353DDDA43A2E9E03CFA395B34926CC66251",
  "header": {},
  "content": "This was a very positive experience which I wholeheartedly recommend to anybody interested.",
  "partitions": {
    "BODY": [
      {
        "@type": "CharSpan",
        "start": 0,
        "end": 91
      }
    ],
    "LINE": [
      {
        "@type": "CharSpan",
        "start": 0,
        "end": 91
      }
    ],
    "SENTENCE": [
      {
        "@type": "SentenceCharSpan",
        "start": 0,
        "end": 91,
        "id": "03a651aa4fbae6409d6a867fb65755e6"
      }
    ],
    "TOKEN": [
      {
        "@type": "TokenCharSpan",
        "start": 0,
        "end": 4,
        "pos": "DT",
        "dependency": {
          "parent": 1,
          "label": "SBJ"
        }
      },
      {
        "@type": "TokenCharSpan",
        "start": 5,
        "end": 8,
        "pos": "VBD",
        "dependency": {
          "parent": -1,
          "label": "ROOT"
        }
      },
      {
        "@type": "TokenCharSpan",
        "start": 9,
        "end": 10,
        "pos": "DT",
        "dependency": {
          "parent": 5,
          "label": "NMOD"
        }
      },
      {
        "@type": "TokenCharSpan",
        "start": 11,
        "end": 15,
        "pos": "RB",
        "dependency": {
          "parent": 4,
          "label": "AMOD"
        }
      },
      {
        "@type": "TokenCharSpan",
        "start": 16,
        "end": 24,
        "pos": "JJ",
        "dependency": {
          "parent": 5,
          "label": "NMOD"
        }
      },
      {
        "@type": "TokenCharSpan",
        "start": 25,
        "end": 35,
        "pos": "NN",
        "dependency": {
          "parent": 1,
          "label": "PRD"
        }
      },
      {
        "@type": "TokenCharSpan",
        "start": 36,
        "end": 41,
        "pos": "WDT",
        "dependency": {
          "parent": 9,
          "label": "OBJ"
        }
      },
      {
        "@type": "TokenCharSpan",
        "start": 42,
        "end": 43,
        "pos": "PRP",
        "dependency": {
          "parent": 9,
          "label": "SBJ"
        }
      },
      {
        "@type": "TokenCharSpan",
        "start": 44,
        "end": 58,
        "pos": "RB",
        "dependency": {
          "parent": 9,
          "label": "MNR"
        }
      },
      {
        "@type": "TokenCharSpan",
        "start": 59,
        "end": 68,
        "pos": "VB",
        "dependency": {
          "parent": 1,
          "label": "VC"
        }
      },
      {
        "@type": "TokenCharSpan",
        "start": 69,
        "end": 71,
        "pos": "TO",
        "dependency": {
          "parent": 9,
          "label": "ADV"
        }
      },
      {
        "@type": "TokenCharSpan",
        "start": 72,
        "end": 79,
        "pos": "NN",
        "dependency": {
          "parent": 10,
          "label": "PMOD"
        }
      },
      {
        "@type": "TokenCharSpan",
        "start": 80,
        "end": 90,
        "pos": "JJ",
        "dependency": {
          "parent": 11,
          "label": "NMOD"
        }
      },
      {
        "@type": "TokenCharSpan",
        "start": 90,
        "end": 91,
        "pos": ".",
        "dependency": {
          "parent": 1,
          "label": "P"
        }
      }
    ]
  },
  "annotations": []
}"""

        document = Document.from_json(json)
        print(document.content_type)
        result = client.get_emotions(content=document.to_dict(),
                                     content_format='json')
        print(result)
        document = Document.from_dict(dict_=result['content'])
        document_polarity = result['polarity']
        assert result['emotions']
        assert result['emotions']['attitude'] > 0.5
        assert document_polarity > 0.5
        assert (
            set(result['dominant_emotion'].keys()) == {'attitude'}
        )

        print('successfully run test against endpoint {}'.format(
            client.get_service_urls()
        ))
