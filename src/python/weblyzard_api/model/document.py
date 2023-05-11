#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Jan 25, 2018

.. codeauthor: Max Goebel <goebel@weblyzard.com>
"""
from __future__ import unicode_literals
from builtins import object
import json
import html

from datetime import datetime
from decimal import Decimal
from typing import Dict

from weblyzard_api.model.parsers.xml_2013 import XML2013
from weblyzard_api.model import SpanFactory, CharSpan
from weblyzard_api.model.parsers.xml_2005 import XML2005
from weblyzard_api.model.parsers.xml_deprecated import XMLDeprecated
from weblyzard_api.model.exceptions import (MissingFieldException,
                                            UnexpectedFieldException)
from weblyzard_api.model.partition import PartitionDict, AnnotationDict
from weblyzard_api.model.content import ContentModel


class Document(object):

    # TODO: to be removed, legacy mode only
    FRAGMENT_KEY = 'FRAGMENT'
    SENTENCE_KEY = u'SENTENCE'
    DUPLICATE_KEY = u'DUPLICATE'
    TITLE_KEY = u'TITLE'
    BODY_KEY = u'BODY'
    TOKEN_KEY = u'TOKEN'
    LAYOUT_KEY = u'LAYOUT'
    SENTIMENT_KEY = u'SENTIMENT_SCOPE'
    # NEGATION_KEY = u'NEGATION_SCOPE'
    MULTIPLIER_KEY = 'MULTIPLIER_SCOPE'

    # mapping from document attributes to serialized JSON fields
    MAPPING = {"content_id": "id",
               "md5sum": "id",
               "span_type": "@type",
               "header": "header",
               "content_type": "format",
               "sem_orient": "semOrient"}

    # list of required attributes
    REQUIRED_FIELDS = ['id', 'format', 'lang',
                       'content']

    # list of optional attributes
    OPTIONAL_FIELDS = ['partitions', 'annotations', 'encoding',
                       'features', 'relations', 'header', 'nilsimsa']

    SUPPORTED_XML_VERSIONS = {XML2005.VERSION: XML2005,
                              XML2013.VERSION: XML2013,
                              XMLDeprecated.VERSION: XMLDeprecated}

    def __init__(self, content_id: int, content: str, content_type: str,
                 lang: str, nilsimsa: str=None, partitions: Dict=None,
                 header: Dict=None, annotations: Dict=None):
        """ 
        :param content_id:
        :param content:
        :param content_type:
        :param lang:
        :param nilsimsa:
        :param partitions:
        :param header:
        :param annotations:
        """
        self.content_id = content_id

        # unescape existing HTML entities
        if isinstance(content, str):
            try:
                content = html.unescape(content)
            except Exception as e:
                pass  # ignore

        self.content_type = content_type

        #
        # self.lang = lang.lower() if lang else lang
        # self.nilsimsa = nilsimsa

        # populate default dicts:
        part_dict = PartitionDict()
        if partitions is not None:
            part_dict = PartitionDict(partitions)

        anno_dict = AnnotationDict()
        if annotations is not None:
            anno_dict = AnnotationDict(annotations)

        self.contentx = ContentModel(text=content,
                                     language=lang.lower() if lang else lang,
                                     nilsimsa=nilsimsa,
                                     partitions=part_dict,
                                     annotations=anno_dict)

        self.header = header if header else {}

    def __repr__(self):
        return 'Document: {}'.format(self.__dict__)

    @property
    def content(self):
        return self.contentx.text

    @property
    def lang(self):
        return self.contentx.language

    @lang.setter
    def lang(self, val: str):
        self.contentx.language = val

    @property
    def title(self):
        return self.contentx.get_title()

    @title.setter
    def title(self, val: str):
        self.contentx.set_title(val)

    @property
    def nilsimsa(self):
        return self.contentx.nilsimsa

    @nilsimsa.setter
    def nilsimsa(self, val: str):
        self.contentx.nilsimsa = val

    @property
    def partitions(self):
        return self.contentx.partitions

    @partitions.setter
    def partitions(self, val: Dict):
        if not isinstance(val, PartitionDict):
            val = PartitionDict(dict)

        self.contentx.partitions = val

    @property
    def annotations(self):
        return self.contentx.annotations

    @annotations.setter
    def annotations(self, val: Dict):
        if not isinstance(val, AnnotationDict):
            val = AnnotationDict(dict)

        self.contentx.annotations = val

    def get_body(self) -> str:
        return self.contentx.get_body()

    def get_title(self) -> str:
        return self.contentx.get_title()

    @classmethod
    def _dict_transform(cls, data, mapping=None):
        """ 
        Recursively transform a document object to a JSON serializable dict, 
        with MAPPING applied as well as empty results removed.
        :param data, the data to be transformed to a dict
        :return a dictionary of a document, ready for JSON serialization
        """
        if mapping is None:
            mapping = cls.MAPPING
        if data is None:
            return None
        if isinstance(data, str):
            return data
        if isinstance(data, int):
            return data
        if isinstance(data, float):
            return data
        if isinstance(data, int):
            return data
        if isinstance(data, bool):
            return data
        if isinstance(data, Decimal):
            return str(data)  # needed for e.g. GEO coordinates
        if isinstance(data, tuple):
            if len(data) == 1:
                return data[0]
            return data
        if isinstance(data, memoryview):
            data = bytes(data)
        if isinstance(data, bytes):
            return data.decode("utf-8")
        if isinstance(data, datetime):
            return data.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(data, list):
            result = []
            for item in data:
                result.append(cls._dict_transform(item, mapping=mapping))
            return result
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                key = mapping.get(key, key)
                if value is not None:
                    value = cls._dict_transform(value, mapping=mapping)
                    if value is not None:
                        result[key] = value
            return result

        if isinstance(data, object):
            result = {}
            for key, value in data.__dict__.items():
                if key in mapping:
                    key = mapping[key]
                elif key.startswith('_'):
                    continue

                if value is not None:
                    if key == 'lang':
                        value = value.upper()
                    value = cls._dict_transform(value, mapping=mapping)
                    if value is not None:
                        result[key] = cls._dict_transform(
                            value, mapping=mapping)
            return result
        return None

    @classmethod
    def from_json(cls, json_payload):
        """ 
        Convert a JSON object into a content model.
        :param json_payload, the string representation of the JSON content model
        """
        parsed_content = json.loads(json_payload, strict=False)
        return cls.from_dict(dict_=parsed_content)

    @classmethod
    def from_dict(cls, dict_):
        """
        Convert a `dict` object corresponding to the JSON serialisation
        into a Document object.
        :param dict_, the `dict` representing the Document.
        """
        # validation
        for required_field in cls.REQUIRED_FIELDS:
            if not required_field in dict_:
                raise MissingFieldException(required_field)

        for key in dict_.keys():
            if not key in cls.REQUIRED_FIELDS + cls.OPTIONAL_FIELDS:
                raise UnexpectedFieldException(key)

        # This is tricky ... the mapping cannot be easily inversed
        # making the md5sum to content_id conversion at the top level necessary
        inverse_mapping = {v: k for k, v in cls.MAPPING.items() if
                                                    k != 'content_id'}
        parsed_content = Document._dict_transform(dict_,
                                                  mapping=inverse_mapping)
        parsed_content['content_id'] = parsed_content.pop('md5sum')

        # populate default dicts:
        partitions = {label: [SpanFactory.new_span(span) for span in spans]
                      for label, spans in parsed_content['partitions'].items()} \
            if 'partitions' in parsed_content else {}

        header = parsed_content['header'] \
            if 'header' in parsed_content and parsed_content[
            'header'] is not None else {}

        if not len(header):
            header = parsed_content['header'] \
                if 'header' in parsed_content else {}

        annotations = parsed_content['annotations'] \
            if 'annotations' in parsed_content else {}

        return cls(content_id=int(parsed_content['content_id']),
                   content=parsed_content.get('content'),
                   nilsimsa=parsed_content.get('nilsimsa'),
                   lang=parsed_content.get('lang'),
                   content_type=parsed_content.get('content_type'),
                   partitions=partitions,
                   header=header,
                   annotations=annotations)

    def to_json(self):
        """
        Serialize a document to JSON """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """
        Create a dict representing the Document analogous to the JSON structure.
        """
        result = self._dict_transform(self)
        return result

    def to_xml(self, ignore_title=False, include_fragments=False,
               xml_version=XML2013.VERSION):
        """ 
        Serialize a document to XML.
        :param ignore_titles: if set, titles will not be serialized.
        :param include_fragments: non-sentence fragments will be included.
        :param xml_version: the version of XML to be used (defaults to 2013)
        :return: the serialized XML
        """
        if not hasattr(self, 'features'):
            self.features = {}

        if not hasattr(self, 'relations'):
            self.relations = {}

        if not hasattr(self, 'titles'):
            self.titles = []
        titles = self.titles
        if ignore_title:
            titles = []

        return self.SUPPORTED_XML_VERSIONS[xml_version].dump_xml(
            titles=titles,
            attributes=self.header,
            sentences=self.get_sentences(include_fragments=include_fragments))

