#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on May 11, 2023

.. codeauthor:: Max Göbel <goebel@weblyzard.com>
"""
from itertools import chain
from typing import List
from enum import Enum

from weblyzard_api.model import Sentence, SpanFactory, CharSpan


class AnnotationKey(str, Enum):

    ORGANISATION = 'OranisationEntity'
    PERSON = 'PersonEntity'
    GEO = 'GeoEntity'


class PartitionKey(str, Enum):

    FRAGMENT = 'FRAGMENT'
    SENTENCE = 'SENTENCE'
    DUPLICATE = 'DUPLICATE'
    TITLE = 'TITLE'
    BODY = 'BODY'
    LINE = 'LINE'
    TOKEN = 'TOKEN'
    LAYOUT = 'LAYOUT'
    SENTIMENT = 'SENTIMENT_SCOPE'
    MISC = 'MISC'
    # NEGATION_KEY = u'NEGATION_SCOPE'
    MULTIPLIER = 'MULTIPLIER_SCOPE'

    @classmethod
    def is_valid(cls, partition_key: str):
        if isinstance(partition_key, cls):
            partition_key = partition_key.value
        if not partition_key.upper() in cls.list():
            return False
        else:
            return True

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class NamedDict(dict):

    NAME = 'Undefined'

    KEYSPACE = None

    def __setitem__(self, k, v):
        if self.KEYSPACE.is_valid(k):
            super().__setitem__(self.KEYSPACE(k), v)
        else:
            raise KeyError(f"{self.NAME} {k} is not valid")

    def __getitem__(self, k):
        if isinstance(k, str):
            k = self.KEYSPACE(k.upper())
        return super().__getitem__(k)


class AnnotationDict(NamedDict):

    Name = 'Annotation'

    KEYSPACE = AnnotationKey


class PartitionDict(NamedDict):

    NAME = 'Partition'

    KEYSPACE = PartitionKey

    def __init__(self, *args, **kwargs):
        NamedDict.__init__(self, *args, **kwargs)
        if len(args):
            for label, spans in args[0].items():
                self[label] = [SpanFactory.new_span(span) for span in spans]

    def partition_content(self, sentences: bool=False, fragments: bool=False) -> str:
        """ Return the textual content according to partitions only. 
        :param sentences:
        :param fragments:
        """
        if not sentences and not fragments:
            return self.text

        item_dict = {}

        if sentences:
            for sent in self.get(PartitionKey.SENTENCE, []):
                item_dict[sent['start']] = self.text[sent['start']:sent['end']]
        if fragments:
            for frag in self.get(PartitionKey.FRAGMENT, []):
                item_dict[frag['start']] = self.text[frag['start']:frag['end']]
        item_dict = {k: v for k, v in sorted(item_dict.items(),
                                             key=lambda item: item[0])}
        return '\n'.join(item_dict.values())

    @classmethod
    def overlapping(cls, spanA: CharSpan, spanB: CharSpan) -> bool:
        """ Return whether two spans overlap. """
        return (spanB.start <= spanA.start and spanB.end > spanA.start) or \
                (spanA.start <= spanB.start and spanA.end > spanB.start)

    def get_overlaps(self, search_span: CharSpan,
                               target_partition_key: str) -> List[CharSpan]:
        """ Return all spans from a given target_partition_key that overlap 
        the search span. 
        :param search_span, the span to search for overlaps by.
        :param target_partition_key, the target partition"""
        result = []

        if not target_partition_key in self:
            return result

        for other_span in self[target_partition_key]:
            if not isinstance(other_span, CharSpan):
                other_span = SpanFactory.new_span(other_span)
            if not isinstance(search_span, CharSpan):
                search_span = SpanFactory.new_span(search_span)
            if self.overlapping(other_span, search_span):
                result.append(other_span)

        return result

    def get_pos_for_annotation(self, start: int) -> str:
        """
        Get the part-of-speech for a given annotation.
        :param annotation
        :return: the POS of the annotation
        """
        for token_span in self.partitions.__getitem__(PartitionKey.TOKEN):
            if not isinstance(token_span, CharSpan):
                token_span = SpanFactory.new_span(token_span)
            if token_span.start == start:
                return token_span.pos
        return None

