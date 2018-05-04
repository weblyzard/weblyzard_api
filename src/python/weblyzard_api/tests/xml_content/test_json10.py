#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import pytest
import unittest

from weblyzard_api.xml_content.parsers.json_10 import (JSON10ParserSentence,
                                                       MalformedJSONException,
                                                       JSON10ParserXMLContent,
                                                       UnexpectedFieldException,
                                                       MissingFieldException)
from weblyzard_api.xml_content import Sentence, XMLContent


class TestJSON10ParserXMLContent(unittest.TestCase):
    '''
    Tests for the JSON_10_Parser class.
    '''
    test_xmlcontent_minimal_dict = {
        'uri': 'derstandard.at/',
        'title': 'Test title'
    }
    test_xmlcontent_maximal_dict = {
        'uri': 'derstandard.at/',
        'title': 'document title',
        'language_id': 'en',
        'sentences': [
            {
                'value': 'Therefore we could show that "x>y" and "y<z.".',
                'id': '6e4c1420b2edaa374ff9d2300b8df31d',
                'is_title': False,
                'pos_list': "RB PRP MD VB IN ' CC JJR JJ ' CC ' NN JJR CD ' .",
                'tok_list': '0,9 10,12 13,18 19,23 24,28 29,30 30,31 31,32 32,33 33,34 35,38 39,40 40,41 41,42 42,44 44,45 45,46',
                'dep_tree': '2:ADV 2:SBJ 16:DEP 2:VC 3:OBJ 3:P 16:DEP 8:AMOD 16:DEP 8:P 8:COORD 10:P 10:CONJ 14:NMOD 12:COORD 14:P -1:ROOT',
                'polarity': 0.0,
            },
        ],
    }
    xml_content_string = '''
        <?xml version="1.0" encoding="UTF-8"?>
        <wl:page xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://www.weblyzard.com/wl/2013#" wl:id="99933" dc:format="text/html" xml:lang="en" wl:nilsimsa="c3f00c9bae798a55a013209ceba9012f4d2349f7c1b2486529674a05ef7be8fb" dc:identifier="http://www.heise.de" dc:related="http://www.heise.de http://www.kurier.at">
           <wl:sentence wl:id="27cd03a5aaac20ae0dba60038f17fdad" wl:is_title="True" wl:pos="JJ NN ." wl:token="0,6 7,14 14,15" wl:sem_orient="0.0" wl:significance="1.5"><![CDATA[Global Dimming.]]></wl:sentence>
           <wl:sentence wl:id="7f3251087b6552159846493558742f18" wl:pos="( CD NNP NN ) IN NNS VBD IN DT CD , NNS VBP VBN IN EX VBZ VBN DT NN IN NN VBG DT NNP : PRP VBD PRP JJ NN ." wl:token="0,1 1,2 2,6 7,18 18,19 20,25 26,38 39,44 45,47 48,51 52,57 57,58 59,69 70,74 75,85 86,90 91,96 97,100 101,105 106,107 108,115 116,118 119,127 128,136 137,140 141,146 146,147 148,152 153,159 160,162 163,169 170,177 177,178" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[(*FULL DOCUMENTARY) Since measurements began in the 1950s, scientists have discovered that there has been a decline of sunlight reaching the Earth; they called it global dimming.]]></wl:sentence>
           <wl:sentence wl:id="93f56b9d196787d1cf662a06ab5f866b" wl:pos="CC VBG TO DT NN VBN IN DT NN IN NNP , DT NN VBD RB VB IN DT CD CC RB IN DT CD NNS VBP VBN DT JJ VBG ." wl:token="0,3 4,13 14,16 17,18 19,24 25,34 35,37 38,41 42,49 50,52 53,60 60,61 62,65 66,73 74,77 78,81 82,90 91,95 96,99 100,105 106,109 110,116 117,122 123,126 127,132 133,143 144,148 149,157 158,159 160,170 171,182 182,183" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[But according to a paper published in the journal of Science, the dimming did not continue into the 1990s and indeed since the 1980s scientists have observed a widespread brightening.]]></wl:sentence>
         </wl:page>
    '''

    def test_unexpected_document_fields(self):
        '''
        Tests that the parser rejects documents with unexpected fields.
        '''
        testkey = 'testkey'
        assert testkey not in JSON10ParserXMLContent.FIELDS_REQUIRED
        assert testkey not in JSON10ParserXMLContent.FIELDS_OPTIONAL
        xmldict_ = dict(self.test_xmlcontent_minimal_dict)
        xmldict_[testkey] = 'random'
        with pytest.raises(UnexpectedFieldException):
            JSON10ParserXMLContent.from_json_string(
                json.dumps(xmldict_))

    def test_required_document_fields(self):
        '''
        Test for checking that all required document fields are present in the JSON.
        '''
        for key in self.test_xmlcontent_minimal_dict:
            xmldict_ = dict(self.test_xmlcontent_minimal_dict)
            del xmldict_[key]
            with pytest.raises(MissingFieldException):
                JSON10ParserXMLContent.from_json_string(json.dumps(xmldict_))
        assert JSON10ParserXMLContent.from_json_string(
            json.dumps(self.test_xmlcontent_minimal_dict)) is not None

    def test_minimal_xmlcontent_from_json(self):
        '''
        Tests for the correct conversion from a JSON string.
        '''
        xmlcontent = JSON10ParserXMLContent.from_json_string(
            json.dumps(self.test_xmlcontent_minimal_dict))

    def test_document_to_json(self):
        '''
        Tests for the correct serialization as JSON of a XMLContent
        object.
        '''
        result = json.loads(
            JSON10ParserXMLContent.from_json_string(
                json.dumps(self.test_xmlcontent_minimal_dict)
            ).to_json(version=1.0))

        assert self.test_xmlcontent_minimal_dict == result
        assert self.test_xmlcontent_maximal_dict == json.loads(
            JSON10ParserXMLContent.from_json_string(
                json.dumps(self.test_xmlcontent_maximal_dict)
            ).to_json(version=1.0))

    def test_document_xml_dict(self):
        '''
        Tests that starting with an XML string, we get the
        correct JSON with only expected attributes.
        '''
        xml_content = XMLContent(self.xml_content_string)
        api_dict = xml_content.to_api_dict(version=1.0)

        assert api_dict == {
            'uri': 'http://www.heise.de',
            'language_id': 'en',
            'title': 'Global Dimming.',
            'sentences': [
                {'polarity': 0.0,
                 'value': 'Global Dimming.',
                 'pos_list': 'JJ NN .',
                 'tok_list': '0,6 7,14 14,15',
                 'is_title': 'True',
                 'id': '27cd03a5aaac20ae0dba60038f17fdad'},
                {'id': '7f3251087b6552159846493558742f18',
                 'is_title': False,
                 'polarity': 0.0,
                 'pos_list': '( CD NNP NN ) IN NNS VBD IN DT CD , NNS VBP VBN IN EX VBZ VBN DT NN IN NN VBG DT NNP : PRP VBD PRP JJ NN .',
                 'tok_list': '0,1 1,2 2,6 7,18 18,19 20,25 26,38 39,44 45,47 48,51 52,57 57,58 59,69 70,74 75,85 86,90 91,96 97,100 101,105 106,107 108,115 116,118 119,127 128,136 137,140 141,146 146,147 148,152 153,159 160,162 163,169 170,177 177,178',
                 'value': '(*FULL DOCUMENTARY) Since measurements began in the 1950s, scientists have discovered that there has been a decline of sunlight reaching the Earth; they called it global dimming.'},
                {'id': '93f56b9d196787d1cf662a06ab5f866b',
                 'is_title': False,
                 'polarity': 0.0,
                 'pos_list': 'CC VBG TO DT NN VBN IN DT NN IN NNP , DT NN VBD RB VB IN DT CD CC RB IN DT CD NNS VBP VBN DT JJ VBG .',
                 'tok_list': '0,3 4,13 14,16 17,18 19,24 25,34 35,37 38,41 42,49 50,52 53,60 60,61 62,65 66,73 74,77 78,81 82,90 91,95 96,99 100,105 106,109 110,116 117,122 123,126 127,132 133,143 144,148 149,157 158,159 160,170 171,182 182,183',
                 'value': 'But according to a paper published in the journal of Science, the dimming did not continue into the 1990s and indeed since the 1980s scientists have observed a widespread brightening.'}
            ],
        }

    def test_incoherent_title(self):
        '''
        Tests that we raise exception if a sentence marked as
        title and the title attribute mismatch.
        '''
        xml_content = XMLContent(self.xml_content_string)
        api_dict = xml_content.to_api_dict(version=1.0)
        api_dict['title'] = 'wrongtitle'
        try:
            xml_content = JSON10ParserXMLContent.from_api_dict(api_dict)
            assert xml_content == False
        except MalformedJSONException as e:
            assert 'is_title' in e.message


