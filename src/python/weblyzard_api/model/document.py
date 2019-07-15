#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 25, 2018

.. codeauthor: Max Goebel <goebel@weblyzard.com>
'''
from __future__ import unicode_literals
from past.builtins import basestring
from builtins import object
import json

from datetime import datetime

from weblyzard_api.model.parsers.xml_2013 import XML2013
from weblyzard_api.model import Sentence, SpanFactory
from weblyzard_api.model.parsers.xml_2005 import XML2005
from weblyzard_api.model.parsers.xml_deprecated import XMLDeprecated
from weblyzard_api.model.exceptions import (MissingFieldException,
                                            UnexpectedFieldException)


class Document(object):
    # supported partition keys
    SENTENCE_KEY = u'SENTENCE'
    TITLE_KEY = u'TITLE'
    TOKEN_KEY = u'TOKEN'

    # mapping from document attributes to serialized JSON fields
    MAPPING = {"content_id": "id",
               "md5sum": "id",
               "span_type": "@type",
               "header": "header",
               "content_type": "format",
               "sem_orient": "semOrient"}

    # list of required attributes
    REQUIRED_FIELDS = ['id', 'format', 'lang',
                       'nilsimsa', 'content']

    # list of optional attributes
    OPTIONAL_FIELDS = ['partitions', 'annotations', 'encoding',
                       'features', 'relations', 'header']

    SUPPORTED_XML_VERSIONS = {XML2005.VERSION: XML2005,
                              XML2013.VERSION: XML2013,
                              XMLDeprecated.VERSION: XMLDeprecated}

    def __init__(self, content_id, content, content_type, lang, nilsimsa=None,
                 partitions=None, header=None, annotations=None):
        ''' '''
        self.content_id = content_id
        self.content = content
        self.content_type = content_type
        self.lang = lang.lower() if lang else lang
        self.nilsimsa = nilsimsa

        # five dictionaries
        self.partitions = partitions if partitions else {}
        self.header = header if header else {}
        self.annotations = annotations if annotations else []

    def get_title(self):
        if self.content is None or len(self.content) == 0:
            return ''
        if self.TITLE_KEY in self.partitions:
            title_spans = self.partitions[self.TITLE_KEY]
            titles = [self.content[span.start:span.end] for span in title_spans]
            return ' '.join(titles)
        return ''

    def set_title(self, title):
        """ """
        assert title in self.content
        start_index = self.content.index(title)
        end_index = start_index + len(title)
        self.partitions[self.TITLE_KEY] = [{
            "@type": "CharSpan",
            "start": start_index,
            "end": end_index
        }]

    title = property(get_title, set_title)

    def __repr__(self):
        return 'Document: {}'.format(self.__dict__)

    @classmethod
    def _dict_transform(cls, data, mapping=None):
        ''' 
        Recursively transform a document object to a JSON serializable dict, 
        with MAPPING applied as well as empty results removed.
        @param data, the data to be transformed to a dict
        @return a dictionary of a document, ready for JSON serialization
        '''
        if mapping is None:
            mapping = cls.MAPPING
        if data is None:
            return None
        if isinstance(data, basestring):
            return data
        if isinstance(data, int):
            return data
        if isinstance(data, float):
            return data
        if isinstance(data, int):
            return data
        if isinstance(data, bool):
            return data
        if isinstance(data, tuple):
            if len(data) == 1:
                return data[0]
            return data
        if isinstance(data, datetime):
            return data.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(data, list):
            result = []
            for item in data:
                result.append(cls._dict_transform(item, mapping=mapping))
            return result
        if isinstance(data, dict):
            result = {}
            for key, value in list(data.items()):
                key = mapping.get(key, key)
                if value is not None:
                    value = cls._dict_transform(value, mapping=mapping)
                    if value is not None:
                        result[key] = value
            #             if not len(result):
            #                 return None
            return result
        if isinstance(data, object):
            result = {}
            for key, value in list(data.__dict__.items()):
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
        ''' 
        Convert a JSON object into a content model.
        @param json_payload, the string representation of the JSON content model
        '''
        parsed_content = json.loads(json_payload, strict=False)
        return cls.from_dict(dict_=parsed_content)

    @classmethod
    def from_dict(cls, dict_):
        '''
        Convert a `dict` object corresponding to the JSON serialisation
        into a Document object.
        @param dict_, the `dict` representing the Document.
        '''
        # validation
        for required_field in cls.REQUIRED_FIELDS:
            if not required_field in dict_:
                raise MissingFieldException(required_field)

        for key in list(dict_.keys()):
            if not key in cls.REQUIRED_FIELDS + cls.OPTIONAL_FIELDS:
                raise UnexpectedFieldException(key)

        parsed_content = dict_

        # This is tricky ... the mapping cannot be easily inversed
        # making the md5sum to content_id conversion at the top level necessary
        inverse_mapping = {v: k for k,
                                    v in cls.MAPPING.items() if
                           k != 'content_id'}
        parsed_content = Document._dict_transform(
            dict_, mapping=inverse_mapping)
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

        return Document(content_id=int(parsed_content['content_id']),
                        content=parsed_content.get('content'),
                        nilsimsa=parsed_content.get('nilsimsa'),
                        lang=parsed_content.get('lang'),
                        content_type=parsed_content.get('content_type'),
                        partitions=partitions,
                        header=header,
                        annotations=annotations)

    def to_json(self):
        '''
        Serialize a document to JSON '''
        return json.dumps(self.to_dict())

    def to_dict(self):
        '''
        Create a dict representing the Document analogous to the JSON structure.
        '''
        result = self._dict_transform(self)
        return result

    def to_xml(self, ignore_title=False, xml_version=XML2013.VERSION):
        ''' 
        Serialize a document to XML.
        @param ignore_titles, if set, titles will not be serialized
        @param xml_version, the version of XML to be used (defaults to 2013)
        @return: the serialized XML
        '''
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
            sentences=self.get_sentences())

    def get_text_by_span(self, span):
        ''' 
        Return the textual content of a span. 
        @param span, the span to extract content for.
        '''
        return self.content[span.start:span.end]

    @classmethod
    def overlapping(cls, spanA, spanB):
        ''' Return whether two spans overlap. '''
        return (spanB.start <= spanA.start and spanB.end >= spanA.end) or \
                (spanA.start <= spanB.start and spanA.end >= spanB.end)

    def get_partition_overlaps(self, search_span, target_partition_key):
        ''' Return all spans from a given target_partition_key that overlap 
        the search span. 
        @param search_span, the span to search for overlaps by.
        @param target_partition_key, the target partition'''
        result = []

        if not target_partition_key in self.partitions:
            return result

        for other_span in self.partitions[target_partition_key]:
            if self.overlapping(other_span, search_span):
                result.append(other_span)

        return result

    def get_pos_for_annotation(self, annotation):
        """
        Get the part-of-speech for a given annotation.
        :param annotation
        :return: the POS of the annotation
        """
        for token_span in self.partitions[self.TOKEN_KEY]:
            if token_span.start >= annotation['start']:
                return token_span.pos
        return None

    def get_sentences(self, zero_based=False):
        """
        Legacy method to extract webLyzard sentences from content model.
        :param zero_based: if True, enforce token indices starting at 0
        """
        result = []
        offset = 0
        if not self.SENTENCE_KEY in self.partitions:
            return result
        for sentence_span in self.partitions[self.SENTENCE_KEY]:
            if zero_based:
                offset = sentence_span.start
            if not sentence_span.span_type == 'SentenceCharSpan':
                raise Exception('Bad sentence span')

            # get tokens
            token_spans = self.get_partition_overlaps(search_span=sentence_span,
                                                      target_partition_key=self.TOKEN_KEY)
            is_title = len(
                self.get_partition_overlaps(search_span=sentence_span,
                                            target_partition_key=self.TITLE_KEY)) > 0

            # serialize POS, tokens, and dependecy to string
            pos_sequence = ' '.join([ts.pos for ts in token_spans])
            tok_sequence = ' '.join(
                ['{},{}'.format(ts.start - offset, ts.end - offset) for ts in
                 token_spans])
            try:
                dep_sequence = ' '.join(
                    ['{}:{}'.format(*ts.dependency.values()) for ts in
                     token_spans])
            except AttributeError:
                dep_sequence = None

            # prefer semOrient over sem_orient, if both are annotated and non-zero
            sem_orient = None
            if getattr(sentence_span, 'semOrient', None):
                sem_orient = sentence_span.semOrient
            else:
                sem_orient = sentence_span.sem_orient

            # finally, extract the sentence text.
            value = self.get_text_by_span(sentence_span)

            result.append(Sentence(md5sum=sentence_span.md5sum,
                                   sem_orient=sem_orient,
                                   significance=sentence_span.significance,
                                   pos=pos_sequence, token=tok_sequence,
                                   value=value, is_title=is_title,
                                   dependency=dep_sequence))

        return result
