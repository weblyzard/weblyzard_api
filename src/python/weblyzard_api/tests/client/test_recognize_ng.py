#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2016

.. codeauthor: max goebel <mcgoebel@gmail.com>
'''
from __future__ import print_function
from __future__ import unicode_literals
import unittest
import re
import copy
import os

from collections import OrderedDict

from weblyzard_api.client.recognize.ng import Recognize

RECOGNIZE_NG_SERVICE_URL = os.getenv('RECOGNIZE_NG_URL', 'http://gecko9.wu.ac.at:8089/rest')


class TestRecognizeNg(unittest.TestCase):

    REQUIRED_REGEXPS = []

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


class TestRecognizeWien(TestRecognizeNg):

    PROFILE_NAME = 'de_full_all'
    DOCUMENTS = [{u'annotations': [],
                   u'content': u'Die Hufgasse in Wien ist alles mögliche, aber weder eine wichtige Einkaufsstraße noch eine Sackgasse, und noch nicht mal eine Hauptstraße oder eine Landstraße.',
                   u'format': u'text/html',
                   u'header': {},
                   u'id': u'1000',
                   u'lang': u'DE',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


class TestRecognizeJobCockpit(TestRecognizeNg):
    PROFILE_NAME = "JOBCOCKPIT_DE_STANF"
    # SERVICE_URL = 'http://localhost:63007/rest'

    # SERVICE_URL = 'http://gecko9.wu.ac.at:8089/rest'
    DOCUMENTS = [{u'annotations': [],
                  u'content': u'Akademiker mit mehrjähriger Berufserfahrung in der Datenaufbereitung, zuletzt in leitender Position, sucht neue Herausforderungen.',
                  u'format': u'text/html',
                  u'header': {},
                  u'id': u'1000',
                  u'lang': u'DE',
                  u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


class TestRecognizeDisambiguation(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.
    Wels
    """
    REQUIRED_REGEXPS = [re.compile(r'.*geonames.*'), re.compile(r'.*openstreetmap.*')]

    PROFILE_NAME = 'de_full_all'

    DOCUMENTS = [{u'annotations': [],
                   u'content': 'In der Waidhausenstraße in Wien ist ab dem 25. Januar 2021 eine Baustelle.',
                   u'format': u'text/html',
                   u'header': {},  #
                   u'id': u'1000',
                   u'lang': u'DE',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                   u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


class TestDisambiguationOsmEn(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.).
    We expect Downing Street, London
    """

    REQUIRED_REGEXPS = [re.compile(r'.*geonames.*'), re.compile(r'.*openstreetmap.*4244999')]

    PROFILE_NAME = 'en_full_all_new'

    DOCUMENTS = [{u'annotations': [],
                   u'content': 'In the United Kingdom, Downing Street is more than just a street name.',
                   u'format': u'text/html',
                   u'header': {},  #
                   u'id': u'1000',
                   u'lang': u'EN',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


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


class TestDisambiguationOsmFr(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.
    (WIP as of 2020-10-10)."""
    REQUIRED_REGEXPS = [re.compile(r'.*geonames.*'), re.compile(r'.*openstreetmap.*')]
    # SERVICE_URL = 'http://gecko9.wu.ac.at:8089'

    SERVICE_URL = 'http://recognize-ng.prod.i.weblyzard.net:8443'
    #
    PROFILE_NAME = 'fr_full_all' \


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


class TestRecognizeOsmNl(TestRecognizeNg):
    REQUIRED_REGEXPS = [re.compile(r'.*openstreetmap.*')]
    # SERVICE_URL = 'http://gecko9.wu.ac.at:8089/rest'
    PROFILE_NAME = 'nl_full_all'
    DOCUMENTS = [{u'annotations': [],
                   u'content': u'Dat was in het pand aan Overdiepse-Polderweg waar nu La Cuisine is gevestigd.',
                   u'format': u'text/html',
                   u'header': {},
                   u'id': u'1000',
                   u'lang': u'NL',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C16650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


class TestRecognizeEvents(TestRecognizeNg):
    REQUIRED_REGEXPS = [re.compile(r'.*weblyzard.*event.*')]
    # SERVICE_URL = 'http://localhost:63007/rest'
    # SERVICE_URL = 'http://gecko9.wu.ac.at:8089/rest'

    SERVICE_URL = 'http://recognize-ng.prod.i.weblyzard.net:8443'
    # PROFILE_NAME = 'sandbox_events'
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


class TestRecognizePersonEn(TestRecognizeNg):
    REQUIRED_REGEXPS = [re.compile('http://www.wikidata.org/entity/.*')]

    SERVICE_URL = 'http://recognize-ng.prod.i.weblyzard.net:8443'
    PROFILE_NAME = 'en_full_all'
    DOCUMENTS = [{u'annotations': [],
                  # 'content': 'Boris Becker is a famous tennis player.',
                  'content': 'Tony Blair is a former politician.',
                  u'format': u'text/html',
                  u'header': {},
                  u'id': u'1000',
                  u'lang': u'DE',
                  u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


class TestRecognizeEventsEn(TestRecognizeNg):
    REQUIRED_REGEXPS = [re.compile(r'.*weblyzard.*event.*')]
    # SERVICE_URL = 'http://localhost:63007/rest'
    # SERVICE_URL = 'http://gecko9.wu.ac.at:8089/rest'

    SERVICE_URL = 'http://recognize-ng.prod.i.weblyzard.net:8443'
    # PROFILE_NAME = 'sandbox_events'
    PROFILE_NAME = 'en_full_all'
    DOCUMENTS = [{u'annotations': [],
                  'content': 'There\'s a lot to celebrate on Easter Monday.',
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
                'greece': 'http://sws.geonames.org/390903/'}.items():
                print(countryname, year)
                self.DOCUMENTS[0]['header'] = {'{http://www.weblyzard.com/wl/2013#}entity': 'http://example.com/example_document',
                              '{http://weblyzard.com/skb/property/}yearUri': 'http://purl.org/dc/terms/date#{year}'.format(year=year),
                              '{http://weblyzard.com/skb/property/}location': country
                              }
                self.REQUIRED_REGEXPS = [re.compile(r'.*Easter.*#{year}.*'.format(year=year))]
                TestRecognizeNg.test_annotate_document(self)


class TestRecognizeCustomDe(TestRecognizeNg):
    REQUIRED_REGEXPS = [re.compile(r'http://weblyzard.com/skb/entity/term/climate_change'),
                        re.compile(r'http://www.wikidata.org/entity/Q688378')]

    SERVICE_URL = 'http://localhost:63007/rest'
    PROFILE_NAME = 'journalists_test'
    DOCUMENTS = [{u'annotations': [],
                  # 'content': 'Boris Becker is a famous tennis player.',
                  'content': 'Armin Wolf ist ein österreichischer Journalist, der für den ORF arbeitet. Immer wieder berichtet er auch über den Klimawandel.',
                  u'format': u'text/html',
                  u'header': {},
                  u'id': u'1000',
                  u'lang': u'DE',
                  u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


class TestRecognizeJournalistsDe(TestRecognizeNg):
    REQUIRED_REGEXPS = [re.compile(r'http://weblyzard.com/skb/entity/term/climate_change'),
                        re.compile(r'http://www.wikidata.org/entity/Q688378')]

    SERVICE_URL = 'http://recognize-ng.prod.i.weblyzard.net:8443'
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


if __name__ == '__main__':
    unittest.main()
