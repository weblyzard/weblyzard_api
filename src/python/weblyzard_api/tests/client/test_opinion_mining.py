# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from builtins import object
from os import getenv

import unittest
import pytest

from weblyzard_api.client.opinion_mining import OpinionClient
from weblyzard_api.model.document import Document
from weblyzard_api.xml_content import XMLContent

@pytest.fixture
def client():
    webservice_url = getenv('WL_TEST_OPINION_MINING', None)
    if webservice_url is None:
        return
    client = OpinionClient(url=webservice_url)
    return client


class TestOpinionClient(object):

    def test_xmlcontent(self, client):
        '''Tests correct handling of XMLContent as input.'''
        xml_content_str = '''<?xml version="1.0" encoding="UTF-8"?><wl:page xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://www.weblyzard.com/wl/2013#" wl:id="192292" dc:format="html/text" xml:lang="en" wl:nilsimsa="172f424f78b62bc2487273e82d9353d586abd1611b3b3551287d3287ee25c548"><wl:sentence wl:id="f1e58cb716f51559baa4dfe20557803e" wl:pos="DT VBZ RB JJR . " wl:dependency="1 -1 3 1 1 " wl:token="0,4 5,7 8,16 17,23 23,24" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[This is slightly better.]]></wl:sentence></wl:page>'''
        result = client.get_polarity(content=xml_content_str,
                                          content_format='xml')
        print(result)
        polarity_value = result['polarity']
        assert polarity_value == 1.0
        xml_content = XMLContent(result['content'])
        assert xml_content.sentences[0].sem_orient == 1.0
        assert xml_content.sentences[0].sem_orient == polarity_value

    def test_wl_document(self, client):
        json = '''{"lang": "DE", "format": "text/plain", "annotations": [], "content": "Ehre sei dem Vater, dem Sohn und dem Heiligen Geist. Wie im Anfang so auch jetzt und alle Zeit und in Ewigkeit Amen.", "header": {}, "id": "192292", "nilsimsa": "18495A20A2AC1180A9470AC7AA7D4C2244CA93596106D3A148AEA8BED9D0F697", "partitions": {"BODY": [{"start": 0, "end": 116, "@type": "CharSpan"}], "LINE": [{"start": 0, "end": 116, "@type": "CharSpan"}], "TOKEN": [{"start": 0, "dependency": {"parent": -1, "label": "null"}, "end": 4, "@type": "TokenCharSpan", "pos": "NN"}, {"start": 5, "dependency": {"parent": 2, "label": "nsubj"}, "end": 8, "@type": "TokenCharSpan", "pos": "VAFIN"}, {"start": 9, "dependency": {"parent": 0, "label": "ROOT"}, "end": 12, "@type": "TokenCharSpan", "pos": "ART"}, {"start": 13, "dependency": {"parent": 4, "label": "det"}, "end": 18, "@type": "TokenCharSpan", "pos": "NN"}, {"start": 18, "dependency": {"parent": 2, "label": "attr"}, "end": 19, "@type": "TokenCharSpan", "pos": "$,"}, {"start": 20, "dependency": {"parent": 4, "label": "p"}, "end": 23, "@type": "TokenCharSpan", "pos": "ART"}, {"start": 24, "dependency": {"parent": 7, "label": "det"}, "end": 28, "@type": "TokenCharSpan", "pos": "NN"}, {"start": 29, "dependency": {"parent": 4, "label": "appos"}, "end": 32, "@type": "TokenCharSpan", "pos": "KON"}, {"start": 33, "dependency": {"parent": 7, "label": "cc"}, "end": 36, "@type": "TokenCharSpan", "pos": "ART"}, {"start": 37, "dependency": {"parent": 11, "label": "det"}, "end": 45, "@type": "TokenCharSpan", "pos": "ADJA"}, {"start": 46, "dependency": {"parent": 11, "label": "amod"}, "end": 51, "@type": "TokenCharSpan", "pos": "NN"}, {"start": 51, "dependency": {"parent": 7, "label": "conj"}, "end": 52, "@type": "TokenCharSpan", "pos": "$."}, {"start": 53, "dependency": {"parent": -1, "label": "null"}, "end": 56, "@type": "TokenCharSpan", "pos": "PWAV"}, {"start": 57, "dependency": {"parent": 13, "label": "advmod"}, "end": 59, "@type": "TokenCharSpan", "pos": "APPRART"}, {"start": 60, "dependency": {"parent": 13, "label": "adpmod"}, "end": 66, "@type": "TokenCharSpan", "pos": "NN"}, {"start": 67, "dependency": {"parent": 2, "label": "adpobj"}, "end": 69, "@type": "TokenCharSpan", "pos": "ADV"}, {"start": 70, "dependency": {"parent": 5, "label": "advmod"}, "end": 74, "@type": "TokenCharSpan", "pos": "ADV"}, {"start": 75, "dependency": {"parent": 6, "label": "advmod"}, "end": 80, "@type": "TokenCharSpan", "pos": "ADV"}, {"start": 81, "dependency": {"parent": 13, "label": "advmod"}, "end": 84, "@type": "TokenCharSpan", "pos": "KON"}, {"start": 85, "dependency": {"parent": 6, "label": "cc"}, "end": 89, "@type": "TokenCharSpan", "pos": "PIDAT"}, {"start": 90, "dependency": {"parent": 9, "label": "det"}, "end": 94, "@type": "TokenCharSpan", "pos": "NN"}, {"start": 95, "dependency": {"parent": 6, "label": "conj"}, "end": 98, "@type": "TokenCharSpan", "pos": "KON"}, {"start": 99, "dependency": {"parent": 6, "label": "cc"}, "end": 101, "@type": "TokenCharSpan", "pos": "APPR"}, {"start": 102, "dependency": {"parent": 13, "label": "adpmod"}, "end": 110, "@type": "TokenCharSpan", "pos": "NN"}, {"start": 111, "dependency": {"parent": 11, "label": "adpobj"}, "end": 115, "@type": "TokenCharSpan", "pos": "VVINF"}, {"start": 115, "dependency": {"parent": 0, "label": "ROOT"}, "end": 116, "@type": "TokenCharSpan", "pos": "$."}], "SENTENCE": [{"end": 52, "id": 1, "start": 0, "semOrient": 0.0, "significance": 0.0, "@type": "SentenceCharSpan"}, {"end": 116, "id": 2, "start": 53, "semOrient": 0.0, "significance": 0.0, "@type": "SentenceCharSpan"}]}}'''
        document = Document.from_json(json)
        print(document.content_type)
        result = client.get_polarity(content=document.to_dict(),
                                          content_format='json')
        print(result)
        document = Document.from_dict(dict_=result['content'])
        document_polarity = result['polarity']
        assert document_polarity - 0.710669054519 < 1e-8
        for sentence in document.get_sentences():
            if sentence.value == 'Ehre sei dem Vater, dem Sohn und dem Heiligen Geist.':
                assert sentence.sem_orient == 1.0
            elif sentence.value == 'Wie im Anfang so auch jetzt und alle Zeit und in Ewigkeit Amen.':
                assert sentence.sem_orient == 0.0
