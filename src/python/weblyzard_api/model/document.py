#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 25, 2018

.. codeauthor: Max Goebel <goebel@weblyzard.com>
'''
from __future__ import unicode_literals
from builtins import object
import json
import html

from datetime import datetime
from decimal import Decimal
from itertools import chain

from weblyzard_api.model.parsers.xml_2013 import XML2013
from weblyzard_api.model import Sentence, SpanFactory, CharSpan
from weblyzard_api.model.parsers.xml_2005 import XML2005
from weblyzard_api.model.parsers.xml_deprecated import XMLDeprecated
from weblyzard_api.model.exceptions import (MissingFieldException,
                                            UnexpectedFieldException)
from typing import Dict


class Document(object):
    # supported partition keys
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

    def __init__(self, content_id, content, content_type, lang, nilsimsa=None,
                 partitions=None, header=None, annotations=None):
        ''' '''
        self.content_id = content_id

        # unescape existing HTML entities
        try:
            content = html.unescape(content)
        except Exception as e:
            pass  # ignore

        self.content = content
        self.content_type = content_type
        self.lang = lang.lower() if lang else lang
        self.nilsimsa = nilsimsa

        # populate default dicts:
        if partitions is None:
            self.partitions = {}
        else:
            self.partitions = {label: [SpanFactory.new_span(span) for span in spans]
                                for label, spans in partitions.items()}
        self.header = header if header else {}
        self.annotations = annotations if annotations else []

    def get_body(self):
        if self.content is None or len(self.content) == 0:
            return ''
        if self.BODY_KEY in self.partitions:
            body_spans = self.partitions[self.BODY_KEY]
            spans = [self.content[span.start:span.end] for span in body_spans]
            return ' '.join(spans)
        return ''

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
        :param data, the data to be transformed to a dict
        :return a dictionary of a document, ready for JSON serialization
        '''
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
        ''' 
        Convert a JSON object into a content model.
        :param json_payload, the string representation of the JSON content model
        '''
        parsed_content = json.loads(json_payload, strict=False)
        return cls.from_dict(dict_=parsed_content)

    @classmethod
    def from_dict(cls, dict_):
        '''
        Convert a `dict` object corresponding to the JSON serialisation
        into a Document object.
        :param dict_, the `dict` representing the Document.
        '''
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
        '''
        Serialize a document to JSON '''
        return json.dumps(self.to_dict())

    def to_dict(self):
        '''
        Create a dict representing the Document analogous to the JSON structure.
        '''
        result = self._dict_transform(self)
        return result

    def to_xml(self, ignore_title=False, include_fragments=False,
               xml_version=XML2013.VERSION):
        ''' 
        Serialize a document to XML.
        :param ignore_titles: if set, titles will not be serialized.
        :param include_fragments: non-sentence fragments will be included.
        :param xml_version: the version of XML to be used (defaults to 2013)
        :return: the serialized XML
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
            sentences=self.get_sentences(include_fragments=include_fragments))

    def get_text_by_span(self, span: CharSpan):
        ''' 
        Return the textual content of a span. 
        :param span, the span to extract content for.
        '''
        if not isinstance(span, CharSpan):
            span = SpanFactory.new_span(span)
        return self.content[span.start:span.end]

    @classmethod
    def overlapping(cls, spanA: CharSpan, spanB: CharSpan):
        ''' Return whether two spans overlap. '''
        return (spanB.start <= spanA.start and spanB.end > spanA.start) or \
                (spanA.start <= spanB.start and spanA.end > spanB.start)

    def get_partition_overlaps(self, search_span: CharSpan,
                               target_partition_key: str):
        ''' Return all spans from a given target_partition_key that overlap 
        the search span. 
        :param search_span, the span to search for overlaps by.
        :param target_partition_key, the target partition'''
        result = []

        if not target_partition_key in self.partitions:
            return result

        for other_span in self.partitions[target_partition_key]:
            if not isinstance(other_span, CharSpan):
                other_span = SpanFactory.new_span(other_span)
            if not isinstance(search_span, CharSpan):
                search_span = SpanFactory.new_span(search_span)
            if self.overlapping(other_span, search_span):
                result.append(other_span)

        return result

    def get_pos_for_annotation(self, annotation: Dict):
        """
        Get the part-of-speech for a given annotation.
        :param annotation
        :return: the POS of the annotation
        """
        for token_span in self.partitions[self.TOKEN_KEY]:
            if not isinstance(token_span, CharSpan):
                token_span = SpanFactory.new_span(token_span)
            if token_span.start >= annotation['start']:
                return token_span.pos
        return None

    def get_sentences(self, zero_based: bool=False,
                      include_title: bool=True,
                      include_fragments: bool=False):
        """
        Legacy method to extract webLyzard sentences from content model.
        :param zero_based: if True, enforce token indices starting at 0
        :param include_title: if True, include title sentences
        :param include_fragments: if True, include fragments (non-sentence text)
        """
        result = []
        offset = 0
        requested_keys = [self.SENTENCE_KEY]

        if include_fragments:
            requested_keys.append(self.FRAGMENT_KEY)
        if not any([key in self.partitions for key in requested_keys]):
            return result
        sentence_spans = chain(
            *(self.partitions.get(key, []) for key in requested_keys)
        )
        sentence_spans = sorted(sentence_spans, key=lambda span: span.start)

        for sentence_span in sentence_spans:
            if not isinstance(sentence_span, CharSpan):
                sentence_span = SpanFactory.new_span(sentence_span)

            if zero_based:
                offset = sentence_span.start
            if not sentence_span.span_type == 'SentenceCharSpan':
                raise Exception('Bad sentence span')

            # get tokens
            token_spans = self.get_partition_overlaps(
                                            search_span=sentence_span,
                                            target_partition_key=self.TOKEN_KEY)
            is_title = len(
                self.get_partition_overlaps(search_span=sentence_span,
                                            target_partition_key=self.TITLE_KEY)) > 0
            if not include_title and is_title:
                continue

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
            sem_orient = sentence_span.sem_orient

            # finally, extract the sentence text.
            value = self.get_text_by_span(sentence_span)

            result.append(Sentence(md5sum=sentence_span.md5sum,
                                   sem_orient=sem_orient,
                                   significance=sentence_span.significance,
                                   pos=pos_sequence, token=tok_sequence,
                                   value=value, is_title=is_title,
                                   dependency=dep_sequence,
                                   emotions=sentence_span.emotions))

        return result
