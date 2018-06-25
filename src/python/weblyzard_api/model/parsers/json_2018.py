#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 25, 2018

.. codeauthor: Max Goebel <goebel@weblyzard.com>
'''
import json

from weblyzard_api.model.parsers import JSONParserBase
from weblyzard_api.model import Partition, SpanFactory
from weblyzard_api.model.exceptions import (MissingFieldException,
                                            UnexpectedFieldException)
from weblyzard_api.model.document import Document


class JSON2018Parser(JSONParserBase):

    MAPPING = {"content_id": "id", "metadata": "header"}

    REQUIRED_FIELDS = ['id', 'format', 'lang',
                       'nilsimsa', 'content']

    OPTIONAL_FIELDS = ['partitions', 'annotations',
                       'features', 'relations', 'header', 'url']

    @classmethod
    def from_json(cls, json_payload):
        ''' 
        Convert a JSON object into a content model.
        @param json_payload, the string representation of the JSON content model
        '''
        parsed_content = json.loads(json_payload, strict=False)

        # validation
        for required_field in cls.REQUIRED_FIELDS:
            if not required_field in parsed_content:
                raise MissingFieldException()

        for key in parsed_content.iterkeys():
            if not key in cls.REQUIRED_FIELDS + cls.OPTIONAL_FIELDS:
                raise UnexpectedFieldException()

        # process optional dicts:
        partitions = {}
        if 'partitions' in parsed_content:
            partitions = {label: Partition(label=label,
                                           spans=[SpanFactory.new_span(span) for span in spans])
                          for label, spans in parsed_content['partitions'].iteritems()}

        header = {}
        if 'header' in parsed_content:
            header = parsed_content['header']

        annotations = {}
        if 'annotations' in parsed_content:
            annotations = parsed_content['annotations']

        relations = {}
        if 'relations' in parsed_content:
            relations = parsed_content['relations']

        features = {}
        if 'features' in parsed_content:
            features = parsed_content['features']

        url = None
        if 'url' in parsed_content:
            url = parsed_content['url']
        return Document(content_id=parsed_content['id'], url=url,
                        content=parsed_content['content'],
                        nilsimsa=parsed_content['nilsimsa'],
                        lang=parsed_content['lang'],
                        content_type=parsed_content['format'],
                        partitions=partitions,
                        metadata=header, annotations=annotations,
                        features=features, relations=relations)
