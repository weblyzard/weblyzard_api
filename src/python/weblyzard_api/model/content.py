#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on May 11, 2023

.. codeauthor:: Max Göbel <goebel@weblyzard.com>
"""
from typing import Optional
from pydantic.main import BaseModel

from weblyzard_api.model.partition import (PartitionDict, AnnotationDict,
                                           PartitionKey)


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

