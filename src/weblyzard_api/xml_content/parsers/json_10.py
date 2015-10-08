# -*- coding: utf-8 -*-

'''
This module contains code to create XMLContent objects from the Weblyzard API
JSON format.

    .. moduleauthor:: Fabian Fischer fabian.fischer@modul.ac.at
'''

import json
import pytest

from weblyzard_api.xml_content import Sentence, XMLContent


class MissingFieldException(Exception):
    '''
    Exception class thrown if a JSON document misses required fields.
    '''
    pass


class UnexpectedFieldException(Exception):
    '''
    Exception class thrown if a JSON document contains an unexpected field.
    '''
    pass

class MalformedJSONException(Exception):
    '''
    Exception to throw if the json.loads function fails.
    '''
    pass


class JSONParserBase(object):
    '''
    JSON Parser base class.
    '''
    #:  Override this constant in the subclasses based on requirements.
    FIELDS_REQUIRED = []
    #:  Override this constant in the subclasses based on requirements.
    FIELDS_OPTIONAL = []
    #:  Override this constant in the subclasses based on requirements.
    API_VERSION = None

    @classmethod
    def from_json_string(cls, json_string):
        '''
        Parses a JSON string.

        :param json_string: The JSON to parse
        :type json_string: str
        :returns: The parsed object.
        :rtype: :py:class:`weblyzard_api.xml_content.XMLContent` or \
            :py:class:`wl_core.document.Document` or \
            :py:class:`weblyzard_api.xml_content.Sentence` or\
            dict.
        '''
        try:
            api_dict = json.loads(json_string)
        except Exception:
            raise MalformedJSONException('JSON could not be parsed. Maybe not correct JSON?')
        return cls.from_api_dict(api_dict)

    @classmethod
    def from_api_dict(cls, api_dict):
        raise NotImplementedError
    
    @classmethod
    def _missing_fields(cls, api_dict):
        '''
        Checks if the given API dict misses a required field.

        :param api_dict: The document to check as dict.
        :type api_dict: dict
        :returns: The list of missing fields, None if all present.
        :rtype: list
        '''
        missing_fields = []
        for key in cls.FIELDS_REQUIRED:
            if key in api_dict:
                # check if the fields contain non-null values
                if api_dict[key] is None or api_dict[key] == '':
                    missing_fields.append(key)
            else:
                missing_fields.append(key)
        if len(missing_fields) > 0:
            return missing_fields
        else:
            return None

    @classmethod
    def _unexpected_fields(cls, api_dict):
        '''
        Checks if the given API dict contains an unexpected field.

        :param api_dict: The document to check as dict.
        :type api_dict: dict
        :returns: The list of unexpected fields, None if all accepted.
        :rtype: list
        '''
        allowed_fields = cls.FIELDS_REQUIRED + cls.FIELDS_OPTIONAL
        unexpected_fields = []
        for key in api_dict:
            if key not in allowed_fields:
                unexpected_fields.append(key)
        if len(unexpected_fields) > 0:
            return unexpected_fields
        else:
            return None

    @classmethod
    def _check_document_format(cls, api_dict, strict=True):
        '''
        Checks if the api_dict has all required fields and if there
        are unexpected and unallowed keys. 

        :param api_dict: The dict to check.
        :type api_dict: dict
        :param strict: If set to true, an UnexpectedFieldException is raised \
                if an unexpected key is contained in the dict.
        :type strict: bool
        '''
        missing_fields = cls._missing_fields(api_dict)
        if missing_fields is not None:
            raise MissingFieldException("Missing document-level field(s) %s" % 
                    ', '.join(missing_fields))
        if strict:
            unexpected_fields = cls._unexpected_fields(api_dict)
            if unexpected_fields is not None:
                raise UnexpectedFieldException("Got unexpected field(s): %s" %
                        ', '.join(unexpected_fields))


class JSON10ParserXMLContent(JSONParserBase):
    '''
    This class is the parser class for JSON documents conforming to
    the Weblyzard API 1.0 definition.
    '''
    FIELDS_REQUIRED = []
    FIELDS_OPTIONAL = ['title', 'language_id', 'sentences']
    API_VERSION = 1.0


    @classmethod
    def from_api_dict(cls, api_dict):
        '''
        Parses a dict with a structure analoguous to the JSON format defined
        in the API specification.

        :param api_dict: The document to parse.
        :type api_dict: dict
        :returns: The parsed document as XMLContent object.
        :rtype: :py:class:`weblyzard_api.xml_content.XMLContent`
        '''
        cls._check_document_format(api_dict)
        # This basically creates an empty XMLContent object
        xml_content = XMLContent(xml_content=None, remove_duplicates=True)
        # add all items in api_dict unless they need special handling
        xml_content.update_attributes({key:value for key, value in api_dict.iteritems() if 
                                       key not in ('sentences', 'annotations', 'language_id')})
        sentences = [JSON10ParserSentence.from_api_dict(sentence_dict) for 
                     sentence_dict in api_dict.get('sentences', [])]
        annotations = [JSON10ParserAnnotation.from_api_dict(annotation_dict) for 
                       annotation_dict in api_dict.get('annotations', [])]
        xml_content.sentences = sentences
        xml_content.attributes['annotations'] = annotations
        # map the language_id to XMLContent.lang
        if 'language_id' in api_dict:
            xml_content.attributes['lang'] = api_dict['language_id']
        if 'title' in api_dict:
            xml_content.titles = [Sentence(value=api_dict['title'], is_title=True), ]
        return xml_content


