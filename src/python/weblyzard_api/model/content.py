#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on May 11, 2023

.. codeauthor:: Max Göbel <goebel@weblyzard.com>
"""
from typing import Optional, List
from pydantic.main import BaseModel
from itertools import chain

from weblyzard_api.model.partition import (PartitionDict, AnnotationDict,
                                           PartitionKey)
from weblyzard_api.model import CharSpan, SpanFactory, Sentence


class ContentModel(BaseModel):

    text: str
    language: Optional[str]
    partitions: Optional[PartitionDict] = {}
    annotations: Optional[AnnotationDict] = {}
    nilsimsa: Optional[str]

    def text_content(self, sentences: bool=False, fragments: bool=False) -> str:
        """
        :param sentences:
        :param fragments:
        """
        if not sentences and not fragments:
            return self.text

        item_dict = {}

        if sentences:
            for sent in self.partitions.get(PartitionKey.SENTENCE, []):
                item_dict[sent['start']] = self.text[sent['start']:sent['end']]
        if fragments:
            for frag in self.partitions.get(PartitionKey.FRAGMENT, []):
                item_dict[frag['start']] = self.text[frag['start']:frag['end']]
        item_dict = {k: v for k, v in sorted(item_dict.items(),
                                             key=lambda item: item[0])}
        return '\n'.join(item_dict.values())

    def get_text_by_span(self, span: CharSpan):
        """ 
        Return the textual content of a span. 
        :param span, the span to extract content for.
        """
        if not isinstance(span, CharSpan):
            span = SpanFactory.new_span(span)
        return self.text[span.start:span.end]

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
        if not any([key.value in self.partitions.keys() for key in requested_keys]):
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
            token_spans = self.partitions.get_overlaps(
                                        search_span=sentence_span,
                                        target_partition_key=PartitionKey.TOKEN)
            is_title = len(
                self.partitions.get_overlaps(search_span=sentence_span,
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

    def get_body(self):
        if self.text is None or len(self.text) == 0:
            return ''
        if PartitionKey.BODY in self.partitions:
            body_spans = self.partitions[PartitionKey.BODY]
            spans = [self.text[span.start:span.end] for span in body_spans]
            return ' '.join(spans)
        return ''

    def get_title(self):
        if self.text is None or len(self.text) == 0:
            return ''
        if PartitionKey.TITLE in self.partitions:
            title_spans = self.partitions[PartitionKey.TITLE]
            titles = [self.text[span.start:span.end] for span in title_spans]
            return ' '.join(titles)
        return ''

    def set_title(self, title):
        """ """
        assert title in self.text
        start_index = self.text.index(title)
        end_index = start_index + len(title)
        self.partitions[PartitionKey.TITLE] = [{
            "@type": "CharSpan",
            "start": start_index,
            "end": end_index
        }]

    title = property(get_title, set_title)

