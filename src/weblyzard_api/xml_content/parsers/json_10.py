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
        raise NotImplementedError

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
    def _check_document_format(cls, api_dict):
        missing_fields = cls._missing_fields(api_dict)
        if missing_fields is not None:
            raise MissingFieldException("Missing document-level field(s) %s" % 
                    ', '.join(missing_fields))
        #  TODO maybe raising an exception is too strict?
        unexpected_fields = cls._unexpected_fields(api_dict)
        if unexpected_fields is not None:
            raise UnexpectedFieldException("Got unexpected field(s): %s" %
                    ', '.join(unexpected_fields))


class JSON10ParserDocument(JSONParserBase):
    '''
    This class is the parser class for JSON documents conforming to
    the Weblyzard API 1.0 definition.
    '''
    FIELDS_REQUIRED = ['repository_id', 'uri', 'title', 'content_type',
                       'content']
    FIELDS_OPTIONAL = ['language_id', 'sentences', 'annotations', 'meta_data']
    API_VERSION = 1.0

    @classmethod
    def from_json_string(cls, json_string):
        '''
        Parses a JSON string.

        :param json_string: The JSON to parse
        :type json_string: str
        :returns: The parsed XMLContent object.
        :rtype: :py:class:`weblyzard_api.xml_content.XMLContent`
        '''
        return cls.from_api_dict(json.loads(json_string))

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
        # map the language_id to XMLContent.lang
        if 'language_id' in api_dict:
            xml_content.attributes['lang'] = api_dict['language_id']
        # Since title is a required field, no check here
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
    def from_json_string(cls, json_string):
        '''
        Parses a JSON string.

        :param json_string: The JSON to parse
        :type json_string: str
        :returns: The parsed XMLContent object.
        :rtype: :py:class:`weblyzard_api.xml_content.Sentence`
        '''
        return cls.from_api_dict(json.loads(json_string))

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
    def from_json_string(cls, json_string):
        '''
        Parses a JSON string.

        :param json_string: The JSON to parse
        :type json_string: str
        :returns: The parsed XMLContent object.
        :rtype: :py:class:`weblyzard_api.xml_content.XMLContent`
        '''
        return cls.from_api_dict(json.loads(json_string))

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


class TestJSON10ParserDocument(object):
    '''
    Tests for the JSON_10_Parser class.
    '''
    test_xmlcontent_minimal_dict = {
            'repository_id': 'repository1',
            'uri': "the repository's uri",
            'title': 'document title',
            'content_type': 'text',
            'content': 'document content',
            }
    FIELDS_OPTIONAL = ['language_id', 'sentences', 'annotations', 'meta_data']
    test_xmlcontent_maximal_dict = {
            'repository_id': 'repository1',
            'uri': "the repository's uri",
            'title': 'document title',
            'content_type': 'text',
            'content': 'document content',
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
            #'annotations': [],
            'meta_data': {},
            }

    def test_unexpected_document_fields(self):
        '''
        Tests that the parser rejects documents with unexpected fields.
        '''
        testkey = 'testkey'
        assert testkey not in JSON10ParserDocument.FIELDS_REQUIRED
        assert testkey not in JSON10ParserDocument.FIELDS_OPTIONAL
        xmldict_ = dict(self.test_xmlcontent_minimal_dict)
        xmldict_[testkey] = 'random'
        with pytest.raises(UnexpectedFieldException):
            JSON10ParserDocument.from_json_string(
                json.dumps(xmldict_))

    def test_required_document_fields(self):
        '''
        Test for checking that all required document fields are present in the JSON.
        '''
        for key in self.test_xmlcontent_minimal_dict:
            xmldict_ = dict(self.test_xmlcontent_minimal_dict)
            del xmldict_[key]
            with pytest.raises(MissingFieldException):
                JSON10ParserDocument.from_json_string(json.dumps(xmldict_))
        assert JSON10ParserDocument.from_json_string(
                json.dumps(self.test_xmlcontent_minimal_dict)) is not None

    def test_minimal_xmlcontent_from_json(self):
        '''
        Tests for the correct conversion from a JSON string.
        '''
        xmlcontent = JSON10ParserDocument.from_json_string(
                json.dumps(self.test_xmlcontent_minimal_dict))
        assert xmlcontent.title == self.test_xmlcontent_minimal_dict['title']
        assert xmlcontent.content_type == self.test_xmlcontent_minimal_dict['content_type']
        # TODO other keys have no obvious direct equivalent in XMLContent

    def test_document_to_json(self):
        '''
        Tests for the correct serialization as JSON of a XMLContent
        object.
        '''
        assert self.test_xmlcontent_minimal_dict == json.loads(
                JSON10ParserDocument.from_json_string(
                    json.dumps(self.test_xmlcontent_minimal_dict)
                ).to_json(version=1.0))
        assert self.test_xmlcontent_maximal_dict == json.loads(
                JSON10ParserDocument.from_json_string(
                    json.dumps(self.test_xmlcontent_maximal_dict)
                ).to_json(version=1.0))


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
