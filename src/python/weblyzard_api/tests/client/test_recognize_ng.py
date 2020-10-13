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

from collections import OrderedDict

from weblyzard_api.client.recognize.ng import Recognize


class TestRecognizeNg(unittest.TestCase):

    REQUIRED_REGEXPS = []

    SERVICE_URL = 'http://gecko6.wu.ac.at:8089/rest'
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
                                                              u'parent': -1},
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
                                                              u'parent': -1},
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
                                                              u'parent': -1},
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
                                                              u'parent': -1},
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
                client =  Recognize(url)
                result = client.search_document(profile_name=profile,
                                                     document=document, limit=0)
                annotations = result['annotations']
                from pprint import pprint
                pprint(annotations)
                assert len(annotations) > 0
                document = result
            if self.REQUIRED_REGEXPS:
                    for regexp in self.REQUIRED_REGEXPS:
                        assert any([re.match(regexp, entity['key']) for entity in annotations])

class TestRecognizeWien(TestRecognizeNg):

    # SERVICE_URL = 'http://gecko6.wu.ac.at:8089/rest'
    SERVICE_URL = 'http://localhost:63007/rest'
    PROFILE_NAME = 'test_street_disambiguation2'
    DOCUMENTS = [{u'annotations': [],
                   u'content': u'Die Hufgasse in Wien ist alles mögliche, aber nicht ist die bekannteste Einkaufsstraße im Westen von Deutschland.',
                   u'format': u'text/html',
                   u'header': {},
                   u'id': u'1000',
                   u'lang': u'DE',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]

class TestRecognizeDisambiguation(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.
    (WIP as of 2020-10-10)."""
    REQUIRED_REGEXPS = [re.compile(r'.*geonames.*'), re.compile(r'.*openstreetmap.*')]
    SERVICE_URL = 'http://localhost:63007/rest'
    PROFILE_NAME = 'test_street_disambiguation3'
    # PROFILE_NAME = 'de_full_all'

    # wien gn id: http://sws.geonames.org/2761333
    # wels gn id http://sws.geonames.org/2761524
    DOCUMENTS = [{u'annotations': [],
                   u'content': u'Die Waidhausenstraße in Wien  (http://sws.geonames.org/2761369/) ist seit 20. August 2020 um eine Attraktion reicher.',
                   u'format': u'text/html',
                   u'header': {},
                   u'id': u'1000',
                   u'lang': u'DE',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]

class TestRecognizeOsmNl(TestRecognizeNg):
    REQUIRED_REGEXPS = [re.compile(r'.*openstreetmap.*')]
    SERVICE_URL = 'http://gecko6.wu.ac.at:8089/rest'
    PROFILE_NAME = 'wl_full_osm_date_nl'
    DOCUMENTS = [{u'annotations': [],
                   u'content': u'Met de aankondiging van de sluiting van Schrameijer Meubelen komt er een einde aan een tijdperk. In 1976 begonnen Hennie en Gea Schrameijer met een antiekzaak. Dat was in het pand aan de Overdiepse-Polderweg waar nu La Cuisine is gevestigd. Later kwamen daar grenen meubelen bij; Hennie ging naar Duitsland voor de inkoop, Gea had de winkel onder haar hoede.',
                   u'format': u'text/html',
                   u'header': {},
                   u'id': u'1000',
                   u'lang': u'NL',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


class TestRecognizeOsmNl2(TestRecognizeOsmNl):
    REQUIRED_REGEXPS = [re.compile(r'.*openstreetmap.*')]
    PROFILE_NAME =  'wl_full_osm_date_nl'
    DOCUMENTS = TestRecognizeOsmNl.DOCUMENTS
    DOCUMENTS[0]['content'] = """En passant slaat Sjors nog een gratis knipbeurt af. ,,Nee dat hoef niet, ik ga maar één keer per jaar naar de kapper.''. Udo, die tijdens zijn geboorte een hersenbeschadiging opliep, vergaarde roem met 'het fietspompje' op de website Dumpert.nl . Rapper Sjors heeft zijn bekendheid vooral te danken aan het bezoek van tv-programma Man Bijt Hond aan zijn ouderlijk huis in 2013. Ook haalde hij het nieuws met optredens die niet helemaal goed verliepen en zijn strijd tegen kanker . Udo heeft zondag al snel last van de warmte: ,,Ik heb het zweet tussen mijn bilnaat zitten.'' De cameraman reageert met een verrassende kwinkslag naar de gewelddadige drillraps: ,,Oh wacht, we doen een drillbilrap.''. Burgemeesteres Bruls. De twee hadden de grootste schik samen. Terwijl ze door de Marikenstraat lopen bespreken ze de grootste hiphop-legendes van Nederland. Rapper Sjors: ,,Je hebt Udo de Beatboxer, Udo de Beatboxer 2.0 en Udo de Beatboxer met de rode pet.''. Tot rappen en beatboxen komen de twee niet, maar Sjors heeft nog wel een boodschap voor 'burgemeesteres Bruls'. ,,Hij moet niet zoveel brullen.''."""

if __name__ == '__main__':
    unittest.main()