class TestJSON10ParserSentence(object):
    test_sentence = Sentence(
        md5sum=u'6e4c1420b2edaa374ff9d2300b8df31d',
        pos=u"RB PRP MD VB IN ' CC JJR JJ ' CC ' NN JJR CD ' .",
        sem_orient=0.0,
        significance=0.0,
        token=u'0,9 10,12 13,18 19,23 24,28 29,30 30,31 31,32 32,33 33,34 35,38 39,40 40,41 41,42 42,44 44,45 45,46',
        value=u'Therefore we could show that "x>y" and "y<z.".',
        is_title=False,
        dependency=u'2:ADV 2:SBJ 16:DEP 2:VC 3:OBJ 3:P 16:DEP 8:AMOD 16:DEP 8:P 8:COORD 10:P 10:CONJ 14:NMOD 12:COORD 14:P -1:ROOT')
    test_sentence_dict = {
        'value': 'Therefore we could show that "x>y" and "y<z.".',
        'id': '6e4c1420b2edaa374ff9d2300b8df31d',
        'is_title': False,
        'pos_list': "RB PRP MD VB IN ' CC JJR JJ ' CC ' NN JJR CD ' .",
        'tok_list': '0,9 10,12 13,18 19,23 24,28 29,30 30,31 31,32 32,33 33,34 35,38 39,40 40,41 41,42 42,44 44,45 45,46',
        'dep_tree': '2:ADV 2:SBJ 16:DEP 2:VC 3:OBJ 3:P 16:DEP 8:AMOD 16:DEP 8:P 8:COORD 10:P 10:CONJ 14:NMOD 12:COORD 14:P -1:ROOT',
        'polarity': 0.0,
    }

    def test_sentence_from_json(self):
        '''
        Tests that sentences can successfully be created from JSON.
        '''
        new_sentence = JSON10ParserSentence.from_json_string(
            json.dumps(self.test_sentence_dict))
        assert new_sentence.as_dict() == self.test_sentence.as_dict()


if __name__ == '__main__':
    unittest.main()