class JSON10ParserSentence(JSONParserBase):
    '''
    This class is the parser class for JSON sentences conforming to
    the Weblyzard API 1.0 definition.
    '''
    FIELDS_REQUIRED = ['id', 'value']
    FIELDS_OPTIONAL = ['is_title', 'pos_list', 'tok_list', 'dep_tree',
                       'sentence_number', 'paragraph_number', 'polarity']
    API_VERSION = 1.0

    @classmethod
    def from_api_dict(cls, api_dict):
        '''
        Parses a dict with a structure analoguous to the JSON format defined
        in the API specification.

        :param api_dict: The document to parse.
        :type api_dict: dict
        :returns: The parsed document as XMLContent object.
        :rtype: :py:class:`weblyzard_api.xml_content.Sentence`
        '''
        cls._check_document_format(api_dict)
        sentence = Sentence(
            md5sum=api_dict['id'],
            value=api_dict['value'],
            pos=api_dict.get('pos_list', None),
            sem_orient=api_dict.get('polarity', None),
            significance=None,
            token=api_dict.get('tok_list', None),
            is_title=api_dict.get('is_title', False),
            dependency=api_dict.get('dep_tree', None))
        return sentence


class JSON10ParserAnnotation(JSONParserBase):
    '''
    This class is the parser class for JSON annotations conforming to
    the Weblyzard API 1.0 definition.
    '''
    FIELDS_REQUIRED = ['start', 'end', 'surface_form']
    FIELDS_OPTIONAL = ['key', 'sentence', 'displayName', 'annotationType',
                       'polarity', 'properties']
    API_VERSION = 1.0

    @classmethod
    def from_api_dict(cls, api_dict):
        '''
        Parses a dict with a structure analoguous to the JSON annotation 
        format defined in the API specification.

        For now, it just checks the dict and returns it, if it validates.

        :param api_dict: The document to parse.
        :type api_dict: dict
        :returns: The parsed annotation as dict
        :rtype: dict
        '''
        cls._check_document_format(api_dict)
        return api_dict


class TestJSON10ParserXMLContent(object):
    '''
    Tests for the JSON_10_Parser class.
    '''
    test_xmlcontent_minimal_dict = {
            }
    test_xmlcontent_maximal_dict = {
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
        <wl:page xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://www.weblyzard.com/wl/2013#" wl:id="99933" dc:format="text/html" xml:lang="en" wl:nilsimsa="c3f00c9bae798a55a013209ceba9012f4d2349f7c1b2486529674a05ef7be8fb" dc:related="http://www.heise.de http://www.kurier.at">
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
        # TODO other keys have no obvious direct equivalent in XMLContent

    def test_document_to_json(self):
        '''
        Tests for the correct serialization as JSON of a XMLContent
        object.
        '''
        assert self.test_xmlcontent_minimal_dict == json.loads(
                JSON10ParserXMLContent.from_json_string(
                    json.dumps(self.test_xmlcontent_minimal_dict)
                ).to_json(version=1.0))
        assert self.test_xmlcontent_maximal_dict == json.loads(
                JSON10ParserXMLContent.from_json_string(
                    json.dumps(self.test_xmlcontent_maximal_dict)
                ).to_json(version=1.0))

    def test_document_xml_json_xml(self):
        '''
        Test that takes an XML string, creates a XMLContent object,
        serializes as JSON, creates an XMLContent object again and
        serializes back to XML string.
        '''
        xml_content = XMLContent(self.xml_content_string)
        json_string = xml_content.to_json(version=1.0)
        xml_content = JSON10ParserXMLContent.from_json_string(json_string)
        assert self.xml_content_string == xml_content.get_xml_document()


class TestJSON10ParserSentence(object):
    test_sentence = Sentence(
            md5sum=u'6e4c1420b2edaa374ff9d2300b8df31d',
            pos=u"RB PRP MD VB IN ' CC JJR JJ ' CC ' NN JJR CD ' .",
            sem_orient=0.0,
            significance=None,
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
