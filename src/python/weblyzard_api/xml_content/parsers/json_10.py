# -*- coding: utf-8 -*-

'''
This module contains code to create XMLContent objects from the Weblyzard API
JSON format.

    .. moduleauthor:: Fabian Fischer fabian.fischer@modul.ac.at
'''

import json

from weblyzard_api.xml_content import Sentence, XMLContent

class MissingContentException(Exception):
    '''
    Exception class thrown if a JSON document misses required fields.
    '''
    pass

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
    Exception to throw if the json.loads function fails or the JSON is
    otherwise ill formatted.
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
            raise MalformedJSONException('JSON could not be parsed')
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
            raise MissingFieldException("Missing field(s) %s" % 
                    ', '.join(missing_fields))
        if strict:
            unexpected_fields = cls._unexpected_fields(api_dict)
            if unexpected_fields is not None:
                raise UnexpectedFieldException("Got unexpected field(s): %s" %
                        ', '.join(unexpected_fields))

    @classmethod
    def _validate_document(cls, json_document):
        ''' '''
        if 'content' in json_document and 'content_type' not in json_document:
            raise MissingFieldException(
                    "When field 'content' is set, 'content_type' must be set, too.")
        elif 'content_type' in json_document and 'content' not in json_document:
            raise MissingFieldException(
                    "When field 'content_type' is set, 'content' must be set, too.")
        elif 'content' not in json_document and \
                'content_type' not in json_document and \
                'sentences' not in json_document:
            raise MissingFieldException(
                    "Either 'sentences' or 'content' and 'content_type' must be set.")
        if 'content' in json_document and 'sentences' in json_document:
            raise MalformedJSONException(
                    "If 'sentences' is set, 'content' must not be set.")
            
class JSON10ParserXMLContent(JSONParserBase):
    '''
    This class is the parser class for JSON documents conforming to
    the Weblyzard API 1.0 definition.
    '''
    FIELDS_REQUIRED = ['uri', 'title']
    FIELDS_OPTIONAL = ['language_id', 'sentences', 'content', 'features', 'relations']
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
        cls._check_document_format(api_dict, strict=True)
        # This basically creates an empty XMLContent object
        xml_content = XMLContent(xml_content=None, remove_duplicates=True)
        # add all items in api_dict unless they need special handling
        xml_content.update_attributes({key:value for key, value in api_dict.iteritems() if 
                                       key not in ('sentences', 'annotations', 
                                                   'language_id', 'features', 
                                                   'relations', 'content')})
        # parse sentences
        sentences = [JSON10ParserSentence.from_api_dict(sentence_dict) for 
                     sentence_dict in api_dict.get('sentences', [])]
        xml_content.sentences = sentences
        
        # parse annotations
        annotations = [JSON10ParserAnnotation.from_api_dict(annotation_dict) for 
                       annotation_dict in api_dict.get('annotations', [])]
        xml_content.body_annotations = annotations
        
        # add relations and features
        xml_content.relations = api_dict.get('relations', {})
        xml_content.features = api_dict.get('features', {})

        # map the language_id to XMLContent.lang
        if 'language_id' in api_dict:
            xml_content.attributes['lang'] = api_dict['language_id']
        # removed this: title is already set via attributes
        if 'title' in api_dict:
            for sentence in sentences:
                if sentence.is_title and sentence.value != api_dict['title']:
                    raise MalformedJSONException('The sentence marked with "is_title": "True" must '+
                                                 'match the "title" attribute.')
        else:
            for sentence in sentences:
                if sentence.is_title:
                    api_dict['title'] = sentence.value
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
            significance=0.0,
            token=api_dict.get('tok_list', None),
            is_title=api_dict.get('is_title', False),
            dependency=api_dict.get('dep_tree', None))
        return sentence

class JSON10ParserAnnotation(JSONParserBase):
    '''
    This class is the parser class for JSON annotations conforming to
    the Weblyzard API 1.0 definition.
    '''
    FIELDS_REQUIRED = ['start', 'end', 'surface_form', 'annotation_type']
    FIELDS_OPTIONAL = ['key', 'sentence', 'display_name', 'polarity', 'properties']
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
        result = dict(api_dict)
        del result['annotation_type']
        return result

    @classmethod
    def to_api_dict(cls, annotation_type, annotation):
        '''
        This method simply puts the annotation_type within
        the annotation dict again.

        :param annotation_type: The type of annotation
        :type annotation_type: str
        :param annotation: The annotation data
        :type annotation: dict
        :returns: the annotation with annotation_type set 
        :rtype: dict
        '''
        result = dict(annotation)
        result['annotation_type'] = annotation_type
        return result

    @classmethod
    def from_api_list(cls, api_list):
        '''
        Parses a list of annotations and returns a dict mapping the
        annotations to their annotation type. I.e. each annotation
        in the list individually states its type and in the output
        dict this type is the key and the value are the individual
        annotations of this type. E.g.

        >>> api_list = [{'start': 87, \
                         'end': 101, \
                         'surface_form': 'Public Service',\
                         'annotation_type': 'OrganizationEntity'}]
        >>> JSON10ParserAnnotation.from_api_list(api_list)
        {'OrganizationEntity': [{'start': 87, 'surface_form': 'Public Service', 'end': 101}]}

        :param api_list: A list of annotations.
        :type api_list: list
        :returns: a nested dict with the annotation types as key \
                and a list of annotations as the value.
        :rtype: dict
        '''
        result = {}
        for annotation in api_list:
            cls._check_document_format(annotation)
            result.setdefault(annotation['annotation_type'], [])
            result.setdefault(annotation['annotation_type'], []).append(
                              JSON10ParserAnnotation.from_api_dict(annotation))
        return result

    @classmethod
    def to_api_list(cls, annotations):
        '''
        Takes a dict that nests a list of annotations in their annotation_type
        and returns a flat list of annotations where each has its
        annotation_type set individually.

        >>> annotations = {'OrganizationEntity': [{'start': 87, 'surface_form': 'Public Service', 'end': 101}]}
        >>> JSON10ParserAnnotation.to_api_list(annotations)
        [{'start': 87, 'surface_form': 'Public Service', 'end': 101, 'annotation_type': 'OrganizationEntity'}]

        :param annotations: The nested dict mapping annotation_type to a list
        :type annotations: dict
        :returns: The flat list of annotations.
        :rtype: list
        '''
        result = []
        if not annotations:
            return result
        for annotation_type in annotations:
            for annotation in annotations[annotation_type]:
                result.append(JSON10ParserAnnotation.to_api_dict(annotation_type,
                                                                 annotation))
        return result