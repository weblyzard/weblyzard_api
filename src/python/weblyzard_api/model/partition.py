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


class PartitionDict(dict):

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        if len(args):
            for label, spans in args[0].items():
                self[label] = [SpanFactory.new_span(span) for span in spans]

    def __setitem__(self, k, v):
        if PartitionKey.is_valid(k):
            super().__setitem__(PartitionKey(k), v)
        else:
            raise KeyError(f"Partition {k} is not valid")

    def __getitem__(self, k):
        if isinstance(k, str):
            k = PartitionKey(k.upper())
        return super().__getitem__(k)

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

    def get_sentences(self, zero_based: bool=False,
                      include_title: bool=True,
                      include_fragments: bool=False) -> List[Sentence]:
        """
        Legacy method to extract webLyzard sentences from content model.
        :param zero_based: if True, enforce token indices starting at 0
        :param include_title: if True, include title sentences
        :param include_fragments: if True, include fragments (non-sentence text)
        """
        result = []
        offset = 0
        requested_keys = [PartitionKey.SENTENCE]

        if include_fragments:
            requested_keys.append(PartitionKey.FRAGMENT)
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
            token_spans = self.get_overlaps(
                                        search_span=sentence_span,
                                        target_partition_key=PartitionKey.TOKEN)
            is_title = len(
                self.get_overlaps(search_span=sentence_span,
                                  target_partition_key=PartitionKey.TITLE)) > 0
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
