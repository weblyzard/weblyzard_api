#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on September 11, 2019

@author: jakob <jakob.steixner@modul.ac.at>
'''

import unittest
import pytest

from weblyzard_api.model import SpanFactory, CharSpan, TokenCharSpan, \
    SentimentCharSpan, SentenceCharSpan, NegationCharSpan


class TestSpanFactory(unittest.TestCase):

    def test_new_span_token(self):
        """"""
        dict_token_span = {"span_type": "TokenCharSpan", "pos": "NN",
                           "start": 3, "end": 9,
                           "dependency": {"label": "DEP", "parent": 0}}
        token_span = SpanFactory.new_span(dict_token_span)
        assert isinstance(token_span, TokenCharSpan)
        with pytest.raises(TypeError):
            # signed as TokenCharSpan but with mismatching keys
            dict_token_span = {"span_type": "TokenCharSpan", "start": 0,
                               "end": 87, "sem_orient": 0.67922089}
            token_span = SpanFactory.new_span(dict_token_span)

    def test_new_span_sentence(self):
        dict_sentence_span = {"span_type": "SentenceCharSpan", "start": 0,
                              "end": 87, "sem_orient": 0.67922089}
        sentence_span = SpanFactory.new_span(dict_sentence_span)
        assert isinstance(sentence_span, SentenceCharSpan)
        with pytest.raises(TypeError):
            dict_sentence_span = {"span_type": "SentenceCharSpan", "pos": "NN",
                                      "start": 3, "end": 9,
                                      "dependency": {"label": "DEP", "parent": 0}}
            sentence_span = SpanFactory.new_span(dict_sentence_span)
            # assert isinstance(sentence_span, SentenceCharSpan)

    def test_new_span_sentence_id(self):
        dict_sentence_span = {"span_type": "SentenceCharSpan", "start": 0,
                              "end": 87, "sem_orient": 0.67922089, "id": 1234564211}
        sentence_span = SpanFactory.new_span(dict_sentence_span)
        assert isinstance(sentence_span, SentenceCharSpan)
        assert not hasattr(sentence_span, 'id')
        assert getattr(sentence_span, 'md5sum', None)
        assert sentence_span.md5sum == dict_sentence_span['id']
