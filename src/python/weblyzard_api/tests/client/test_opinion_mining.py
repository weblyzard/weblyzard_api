# -*- coding: utf-8 -*-

from os import getenv

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
        assert document_polarity == 0.8606629658238704
        for sentence in document.get_sentences():
            if sentence.value == 'Ehre sei dem Vater, dem Sohn und dem Heiligen Geist.':
                assert sentence.sem_orient == 1.0
            elif sentence.value == 'Wie im Anfang so auch jetzt und alle Zeit und in Ewigkeit Amen.':
                assert sentence.sem_orient == 0.0

    def test_negation_triggers(self, client):
        """Tests negation of sentiment keywords by triggers 'weder-noch'"""
        xml_content_str = '''<?xml version="1.0" encoding="UTF-8"?><wl:page xmlns:wl="http://www.weblyzard.com/wl/2013#" xmlns:dc="http://purl.org/dc/elements/1.1/" wl:id="192292" dc:format="html/text" xml:lang="de" wl:nilsimsa="79FD4E2402678A0016BBCDFCFEE37640406C39B21B793CE9FFB94FC2BE8BF374"><wl:sentence wl:id="54a4f9cbfc85df3b197ad5db2dc22cc9" wl:pos="ART ADJA NN VAFIN KON ADJD KON ADJD $." wl:dependency="2:det 2:amod 3:nsubj -1:ROOT 3:cc 3:acomp 5:cc 5:conj 3:p" wl:token="0,3 4,14 15,21 22,25 26,31 32,40 41,45 46,58 58,59" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[Das derzeitige Gesetz ist weder sinnvoll noch verständlich.]]></wl:sentence></wl:page>'''
        result = client.get_polarity(content=xml_content_str,
                                     content_format='xml')
        print(result)
        polarity_value = result['polarity']
        assert polarity_value == -1.0
        xml_content = XMLContent(result['content'])
        assert xml_content.sentences[0].sem_orient == -1.0
        assert xml_content.sentences[0].sem_orient == polarity_value

    def test_ngram(self, client):
        """Tests that 'nicht nur' is not treated as negation"""
        xml_content_str = """<?xml version="1.0" encoding="UTF-8"?><wl:page xmlns:wl="http://www.weblyzard.com/wl/2013#" xmlns:dc="http://purl.org/dc/elements/1.1/" wl:id="192292" dc:format="html/text" xml:lang="de" wl:nilsimsa="7224521128026A4684A089F17C8344C415D2EFE11C8C0C53B439489133802200"><wl:sentence wl:id="bc570f2b4355afdddbacf18f511e95ef" wl:pos="PPER VAFIN PTKNEG ADV ART ADJA NN $, KON ADV ART NN VAFIN ADJD $." wl:dependency="1:nsubj -1:ROOT 1:neg 1:advmod 6:det 6:amod 1:attr 6:p 6:cc 12:advmod 11:det 12:nsubj 6:conj 12:acomp 1:p" wl:token="0,2 3,6 7,12 13,16 17,20 21,28 29,34 34,35 36,43 44,48 49,52 53,58 59,62 63,72 72,73" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[Es war nicht nur ein schöner Abend, das Essen war auch OK.]]></wl:sentence></wl:page>"""
        result = client.get_polarity(content=xml_content_str,
                                     content_format='xml')
        print(result)
        polarity_value = result['polarity']
        assert polarity_value > 0.75
        xml_content = XMLContent(result['content'])
        assert xml_content.sentences[0].sem_orient == polarity_value

    def test_typographic_apostrophe(self, client):
        """test that 'don’t' with typographic apostrophe is treated as negation
        """
        xml_content_str = """<?xml version="1.0" encoding="UTF-8"?><wl:page xmlns:wl="http://www.weblyzard.com/wl/2013#" xmlns:dc="http://purl.org/dc/elements/1.1/" wl:id="192292" dc:format="html/text" xml:lang="en" wl:nilsimsa="6F92A322007A903D184E885A922A8443EAB5F2EF27AAC6C3A1344EB86484286C"><wl:sentence wl:id="134d482a918027336f03bc0db4d0a26e" wl:pos="' PRP VBP RB VB PRP POS DT JJ NN TO VB ' ." wl:dependency="-1:SUFFIX 2:SBJ 13:DEP 2:ADV 2:VC 4:OBJ 9:NMOD 9:NMOD 9:NMOD 4:EXT 9:NMOD 10:IM 11:SUFFIX 0:NMOD" wl:token="0,1 1,2 3,5 5,8 9,14 15,17 17,19 20,23 24,29 30,34 35,37 38,43 43,44 44,45" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[“I don’t think it’s the right call to leave”.]]></wl:sentence></wl:page>"""
        result = client.get_polarity(content=xml_content_str,
                                     content_format='xml')
        print(result)
        polarity_value = result['polarity']
        assert polarity_value <= 0.0
        xml_content = XMLContent(result['content'])
        assert xml_content.sentences[0].sem_orient == polarity_value

    def test_non_typographic_apostrophe(self, client):
        """test that 'don't' with straight single quote is treated as negation
        """
        xml_content_str = """<?xml version="1.0" encoding="UTF-8"?><wl:page xmlns:wl="http://www.weblyzard.com/wl/2013#" xmlns:dc="http://purl.org/dc/elements/1.1/" wl:id="192292" dc:format="html/text" xml:lang="en" wl:nilsimsa="69B6A512007A8039114C808300820647E3C4F4E30522D043013CCABA6458202C"><wl:sentence wl:id="1ee48705d522621ad6d8a0301fbcc751" wl:pos="PRP VBP RB VB PRP VBZ DT JJ NN TO VB ." wl:dependency="1:SBJ -1:ROOT 1:ADV 1:VC 5:SBJ 3:OBJ 8:NMOD 8:NMOD 5:PRD 8:NMOD 9:IM 1:P" wl:token="0,1 2,4 4,7 8,13 14,16 16,18 19,22 23,28 29,33 34,36 37,42 42,43" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[I don't think it's the right call to leave.]]></wl:sentence></wl:page>"""
        result = client.get_polarity(content=xml_content_str,
                                     content_format='xml')
        print(result)
        polarity_value = result['polarity']
        assert polarity_value < 0.0
        xml_content = XMLContent(result['content'])
        assert xml_content.sentences[0].sem_orient == polarity_value
