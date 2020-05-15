#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on May 15, 2020

@author: jakob <jakob.steixner@modul.ac.at>
'''
import os
import unittest

from weblyzard_api.client.openthesaurus import OpenThesaurusClient

OPEN_THESAURUS_SERVICE_URL = os.getenv(
    'OPEN_THESAURUS_SERVICE_URL',
    'https://www.openthesaurus.de')


class TestOpenThesaurusClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.openthesaurus = OpenThesaurusClient(OPEN_THESAURUS_SERVICE_URL)

    def test_get_synsets(self):
        result = self.openthesaurus.get_synsets('lockerung')
        assert result
        assert isinstance(result, dict)
        assert all(isinstance(k, int) for k in result.keys())
        assert all(isinstance(k, list) for k in result.values())

    def test_get_plain_synonyms(self):
        result = self.openthesaurus.get_plain_synonyms('lockerung')
        assert result
        assert isinstance(result, set)
        assert all(isinstance(k, str) for k in result)
