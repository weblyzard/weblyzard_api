#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on November 14, 2019

@author: jakob <jakob.steixner@modul.ac.at>
'''
import os
import unittest

import pytest

from weblyzard_api.model import Sentence
from weblyzard_toolkit.apis.term_sense_client import TermSenseClient as LemmatizerClient

LEMMATIZER_SERVICE_URL = os.getenv('LEMMATIZER_SERVICE_URL',
                                   'http://localhost:5002')

class TestLemmatizerClient(unittest.TestCase):
    lemmatizer = LemmatizerClient(service_url=LEMMATIZER_SERVICE_URL)
    test_text = 'Nur zu, lache soviel du willst: Zugegeben, unsere Angebote sind einfach unschlagbar: Von ' \
                'Laken bis Lacken haben wir alles, wonach Sie bei den ' \
                'Angeboten der Konkurrenz lange suchen.'
    
    
    def test_plain_text_unique(self):
        
        result = self.lemmatizer.get_unique_lemmas_string(
            language='de',
            plain_text=self.test_text)

        print(result)
        assert 'Angeboten' not in result # ambiguous: Angebot, anbieten
        assert 'lache' not in result # die Lache, lachen
        assert result['Angebote'] == 'Angebot'
        assert all(isinstance(v, str) for v in result.values())

    def test_plain_text_any(self):
        result1 = self.lemmatizer.get_all_lemmas(language='de', plain_text=self.test_text)
        print(result1)
        assert 'Angeboten' in result1
        assert 'lache' in result1
        assert all(isinstance(v, list) for v in result1.values())

    def test_sentence_raw_postags(self):
        sentence = Sentence(value='Ich bin froh und lache',
                            token='0,3 4,7 8,12 13,16 17,22',
                            pos='PPN VVFIN ADJD CONJ VVFIN')
        result2 = self.lemmatizer.get_lemmas_annotated_sentence(language='de',
                                                           sentence=sentence,
                                                           check_unique=True)
        print(result2)
        assert all(isinstance(v, str) for v in result2.values())
        assert 'froh@adjective' in result2
        assert 'lache@verb' in result2

    def test_sentence_mapped_postags(self):
        sentence2 = Sentence(value='Ich bin froh und lache',
                             token='0,3 4,7 8,12 13,16 17,22',
                             pos='pronoun verb adjective conjunction verb')
        result3 = self.lemmatizer.get_lemmas_annotated_sentence(language='de',
                                                           sentence=sentence2,
                                                           check_unique=True)
        print(result3)
        assert all(isinstance(v, str) for v in result3.values())
        assert 'froh@adjective' in result3
        assert 'lache@verb' in result3

    def test_sentence_allow_multiple(self):

        sentence = Sentence(value='Ich bin froh und lache',
                             token='0,3 4,7 8,12 13,16 17,22',
                             pos='pronoun verb adjective conjunction verb')
        result = self.lemmatizer.get_lemmas_annotated_sentence(language='de',
                                                           sentence=sentence,
                                                           check_unique=False)
        assert all(isinstance(v, list) for v in result.values())
        assert 'froh@adjective' in result
        assert 'lache@verb' in result


