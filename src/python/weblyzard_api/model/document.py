#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 25, 2018

.. codeauthor: Max Goebel <goebel@weblyzard.com>
'''
import json

from weblyzard_api.model.parsers.xml_2013 import XML2013
from weblyzard_api.model import Sentence, DictObject, dict_transform
from weblyzard_api.model.parsers.xml_2005 import XML2005
from weblyzard_api.model.parsers.xml_deprecated import XMLDeprecated


class Document(DictObject):

    # partition keys
    SENTENCE_KEY = u'SENTENCE'
    TITLE_KEY = u'TITLE'
    TOKEN_KEY = u'TOKEN'

    SUPPORTED_XML_VERSIONS = {XML2005.VERSION: XML2005,
                              XML2013.VERSION: XML2013,
                              XMLDeprecated.VERSION: XMLDeprecated}

    def __init__(self, content_id, content, content_type, lang, url=None, nilsimsa=None,
                 partitions={}, metadata={}, annotations={}, features={},
                 relations={}):
        ''' '''
        self.content_id = content_id
        self.content = content
        self.content_type = content_type,
        self.lang = lang,
        self.url = url
        self.nilsimsa = nilsimsa
        self.partitions = partitions
        self.metadata = metadata
        self.annotations = annotations
        self.features = features
        self.relations = relations

    def to_json(self):
        ''' 
        Serialize a document to JSON '''
        dict_object = dict_transform(self)
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

        for other_span in self.partitions[target_partition_key].spans:
            if self.overlapping(other_span, search_span):
                result.append(other_span)

        return result

    def get_sentences(self):
        ''' Legacy method to extract webLyzard sentences from content model.'''
        result = []

        if not self.SENTENCE_KEY in self.partitions:
            return result

        for sentence_span in self.partitions[self.SENTENCE_KEY].spans:
            if not sentence_span.type == 'SentenceCharSpan':
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
