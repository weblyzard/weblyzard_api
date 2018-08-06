#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 25, 2018

.. codeauthor: Max Goebel <goebel@weblyzard.com>
'''
import json

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
               "metadata": "header",
               "content_type": "format"}

    # list of required attributes
    REQUIRED_FIELDS = ['id', 'format', 'lang',
                       'nilsimsa', 'content']

    # list of optional attributes
    OPTIONAL_FIELDS = ['partitions', 'annotations',
                       'features', 'relations', 'header', 'url']

    SUPPORTED_XML_VERSIONS = {XML2005.VERSION: XML2005,
                              XML2013.VERSION: XML2013,
                              XMLDeprecated.VERSION: XMLDeprecated}

    def __init__(self, content_id, content, content_type, lang, url=None, nilsimsa=None,
                 partitions=None, metadata=None, annotations=None, features=None,
                 relations=None):
        ''' '''
        self.content_id = content_id
        self.content = content
        self.content_type = content_type,
        self.lang = lang,
        self.url = url
        self.nilsimsa = nilsimsa
        self.partitions = partitions if partitions else {}
        self.metadata = metadata if metadata else {}
        self.annotations = annotations if annotations else {}
        self.features = features if features else {}
        self.relations = relations if relations else {}

    @classmethod
    def _dict_transform(cls, data):
        ''' 
        Recursively transform a document object to a JSON serializable dict, 
        with MAPPING applied as well as empty results removed.
        @param data, the data to be transformed to a dict
        @return a dictionary of a document, ready for JSON serialization
        '''
        if data is None:
            return None
        if isinstance(data, basestring):
            return data
        if isinstance(data, int):
            return data
        if isinstance(data, float):
            return data
        if isinstance(data, bool):
            return data
        if isinstance(data, tuple):
            if len(data) == 1:
                return data[0]
            return data
        if isinstance(data, list):
            result = []
            for item in data:
                result.append(cls._dict_transform(item))
            return result
        if isinstance(data, dict):
            result = {}
            for key, value in data.iteritems():
                if value is not None:
                    value = cls._dict_transform(value)
                    if value is not None:
                        result[key] = value

            if not len(result):
                return None
            return result
        if isinstance(data, object):
            result = {}
            for key, value in data.__dict__.iteritems():
                if key in cls.MAPPING:
                    key = cls.MAPPING[key]
                elif key.startswith('_'):
                    continue
                if value is not None:
                    value = cls._dict_transform(value)
                    if value is not None:
                        result[key] = cls._dict_transform(value)
            return result
        return None

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

        # populate default dicts:
        partitions = {label: [SpanFactory.new_span(span) for span in spans]
                      for label, spans in parsed_content['partitions'].iteritems()} \
            if 'partitions' in parsed_content else {}

        metadata = parsed_content['header'] \
            if 'header' in parsed_content else {}

        if not len(metadata):
            metadata = parsed_content['metadata'] \
                if 'metadata' in parsed_content else {}

        annotations = parsed_content['annotations'] \
            if 'annotations' in parsed_content else {}

        relations = parsed_content['relations'] \
            if 'relations' in parsed_content else {}

        features = parsed_content['features'] \
            if 'features' in parsed_content else {}

        return Document(content_id=parsed_content['id'],
                        url=parsed_content.get('url'),
                        content=parsed_content.get('content'),
                        nilsimsa=parsed_content.get('nilsimsa'),
                        lang=parsed_content.get('lang'),
                        content_type=parsed_content.get('format'),
                        partitions=partitions,
                        metadata=metadata,
                        annotations=annotations,
                        features=features,
                        relations=relations)

    def to_json(self):
        ''' 
        Serialize a document to JSON '''
        dict_object = self._dict_transform(self)
        return json.dumps(dict_object)

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

        titles = self.titles
        if ignore_title:
            titles = []

        return self.SUPPORTED_XML_VERSIONS[xml_version].dump_xml(
            titles=titles,
            attributes=self.attributes,
            sentences=self.sentences,
            annotations=self.annotations,
            features=self.features,
            relations=self.relations)

    def get_text_by_span(self, span):
        ''' 
        Return the textual content of a span. 
        @param span, the span to extract content for.
        '''
        return self.content[span.start:span.end]

    @classmethod
    def overlapping(cls, spanA, spanB):
        ''' Return whether two spans overlap. '''
        return spanB.start <= spanA.start and spanB.end >= spanA.end

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

    def get_sentences(self):
        ''' Legacy method to extract webLyzard sentences from content model.'''
        result = []

        if not self.SENTENCE_KEY in self.partitions:
            return result

        for sentence_span in self.partitions[self.SENTENCE_KEY]:
            if not sentence_span.span_type == 'SentenceCharSpan':
                raise Exception('Bad sentence span')

            # get tokens
            token_spans = self.get_partition_overlaps(search_span=sentence_span,
                                                      target_partition_key=self.TOKEN_KEY)
            is_title = len(self.get_partition_overlaps(search_span=sentence_span,
                                                       target_partition_key=self.TITLE_KEY)) > 0
            pos_sequence = ' '.join([ts.pos for ts in token_spans])
            tok_sequence = ' '.join(
                ['{},{}'.format(ts.start, ts.end) for ts in token_spans])
            value = self.get_text_by_span(sentence_span)
            result.append(Sentence(md5sum=sentence_span.md5sum,
                                   sem_orient=sentence_span.sem_orient,
                                   significance=sentence_span.significance,
                                   pos=pos_sequence, token=tok_sequence,
                                   value=value, is_title=is_title))

        return result
