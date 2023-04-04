#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2016

.. codeauthor: Max Goebel <goebel@weblyzard.com>
'''

import unittest
import re
import os
import pytest

from collections import OrderedDict

from weblyzard_api.client.recognize.ng import Recognize

# RECOGNIZE_NG_SERVICE_URL = os.getenv('RECOGNIZE_NG_URL', None)
RECOGNIZE_NG_SERVICE_URL = 'http://recognize-ng-develop.branch.i.weblyzard.net:8443'


class TestRecognizeNg(unittest.TestCase):

    REQUIRED_REGEXPS = []
    UNDESIRED_REGEXPS = []

    SERVICE_URL = RECOGNIZE_NG_SERVICE_URL
    PROFILE_NAME = 'en_full_all'
    URLS_PROFILES_MAPPING = None
    DOCUMENTS = [{u'annotations': [],
                  u'content': u'Hello "world" more \nDonald Trump and Barack Obama are presidents in the United States. Vienna is the capital of Austria, Berlin is the capital of Germany. Linz also is in Austria" 1000',
                  u'format': u'text/html',
                  u'header': {},
                  u'id': u'1000',
                  u'lang': u'EN',
                  u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C06650B80E6ED',
                  u'partitions': {u'BODY': [{u'@type': u'CharSpan',
                                             u'end': 184,
                                             u'start': 20}],
                                  u'LINE': [{u'@type': u'CharSpan', u'end': 19, u'start': 0},
                                            {u'@type': u'CharSpan',
                                             u'end': 184,
                                             u'start': 20}],
                                  u'SENTENCE': [{u'@type': u'SentenceCharSpan',
                                                 u'end': 18,
                                                 u'id': u'26d2d0113429b0dc98352c2b5fd842a1',
                                                 u'semOrient': 0.0,
                                                 u'significance': 0.0,
                                                 u'start': 0},
                                                {u'@type': u'SentenceCharSpan',
                                                 u'end': 86,
                                                 u'id': u'ddbe82fc058d01f347dda640aa123e76',
                                                 u'semOrient': 0.0,
                                                 u'significance': 0.0,
                                                 u'start': 20},
                                                {u'@type': u'SentenceCharSpan',
                                                 u'end': 154,
                                                 u'id': u'aef32ea74929a8ff3828e6285da0f915',
                                                 u'semOrient': 0.0,
                                                 u'significance': 0.0,
                                                 u'start': 87},
                                                {u'@type': u'SentenceCharSpan',
                                                 u'end': 184,
                                                 u'id': u'94ae0254cdd4396fb2adbfea90676563',
                                                 u'semOrient': 0.0,
                                                 u'significance': 0.0,
                                                 u'start': 155}],
                                  u'TITLE': [{u'@type': u'CharSpan', u'end': 19, u'start': 0}],
                                  u'TOKEN': [{u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'null',
                                                              u'parent':-1},
                                              u'end': 5,
                                              u'pos': u'UH',
                                              u'start': 0},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NMOD',
                                                              u'parent': 3},
                                              u'end': 7,
                                              u'pos': u"'",
                                              u'start': 6},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'SUFFIX',
                                                              u'parent': 1},
                                              u'end': 12,
                                              u'pos': u'NN',
                                              u'start': 7},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'ROOT',
                                                              u'parent': 0},
                                              u'end': 13,
                                              u'pos': u"'",
                                              u'start': 12},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'SUFFIX',
                                                              u'parent': 3},
                                              u'end': 18,
                                              u'pos': u'RBR',
                                              u'start': 14},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'null',
                                                              u'parent':-1},
                                              u'end': 26,
                                              u'pos': u'NNP',
                                              u'start': 20},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NAME',
                                                              u'parent': 2},
                                              u'end': 32,
                                              u'pos': u'NNP',
                                              u'start': 27},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'SBJ',
                                                              u'parent': 6},
                                              u'end': 36,
                                              u'pos': u'CC',
                                              u'start': 33},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'COORD',
                                                              u'parent': 2},
                                              u'end': 43,
                                              u'pos': u'NNP',
                                              u'start': 37},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NAME',
                                                              u'parent': 5},
                                              u'end': 49,
                                              u'pos': u'NNP',
                                              u'start': 44},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'CONJ',
                                                              u'parent': 3},
                                              u'end': 53,
                                              u'pos': u'VBP',
                                              u'start': 50},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'ROOT',
                                                              u'parent': 0},
                                              u'end': 64,
                                              u'pos': u'NNS',
                                              u'start': 54},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'PRD',
                                                              u'parent': 6},
                                              u'end': 67,
                                              u'pos': u'IN',
                                              u'start': 65},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'LOC',
                                                              u'parent': 7},
                                              u'end': 71,
                                              u'pos': u'DT',
                                              u'start': 68},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NMOD',
                                                              u'parent': 11},
                                              u'end': 78,
                                              u'pos': u'NNP',
                                              u'start': 72},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NMOD',
                                                              u'parent': 11},
                                              u'end': 85,
                                              u'pos': u'NNPS',
                                              u'start': 79},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'PMOD',
                                                              u'parent': 8},
                                              u'end': 86,
                                              u'pos': u'.',
                                              u'start': 85},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'null',
                                                              u'parent':-1},
                                              u'end': 93,
                                              u'pos': u'NNP',
                                              u'start': 87},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'SBJ',
                                                              u'parent': 2},
                                              u'end': 96,
                                              u'pos': u'VBZ',
                                              u'start': 94},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'ROOT',
                                                              u'parent': 0},
                                              u'end': 100,
                                              u'pos': u'DT',
                                              u'start': 97},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NMOD',
                                                              u'parent': 4},
                                              u'end': 108,
                                              u'pos': u'NN',
                                              u'start': 101},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'PRD',
                                                              u'parent': 2},
                                              u'end': 111,
                                              u'pos': u'IN',
                                              u'start': 109},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NMOD',
                                                              u'parent': 4},
                                              u'end': 119,
                                              u'pos': u'NNP',
                                              u'start': 112},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'PMOD',
                                                              u'parent': 5},
                                              u'end': 120,
                                              u'pos': u',',
                                              u'start': 119},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'P', u'parent': 9},
                                              u'end': 127,
                                              u'pos': u'NNP',
                                              u'start': 121},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'SBJ',
                                                              u'parent': 9},
                                              u'end': 130,
                                              u'pos': u'VBZ',
                                              u'start': 128},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'DEP',
                                                              u'parent': 14},
                                              u'end': 134,
                                              u'pos': u'DT',
                                              u'start': 131},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NMOD',
                                                              u'parent': 11},
                                              u'end': 142,
                                              u'pos': u'NN',
                                              u'start': 135},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'PRD',
                                                              u'parent': 9},
                                              u'end': 145,
                                              u'pos': u'IN',
                                              u'start': 143},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'NMOD',
                                                              u'parent': 11},
                                              u'end': 153,
                                              u'pos': u'NNP',
                                              u'start': 146},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'PMOD',
                                                              u'parent': 12},
                                              u'end': 154,
                                              u'pos': u'.',
                                              u'start': 153},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'null',
                                                              u'parent':-1},
                                              u'end': 159,
                                              u'pos': u'NNP',
                                              u'start': 155},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'SBJ',
                                                              u'parent': 3},
                                              u'end': 164,
                                              u'pos': u'RB',
                                              u'start': 160},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'ADV',
                                                              u'parent': 3},
                                              u'end': 167,
                                              u'pos': u'VBZ',
                                              u'start': 165},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'ROOT',
                                                              u'parent': 0},
                                              u'end': 170,
                                              u'pos': u'IN',
                                              u'start': 168},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'LOC-PRD',
                                                              u'parent': 3},
                                              u'end': 178,
                                              u'pos': u'NNP',
                                              u'start': 171},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'HMOD',
                                                              u'parent': 7},
                                              u'end': 179,
                                              u'pos': u"'",
                                              u'start': 178},
                                             {u'@type': u'TokenCharSpan',
                                              u'dependency': {u'label': u'SUFFIX',
                                                              u'parent': 5},
                                              u'end': 184,
                                              u'pos': u'CD',
                                              u'start': 180}]}}]

    def setUp(self):
        self.available_profiles = []
        self.client = Recognize(self.SERVICE_URL)
        self.service_is_online = self.client.is_online()
        if not self.service_is_online:
            print('WARNING: Webservice is offline --> not executing all tests!!')
            self.IS_ONLINE = False
            return

    def test_available_profiles(self):
        profiles = self.client.list_profiles()
        assert len(profiles) > 0

#     def test_search_text(self):
#         text = 'Vienna is the capital of Austria, Berlin is the capital of Germany. Linz also is in Austria'
#         result = self.client.search_text(
#             self.PROFILE_NAME, lang='en', text=text)
#         assert len(result) == 6

    def test_annotate_document(self):
        if not self.URLS_PROFILES_MAPPING:
            urls_profiles_mapping = [(self.SERVICE_URL, self.PROFILE_NAME)]
        else:
            urls_profiles_mapping = self.URLS_PROFILES_MAPPING
        for document in self.DOCUMENTS:
            for url, profile in urls_profiles_mapping:
                client = Recognize(url)
                result = client.search_document(profile_name=profile,
                                                document=document, limit=0)
                annotations = result['annotations']
                from pprint import pprint
                import json
                print(json.dumps(annotations))
                pprint(annotations)
                assert len(annotations) > 0
                document = result
            if self.REQUIRED_REGEXPS:
                for regexp in self.REQUIRED_REGEXPS:
                    assert any([re.match(regexp, entity['key']) for entity in annotations])
            if self.UNDESIRED_REGEXPS:
                for regexp in self.UNDESIRED_REGEXPS:
                    assert not any([re.match(regexp, entity['key']) for entity in annotations])


class TestRecognizeWien(TestRecognizeNg):

    PROFILE_NAME = 'de_full_all'
    DOCUMENTS = [{u'annotations': [],
                   u'content': u'Die Satzberggasse in Wien ist alles mögliche, aber weder eine wichtige Einkaufsstraße noch eine Sackgasse, und noch nicht mal eine Hauptstraße oder eine Landstraße.',
                   u'format': u'text/html',
                   u'header': {},
                   u'id': u'1000',
                   u'lang': u'DE',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]

#
# class TestRecognizeJobCockpit(TestRecognizeNg):
#     PROFILE_NAME = "JOBCOCKPIT_DE_STANF"
#
#     DOCUMENTS = [{u'annotations': [],
#                   u'content': u'Akademiker mit mehrjähriger Berufserfahrung in der Datenaufbereitung, zuletzt in leitender Position, sucht neue Herausforderungen.',
#                   u'format': u'text/html',
#                   u'header': {},
#                   u'id': u'1000',
#                   u'lang': u'DE',
#                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C06650B80E6ED',
#                   u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]
#
#


@pytest.mark.xfail(reason='Currently `de_full_all` uses only unique street '
                         'names, reactivate the test when disambiguation of '
                         'non-unique names has been reactivated in production.')
class TestRecognizeDisambiguation(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.
    Wels
    """
    REQUIRED_REGEXPS = [
        re.compile(r'.*geonames.*'),
        re.compile(r'.*openstreetmap.*149673')]
    UNDESIRED_REGEXPS = [re.compile(r'.*openstreetmap.*23900645')]

    PROFILE_NAME = 'de_full_all'

    DOCUMENTS = [{u'annotations': [],
                   u'content': 'In der Waidhausenstraße in Wien ist ab dem 25. Januar 2021 eine Baustelle.',
                   u'format': u'text/html',
                   u'header': {},  #
                   u'id': u'1000',
                   u'lang': u'DE',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                   u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


@pytest.mark.xfail(reason='Expected to fail with switch to unique only osm lexika.')
class TestDisambiguationOsmEn(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.).
    We expect Downing Street, London
    """

    REQUIRED_REGEXPS = [re.compile(r'.*geonames.*'), re.compile(r'.*openstreetmap.*4244999')]

    PROFILE_NAME = 'en_full_all'

    DOCUMENTS = [{u'annotations': [],
                   u'content': 'In the United Kingdom, Downing Street is more than just a street name.',
                   u'format': u'text/html',
                   u'header': {},  #
                   u'id': u'1000',
                   u'lang': u'EN',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


class TestDisambiguationOsmEnWallStreet(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.).
    We expect No osm entity returned because of disambiguation failure. This
    test should work even if there are issues within a country

    As of 2022-05, with a profile containing non-unique streets, this succeeds
    """

    UNDESIRED_REGEXPS = [re.compile(r'.*openstreetmap.*')]

    PROFILE_NAME = 'en_full_all'

    DOCUMENTS = [{u'annotations': [],
                   u'content': 'Wall Street is performing well after an initial panic earlier today.',
                   u'format': u'text/html',
                   u'header': {},  #
                   u'id': u'1000',
                   u'lang': u'EN',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


@pytest.mark.xfail
class TestDisambiguationOsmEnWallStreetNewYork(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.).
    We expect https://www.openstreetmap.org/way/5672361, i.e. Wall Street
    in Manhattan, New York

    As of 2022-05, with a profile containing non-unique streets, this fails
    with another US street apparently randomly selected
    """

    REQUIRED_REGEXPS = [re.compile(r'.*geonames.*'), re.compile(r'.*openstreetmap.*5672361.*')]
    UNDESIRED_REGEXPS = []

    PROFILE_NAME = 'en_full_all'

    DOCUMENTS = [{u'annotations': [],
                   u'content': 'New York City: Wall Street in Manhattan is performing well after an initial panic earlier today.',
                   u'format': u'text/html',
                   u'header': {},  #
                   u'id': u'1000',
                   u'lang': u'EN',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


@pytest.mark.xfail
class TestDisambiguationOsmEnWallStreetLA(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.).
    We expect Wall Street in LA, https://www.openstreetmap.org/way/13378624

    As of 2022-05, with a profile containing non-unique streets, this fails
    with another US street apparently randomly selected
    """

    REQUIRED_REGEXPS = [re.compile(r'.*geonames.*'), re.compile(r'.*openstreetmap.*13378624.*')]
    UNDESIRED_REGEXPS = []

    PROFILE_NAME = 'en_full_all'

    DOCUMENTS = [{u'annotations': [],
                   u'content': 'Wall Street in Los Angeles is a different matter altogether',
                   u'format': u'text/html',
                   u'header': {},  #
                   u'id': u'1000',
                   u'lang': u'EN',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


@pytest.mark.xfail(reason='Expected to fail with switch to unique only osm lexika.')
class TestDisambiguationOsmEnAlternate(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities, countries) when occurring in
    the same text.).
    There is a Downing street in Christchurch
    """

    REQUIRED_REGEXPS = [re.compile(r'.*geonames.*'), re.compile(r'.*openstreetmap.*22988383')]
    PROFILE_NAME = 'en_full_all'

    DOCUMENTS = [{u'annotations': [],
                   u'content': 'There is another Downing Street in New Zealand.',
                   u'format': u'text/html',
                   u'header': {},  #
                   u'id': u'1000',
                   u'lang': u'EN',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


@pytest.mark.xfail(reason='Expected to fail with switch to unique only osm lexika.')
class TestDisambiguationOsmEs(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.
    (WIP as of 2020-10-10)."""
    REQUIRED_REGEXPS = [re.compile(r'.*geonames.*'), re.compile(r'.*openstreetmap.*')]

    PROFILE_NAME = 'es_full_all'

    DOCUMENTS = [{u'annotations': [],
                   u'content': 'Paseo de las Acacias en Murcia es una atracción principal.',
                   u'format': u'text/html',
                   u'header': {},
                   u'id': u'1000',
                   u'lang': u'ES',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


#
#
class TestDisambiguationOsmFr(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.
    (WIP as of 2020-10-10)."""
    REQUIRED_REGEXPS = [re.compile(r'.*geonames.*'), re.compile(r'.*openstreetmap.*')]

    PROFILE_NAME = 'fr_full_all'

    # wien gn id: http://sws.geonames.org/2761333
    # wels gn id http://sws.geonames.org/2761524
    DOCUMENTS = [{u'annotations': [],
                   u'content': 'Rue Alphonse Daudet en Marseille c\'é un attraction principale.',
                   u'format': u'text/html',
                   u'header': {},  #
                   u'id': u'1000',
                   u'lang': u'FR',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]

#
#
# class TestRecognizeOsmNl(TestRecognizeNg):
#     REQUIRED_REGEXPS = [re.compile(r'.*openstreetmap.*')]
#     PROFILE_NAME = 'nl_full_all'
#     DOCUMENTS = [{u'annotations': [],
#                    u'content': u'Dat was in het pand aan Overdiepse-Polderweg waar nu La Cuisine is gevestigd.',
#                    u'format': u'text/html',
#                    u'header': {},
#                    u'id': u'1000',
#                    u'lang': u'NL',
#                    u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C16650B80E6ED',
#                   u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]
#
#
# class TestRecognizeEvents(TestRecognizeNg):
#     REQUIRED_REGEXPS = [re.compile(r'.*weblyzard.*event.*')]
#
#     # PROFILE_NAME = 'sandbox_events'
#     PROFILE_NAME = 'de_full_all'
#     DOCUMENTS = [{u'annotations': [],
#                   'content': 'Am Ostermontag gibt es es viel zu feiern.',
#                   u'format': u'text/html',
#                   u'header': {},
#                   u'id': u'1000',
#                   u'lang': u'DE',
#                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
#                   u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]
#
#     def test_annotate_document(self):
#         for year in range(2017, 2023):
#             for countryname, country in {
#                 'austria': 'http://sws.geonames.org/2782113/',
#                 'greece': 'http://sws.geonames.org/390903/'
#             }.items():
#                 print(countryname, year)
#                 self.DOCUMENTS[0]['header'] = {'{http://www.weblyzard.com/wl/2013#}entity': 'http://example.com/example_document',
#                               '{http://weblyzard.com/skb/property/}yearUri': 'http://purl.org/dc/terms/date#{year}'.format(year=year),
#                               '{http://weblyzard.com/skb/property/}location': country
#                               }
#                 self.REQUIRED_REGEXPS = [re.compile(r'.*Easter.*#{year}.*'.format(year=year))]
#                 TestRecognizeNg.test_annotate_document(self)
#
#
# class TestRecognizePersonEn(TestRecognizeNg):
#     REQUIRED_REGEXPS = [re.compile('http://www.wikidata.org/entity/.*')]
#

#     PROFILE_NAME = 'en_full_all'
#     DOCUMENTS = [{u'annotations': [],
#                   # 'content': 'Boris Becker is a famous tennis player.',
#                   'content': 'Tony Blair is a former politician.',
#                   u'format': u'text/html',
#                   u'header': {},
#                   u'id': u'1000',
#                   u'lang': u'DE',
#                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
#                   u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]
#
#
# class TestRecognizeEventsEn(TestRecognizeNg):
#     REQUIRED_REGEXPS = [re.compile(r'.*weblyzard.*event.*')]
#
#     PROFILE_NAME = 'en_full_all'
#     DOCUMENTS = [{u'annotations': [],
#                   'content': 'There\'s a lot to celebrate on Easter Monday.',
#                   u'format': u'text/html',
#                   u'header': {},
#                   u'id': u'1000',
#                   u'lang': u'DE',
#                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
#                   u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]
#
#     def test_annotate_document(self):
#         for year in range(2017, 2023):
#             for countryname, country in {
#                 'austria': 'http://sws.geonames.org/2782113/',
#                 'greece': 'http://sws.geonames.org/390903/'}.items():
#                 print(countryname, year)
#                 self.DOCUMENTS[0]['header'] = {'{http://www.weblyzard.com/wl/2013#}entity': 'http://example.com/example_document',
#                               '{http://weblyzard.com/skb/property/}yearUri': 'http://purl.org/dc/terms/date#{year}'.format(year=year),
#                               '{http://weblyzard.com/skb/property/}location': country
#                               }
#                 self.REQUIRED_REGEXPS = [re.compile(r'.*Easter.*#{year}.*'.format(year=year))]
#                 TestRecognizeNg.test_annotate_document(self)


class TestRecognizeWhiteHouse(TestRecognizeNg):
    # FIXME: Incorrect Kevin O'Connor annotated (not likely that we can fix this one due to too little Wikidata metadata)
    REQUIRED_REGEXPS = [re.compile(r'http://www.wikidata.org/entity/Q6279'),  # Biden
                        # re.compile(r'http://www.wikidata.org/entity/Q104881886'),  # Kevin O'Connor
                        re.compile(r'http://www.wikidata.org/entity/Q1355327'),  # Executive Office of the President of the United States (White House)
                        ]

    PROFILE_NAME = 'en_full_bg'
    DOCUMENTS = [{u'annotations': [],
                  'content': 'President Biden, at 79, is of advanced age and ostensibly vulnerable to the virus’s worst effects. ' +
                             'But his illness never really advanced beyond an occasional cough, elevated temperature and a stuffy nose, ' +
                             'according to White House physician Kevin O’Connor. During his recovery he was residing at the presidential mansion.',
                  u'format': u'text/html',
                  u'header': {},
                  u'id': u'1000',
                  u'lang': u'DE',
                  u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]
    
@pytest.mark.xfail(reason='This test is not working (ideally it should work and be the goal).')
class TestRecognizeUSA(TestRecognizeNg):
    # FIXME: Incorrect annotation of "The U.S.", working for "U.S."
    REQUIRED_REGEXPS = [re.compile(r'http://www.wikidata.org/entity/Q6279'),  # Biden
                        re.compile(r'http://sws.geonames.org/6252001/'),  # United States
                        re.compile(r'http://sws.geonames.org/5332921/'),  # California
                        ]

    PROFILE_NAME = 'en_full_bg'
    DOCUMENTS = [{u'annotations': [],
                  'content': '''
                  California and the nation need President Biden's vaccination mandate on companies with more than 100 employees. 
                  The new policy, announced Thursday, is necessary to quell COVID-19 and protect workers from getting the virus and spreading it 
                  to their communities. Red states, as expected, are challenging the law's constitutionality. The U.S. Supreme Court will likely 
                  make the final call. When it does, the court should recognize the law entitles workers to a safe workplace. Biden's rule does just that. 
                  ''',
                  u'format': u'text/html',
                  u'header': {},
                  u'id': u'1000',
                  u'lang': u'DE',
                  u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


class TestRecognizeCustomDe(TestRecognizeNg):
    # FIXME: ORF is not annotated
    REQUIRED_REGEXPS = [re.compile(r'http://weblyzard.com/skb/entity/term/climate_change'),
                        re.compile(r'http://www.wikidata.org/entity/Q688378')]

    PROFILE_NAME = 'de_full_all'
    DOCUMENTS = [{u'annotations': [],
                  'content': 'Armin Wolf ist ein österreichischer Journalist, der für den ORF arbeitet. Immer wieder berichtet er auch über den Klimawandel.',
                  u'format': u'text/html',
                  u'header': {},
                  u'id': u'1000',
                  u'lang': u'DE',
                  u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


class TestRecognizeJournalistsDe(TestRecognizeNg):
    REQUIRED_REGEXPS = [re.compile(r'http://www.wikidata.org/entity/Q688378'),
                        re.compile(r'http://www.wikidata.org/entity/Q1342403'),
                        re.compile(r'http://weblyzard.com/skb/entity/person/isabell_widek'),
                        re.compile(r'http://weblyzard.com/skb/entity/person/su_sametinger'),
                        re.compile(r'http://www.wikidata.org/entity/Q1608032'),
                        re.compile(r'http://www.wikidata.org/entity/Q1729359'),
                        re.compile(r'http://weblyzard.com/skb/entity/person/bernd_affenzeller'),
                        re.compile(r'http://www.wikidata.org/entity/Q1729359'),
                        ]

    PROFILE_NAME = 'de_full_all'

    DOCUMENTS = [{u'annotations': [],
                'content': 'Armin Wolf, Florian Klenk, Isabell Widek, Su Sametinger, Ingrid Thurnher und Karim El-Gawhary sind alle österreichische Journalisten.' +
                            'Bernd Affenzeller auch. Vielleicht ist auch Karim El Gawhary ein Journalist?',
                  u'format': u'text/html',
                  u'header': {},
                  u'id': u'1000',
                  u'lang': u'DE',
                  u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]

# class TestRecognizeBlazegraphDe(TestRecognizeNg):
#     REQUIRED_REGEXPS = [re.compile(r'http://weblyzard.com/skb/entity/term/climate_change'),
#                         re.compile(r'http://www.wikidata.org/entity/Q688378')]
#
#     PROFILE_NAME = 'de_full_all_bg'
#     DOCUMENTS = [{u'annotations': [],
#                   # 'content': 'Boris Becker is a famous tennis player.',
#                   'content': 'Jenson Button,  , NOAA, Max Verstappen, alles da? Nasa calling',
#                   u'format': u'text/html',
#                   u'header': {},
#                   u'id': u'1000',
#                   u'lang': u'DE',
#                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
#                   u'partitions': {u'BODY': [{u'@type': u'CharSpan',
#                                             u'end': 184,
#                                             u'start': 20}]}}]


class TestRecognizeEvents(TestRecognizeNg):
    REQUIRED_REGEXPS = [re.compile(r'.*weblyzard.*event.*')]
    SERVICE_URL = 'http://recognize-ng.prod.i.weblyzard.net:8443'
    PROFILE_NAME = 'de_full_all'
    DOCUMENTS = [{u'annotations': [],
                  'content': 'Am Ostermontag gibt es es viel zu feiern.',
                  u'format': u'text/html',
                  u'header': {},
                  u'id': u'1000',
                  u'lang': u'DE',
                  u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]

    def test_annotate_document(self):
        for year in range(2017, 2023):
            for countryname, country in {
                'austria': 'http://sws.geonames.org/2782113/',
                'greece': 'http://sws.geonames.org/390903/'
            }.items():
                print(countryname, year)
                self.DOCUMENTS[0]['header'] = {'{http://www.weblyzard.com/wl/2013#}entity': 'http://example.com/example_document',
                              '{http://weblyzard.com/skb/property/}yearUri': 'http://purl.org/dc/terms/date#{year}'.format(year=year),
                              '{http://weblyzard.com/skb/property/}location': country
                              }
                self.REQUIRED_REGEXPS = [re.compile(r'.*Easter.*#{year}.*'.format(year=year))]
                TestRecognizeNg.test_annotate_document(self)


class TestRecognizeRoche(TestRecognizeNg):
    REQUIRED_REGEXPS = [re.compile(r'http://ontology.roche.com/ROX1301557461838')]

    PROFILE_NAME = 'roche_rts_20220204'
    DOCUMENTS = [{u'annotations': [],
                  # 'content': 'Boris Becker is a famous tennis player.',
                  'content': 'What is Personalized Type 2 Diabetes Management? Currently, the management of type 2 diabetes (T2D) is driven by established international guidelines, and until recent years these did not take account of individual characteristics and the presence of co-morbidities for individual patients. Much of the treatment options recommended by guidelines are based on evidence accumulated from Phase 3 clinical trials and real-world evidence based on population-based studies. These recommendations have clearly made a difference to overall diabetes care. 1 , 2 These guidelines do not examine the concept of individualized or personalized management. Individuals differ in their presentation of T2D, some have a short duration, others a long duration and other complications at the time of presentation. Therefore, with respect to treatment, "one size does not fit all". More recently, the American Diabetes Association (ADA) and European Association for the Study of Diabetes (EASD) (along with other guidelines) have recommended tailoring therapy to be more stringent and less stringent based on patients attitudes, hypoglycemia risk, disease duration, life expectancy, comorbidities and resources. Personalized diabetes management is based on developing a clinical plan that is tailored to the individual. This may take into account many complex factors. These included patient factors, social, medical (including complications) as well as phenotypic, biochemical and genetic factors (see Figure 1 ). Therefore, the concept of personalized management is complex and broad. The therapeutic options for managing T2D have increased considerably in the past 10 years, so perhaps the time has come to focus and tailor therapy to the phenotype and personal characteristics of the patient. Personalized care may provide the opportunity to address two potential reasons for the continued morbidity and mortality associated with T2D. These include firstly, the suboptimal application of evidence-based therapies (eg, due to lack of medication intensification or insufficient lifestyle changes or medication adherence by patients) and secondly inadequate efficacies of current therapies when optimally applied. Figure 1 Personalized diabetes care. This figure summarizes the key considerations that are needed when contemplating the choice of diabetes pharmacotherapy for a patient with T2D.',
                  u'format': u'text/html',
                  u'header': {},
                  u'id': u'1000',
                  u'lang': u'DE',
                  u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': {u'BODY': [{u'@type': u'CharSpan',
                                            u'end': 184,
                                            u'start': 20}]}}]

@pytest.mark.skip(reason='For manual testing.')
class TestRecognizeGeonames(TestRecognizeNg):
    REQUIRED_REGEXPS = []

    example = "The United States is a country with a lot of states, such as Alabama or New York County."
    example1 = "At least 10 people have been killed in the US state of Arkansas as storms and tornadoes careered up a swathe of the central United States. The latest victim was found dead in central Arkansas, local police said. Five others died as flood waters swept their cars off the road in the state's north-west, while four more died in a small town ravaged by a tornado. The National Weather Service issued a high risk warning across across Tennesee, Arkansas, and Texas. Meanwhile in Poplar Bluff, Missouri, 17,000 residents are hoping a levee holds and prevents major flooding. Storms have pummelled states across the region for weeks and more rain is due. More than a dozen tornadoes were reported in Texas and Arkansas on Monday night. In eastern Texas, damage was reported in the largely rural Houston County but the extent was unclear because much of the area was without power, the Associated Press quoted Fire Marshal David Lamb as saying."
    example2 = "The Dothan-Houston County Emergency Management Agency is working with Houston County Schools and local law enforcement agencies to perform a drill on Thursday simulating the evacuation of certain areas, including two county schools. The drill will be conducted from 9:30 to 11 a.m., according to a release from Chris Judah, director of the Dothan-Houston County Emergency Management Agency (EMA). The drill will involve Ashford High School and Houston County High School in Columbia and will evaluate several variables, according to Judah. The simulated evacuations will require the transport to a reunification center, and several buses from each school will be escorted from the schools via law enforcement to a reception center located at the Houston County Career Academy on West Main Street in Dothan. There will be no students on the buses. Neither the parents of students in these schools nor residents of the areas involved in drill should be alarmed."
    example3 = "Focus Russia: The year 2014 will be remembered as a transitional year in the political climate of Europe. Following the civil war in eastern Ukraine and the incorporation of Crimea by the Russian Federation, the continent is experiencing a reversal from a system of consensus into a system that is more reminiscent of the past opposition between NATO and the Warsaw Pact. This shift may seem even more surprising, because the new order that had rapidly emerged after the end of the cold war, with its regular conferences and summits, had become the order of the day. Unfortunately, international relations do not follow a uniform path of progress; there is, of course, no “end to history”."

    PROFILE_NAME = 'en_full_bg'
    DOCUMENTS = [{u'annotations': [],
                  u'content': example1,
                  u'format': u'text/html',
                  u'header': {},
                  u'id': u'1000',
                  u'lang': u'DE',
                  u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': {u'BODY': [{u'@type': u'CharSpan',
                                            u'end': 184,
                                            u'start': 20}]}}]
    
class TestRecognizeGeonamesAU(TestRecognizeNg):
    REQUIRED_REGEXPS = ['http://sws.geonames.org/7839347/', # Broome
                        'http://sws.geonames.org/2075265/', # Busselton
                        'http://sws.geonames.org/2067119/', # Mandurah
                        'http://sws.geonames.org/2077963/', # Albany
                        'http://sws.geonames.org/2077456/', # Australia
                        'http://sws.geonames.org/7839517/', # Jondaloop (through regex)
                        'http://sws.geonames.org/7839519/', # Kalgoorlie (through regex)
                        'http://sws.geonames.org/2071858/', # Esperance (through regex)
                        ]

    text = '''
    Travelling through Australia there are a lot of areas to see: Mandurah, Busselton, Joondalup. Albany is very well known.
    Less well known are Esperance, Broome and Kalgoorlie, but still worth a visit. Shire of Esperance and Kalgoorlie Boulder are regions. 
    '''
    
    PROFILE_NAME = 'en_full_bg_AU'
    DOCUMENTS = [{u'annotations': [],
                  u'content': text,
                  u'format': u'text/html',
                  u'header': {},
                  u'id': u'1000',
                  u'lang': u'EN',
                  u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': {u'BODY': [{u'@type': u'CharSpan',
                                            u'end': 184,
                                            u'start': 20}]}}]


if __name__ == '__main__':
    unittest.main()
