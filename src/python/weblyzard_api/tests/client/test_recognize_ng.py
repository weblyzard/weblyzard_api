#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Aug 30, 2016

.. codeauthor: Max Goebel <goebel@weblyzard.com>
"""

import os
import re
import unittest

import pytest

from weblyzard_api.client.recognize.ng import Recognize

SERVICE_URL = os.getenv("RECOGNIZE_NG_URL", None)


class TestRecognizeNg(unittest.TestCase):
    REQUIRED_REGEXPS = []
    UNDESIRED_REGEXPS = []

    SERVICE_URL = SERVICE_URL
    PROFILE_NAME = "en_full_all"
    URLS_PROFILES_MAPPING = None
    DOCUMENTS = [{"annotations": [],
                  "content": "Hello \"world\" more \nDonald Trump and Barack Obama are presidents in the United States. Vienna is the capital of Austria, Berlin is the capital of Germany. Linz also is in Austria 1000",
                  "format": "text/html",
                  "header": {},
                  "id": "1000",
                  "lang": "EN",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C06650B80E6ED",
                  "partitions": {"BODY": [{"@type": "CharSpan",
                                           "end": 184,
                                           "start": 20}],
                                 "LINE": [{"@type": "CharSpan", "end": 19,
                                           "start": 0},
                                          {"@type": "CharSpan",
                                           "end": 184,
                                           "start": 20}],
                                 "SENTENCE": [{"@type": "SentenceCharSpan",
                                               "end": 18,
                                               "id": "26d2d0113429b0dc98352c2b5fd842a1",
                                               "semOrient": 0.0,
                                               "significance": 0.0,
                                               "start": 0},
                                              {"@type": "SentenceCharSpan",
                                               "end": 86,
                                               "id": "ddbe82fc058d01f347dda640aa123e76",
                                               "semOrient": 0.0,
                                               "significance": 0.0,
                                               "start": 20},
                                              {"@type": "SentenceCharSpan",
                                               "end": 154,
                                               "id": "aef32ea74929a8ff3828e6285da0f915",
                                               "semOrient": 0.0,
                                               "significance": 0.0,
                                               "start": 87},
                                              {"@type": "SentenceCharSpan",
                                               "end": 184,
                                               "id": "94ae0254cdd4396fb2adbfea90676563",
                                               "semOrient": 0.0,
                                               "significance": 0.0,
                                               "start": 155}],
                                 "TITLE": [{"@type": "CharSpan", "end": 19,
                                            "start": 0}],
                                 "TOKEN": [{"@type": "TokenCharSpan",
                                            "dependency": {"label": "null",
                                                           "parent": -1},
                                            "end": 5,
                                            "pos": "UH",
                                            "start": 0},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "NMOD",
                                                           "parent": 3},
                                            "end": 7,
                                            "pos": """,
                                              "start": 6},
                                             {"@type": "TokenCharSpan",
                                              "dependency": {"label": "SUFFIX",
                                                              "parent": 1},
                                              "end": 12,
                                              "pos": "NN",
                                              "start": 7},
                                             {"@type": "TokenCharSpan",
                                              "dependency": {"label": "ROOT",
                                                              "parent": 0},
                                              "end": 13,
                                              "pos": """,
                                            "start": 12},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {
                                                "label": "SUFFIX",
                                                "parent": 3},
                                            "end": 18,
                                            "pos": "RBR",
                                            "start": 14},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "null",
                                                           "parent": -1},
                                            "end": 26,
                                            "pos": "NNP",
                                            "start": 20},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "NAME",
                                                           "parent": 2},
                                            "end": 32,
                                            "pos": "NNP",
                                            "start": 27},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "SBJ",
                                                           "parent": 6},
                                            "end": 36,
                                            "pos": "CC",
                                            "start": 33},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {
                                                "label": "COORD",
                                                "parent": 2},
                                            "end": 43,
                                            "pos": "NNP",
                                            "start": 37},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "NAME",
                                                           "parent": 5},
                                            "end": 49,
                                            "pos": "NNP",
                                            "start": 44},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "CONJ",
                                                           "parent": 3},
                                            "end": 53,
                                            "pos": "VBP",
                                            "start": 50},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "ROOT",
                                                           "parent": 0},
                                            "end": 64,
                                            "pos": "NNS",
                                            "start": 54},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "PRD",
                                                           "parent": 6},
                                            "end": 67,
                                            "pos": "IN",
                                            "start": 65},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "LOC",
                                                           "parent": 7},
                                            "end": 71,
                                            "pos": "DT",
                                            "start": 68},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "NMOD",
                                                           "parent": 11},
                                            "end": 78,
                                            "pos": "NNP",
                                            "start": 72},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "NMOD",
                                                           "parent": 11},
                                            "end": 85,
                                            "pos": "NNPS",
                                            "start": 79},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "PMOD",
                                                           "parent": 8},
                                            "end": 86,
                                            "pos": ".",
                                            "start": 85},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "null",
                                                           "parent": -1},
                                            "end": 93,
                                            "pos": "NNP",
                                            "start": 87},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "SBJ",
                                                           "parent": 2},
                                            "end": 96,
                                            "pos": "VBZ",
                                            "start": 94},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "ROOT",
                                                           "parent": 0},
                                            "end": 100,
                                            "pos": "DT",
                                            "start": 97},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "NMOD",
                                                           "parent": 4},
                                            "end": 108,
                                            "pos": "NN",
                                            "start": 101},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "PRD",
                                                           "parent": 2},
                                            "end": 111,
                                            "pos": "IN",
                                            "start": 109},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "NMOD",
                                                           "parent": 4},
                                            "end": 119,
                                            "pos": "NNP",
                                            "start": 112},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "PMOD",
                                                           "parent": 5},
                                            "end": 120,
                                            "pos": ",",
                                            "start": 119},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "P",
                                                           "parent": 9},
                                            "end": 127,
                                            "pos": "NNP",
                                            "start": 121},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "SBJ",
                                                           "parent": 9},
                                            "end": 130,
                                            "pos": "VBZ",
                                            "start": 128},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "DEP",
                                                           "parent": 14},
                                            "end": 134,
                                            "pos": "DT",
                                            "start": 131},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "NMOD",
                                                           "parent": 11},
                                            "end": 142,
                                            "pos": "NN",
                                            "start": 135},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "PRD",
                                                           "parent": 9},
                                            "end": 145,
                                            "pos": "IN",
                                            "start": 143},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "NMOD",
                                                           "parent": 11},
                                            "end": 153,
                                            "pos": "NNP",
                                            "start": 146},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "PMOD",
                                                           "parent": 12},
                                            "end": 154,
                                            "pos": ".",
                                            "start": 153},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "null",
                                                           "parent": -1},
                                            "end": 159,
                                            "pos": "NNP",
                                            "start": 155},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "SBJ",
                                                           "parent": 3},
                                            "end": 164,
                                            "pos": "RB",
                                            "start": 160},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "ADV",
                                                           "parent": 3},
                                            "end": 167,
                                            "pos": "VBZ",
                                            "start": 165},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "ROOT",
                                                           "parent": 0},
                                            "end": 170,
                                            "pos": "IN",
                                            "start": 168},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {
                                                "label": "LOC-PRD",
                                                "parent": 3},
                                            "end": 178,
                                            "pos": "NNP",
                                            "start": 171},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {"label": "HMOD",
                                                           "parent": 7},
                                            "end": 179,
                                            "pos": "\"",
                                            "start": 178},
                                           {"@type": "TokenCharSpan",
                                            "dependency": {
                                                "label": "SUFFIX",
                                                "parent": 5},
                                            "end": 184,
                                            "pos": "CD",
                                            "start": 180}]}}]

    def setUp(self):
        self.available_profiles = []
        self.client = Recognize(self.SERVICE_URL)
        self.service_is_online = self.client.is_online()
        if not self.service_is_online:
            print(
                "WARNING: Webservice is offline --> not executing all tests!!")
            self.IS_ONLINE = False
            return

    def test_available_profiles(self):
        profiles = self.client.list_profiles()
        assert len(profiles) > 0

    #     def test_search_text(self):
    #         text = "Vienna is the capital of Austria, Berlin is the capital of Germany. Linz also is in Austria"
    #         result = self.client.search_text(
    #             self.PROFILE_NAME, lang="en", text=text)
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
                annotations = result["annotations"]
                from pprint import pprint
                import json
                print(json.dumps(annotations))
                pprint(annotations)
                assert len(annotations) > 0
                document = result
            if self.REQUIRED_REGEXPS:
                for regexp in self.REQUIRED_REGEXPS:
                    assert any([re.match(regexp, entity["key"]) for entity in
                                annotations])
            if self.UNDESIRED_REGEXPS:
                for regexp in self.UNDESIRED_REGEXPS:
                    assert not any(
                        [re.match(regexp, entity["key"]) for entity in
                         annotations])


class TestRecognizeWien(TestRecognizeNg):
    PROFILE_NAME = "de_full_all"
    DOCUMENTS = [{"annotations": [],
                  "content": "Die Satzberggasse in Wien ist alles mögliche, aber weder eine wichtige Einkaufsstraße noch eine Sackgasse, und noch nicht mal eine Hauptstraße oder eine Landstraße.",
                  "format": "text/html",
                  "header": {},
                  "id": "1000",
                  "lang": "DE",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C06650B80E6ED",
                  "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]


#
# class TestRecognizeJobCockpit(TestRecognizeNg):
#     PROFILE_NAME = "JOBCOCKPIT_DE_STANF"
#
#     DOCUMENTS = [{"annotations": [],
#                   "content": "Akademiker mit mehrjähriger Berufserfahrung in der Datenaufbereitung, zuletzt in leitender Position, sucht neue Herausforderungen.",
#                   "format": "text/html",
#                   "header": {},
#                   "id": "1000",
#                   "lang": "DE",
#                   "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C06650B80E6ED",
#                   "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]
#
#


@pytest.mark.xfail(reason="Currently `de_full_all` uses only unique street "
                          "names, reactivate the test when disambiguation of "
                          "non-unique names has been reactivated in production.")
class TestRecognizeDisambiguation(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.
    Wels
    """
    REQUIRED_REGEXPS = [
        re.compile(r".*geonames.*"),
        re.compile(r".*openstreetmap.*149673")]
    UNDESIRED_REGEXPS = [re.compile(r".*openstreetmap.*23900645")]

    PROFILE_NAME = "de_full_all"

    DOCUMENTS = [{"annotations": [],
                  "content": "In der Waidhausenstraße in Wien ist ab dem 25. Januar 2021 eine Baustelle.",
                  "format": "text/html",
                  "header": {},  #
                  "id": "1000",
                  "lang": "DE",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]


@pytest.mark.xfail(
    reason="Expected to fail with switch to unique only osm lexika.")
class TestDisambiguationOsmEn(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.).
    We expect Downing Street, London
    """

    REQUIRED_REGEXPS = [re.compile(r".*geonames.*"),
                        re.compile(r".*openstreetmap.*4244999")]

    PROFILE_NAME = "en_full_all"

    DOCUMENTS = [{"annotations": [],
                  "content": "In the United Kingdom, Downing Street is more than just a street name.",
                  "format": "text/html",
                  "header": {},  #
                  "id": "1000",
                  "lang": "EN",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]


class TestDisambiguationOsmEnWallStreet(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.).
    We expect No osm entity returned because of disambiguation failure. This
    test should work even if there are issues within a country

    As of 2022-05, with a profile containing non-unique streets, this succeeds
    """

    UNDESIRED_REGEXPS = [re.compile(r".*openstreetmap.*")]

    PROFILE_NAME = "en_full_all"

    DOCUMENTS = [{"annotations": [],
                  "content": "Wall Street is performing well after an initial panic earlier today.",
                  "format": "text/html",
                  "header": {},  #
                  "id": "1000",
                  "lang": "EN",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]


@pytest.mark.xfail
class TestDisambiguationOsmEnWallStreetNewYork(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.).
    We expect https://www.openstreetmap.org/way/5672361, i.e. Wall Street
    in Manhattan, New York

    As of 2022-05, with a profile containing non-unique streets, this fails
    with another US street apparently randomly selected
    """

    REQUIRED_REGEXPS = [re.compile(r".*geonames.*"),
                        re.compile(r".*openstreetmap.*5672361.*")]
    UNDESIRED_REGEXPS = []

    PROFILE_NAME = "en_full_all"

    DOCUMENTS = [{"annotations": [],
                  "content": "New York City: Wall Street in Manhattan is performing well after an initial panic earlier today.",
                  "format": "text/html",
                  "header": {},  #
                  "id": "1000",
                  "lang": "EN",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]


@pytest.mark.xfail
class TestDisambiguationOsmEnWallStreetLA(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.).
    We expect Wall Street in LA, https://www.openstreetmap.org/way/13378624

    As of 2022-05, with a profile containing non-unique streets, this fails
    with another US street apparently randomly selected
    """

    REQUIRED_REGEXPS = [re.compile(r".*geonames.*"),
                        re.compile(r".*openstreetmap.*13378624.*")]
    UNDESIRED_REGEXPS = []

    PROFILE_NAME = "en_full_all"

    DOCUMENTS = [{"annotations": [],
                  "content": "Wall Street in Los Angeles is a different matter altogether",
                  "format": "text/html",
                  "header": {},  #
                  "id": "1000",
                  "lang": "EN",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]


@pytest.mark.xfail(
    reason="Expected to fail with switch to unique only osm lexika.")
class TestDisambiguationOsmEnAlternate(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities, countries) when occurring in
    the same text.).
    There is a Downing street in Christchurch
    """

    REQUIRED_REGEXPS = [re.compile(r".*geonames.*"),
                        re.compile(r".*openstreetmap.*22988383")]
    PROFILE_NAME = "en_full_all"

    DOCUMENTS = [{"annotations": [],
                  "content": "There is another Downing Street in New Zealand.",
                  "format": "text/html",
                  "header": {},  #
                  "id": "1000",
                  "lang": "EN",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]


@pytest.mark.xfail(
    reason="Expected to fail with switch to unique only osm lexika.")
class TestDisambiguationOsmEs(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.
    (WIP as of 2020-10-10)."""
    REQUIRED_REGEXPS = [re.compile(r".*geonames.*"),
                        re.compile(r".*openstreetmap.*")]

    PROFILE_NAME = "es_full_all"

    DOCUMENTS = [{"annotations": [],
                  "content": "Paseo de las Acacias en Murcia es una atracción principal.",
                  "format": "text/html",
                  "header": {},
                  "id": "1000",
                  "lang": "ES",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]


#
#
class TestDisambiguationOsmFr(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.
    (WIP as of 2020-10-10)."""
    REQUIRED_REGEXPS = [re.compile(r".*geonames.*"),
                        re.compile(r".*openstreetmap.*")]

    PROFILE_NAME = "fr_full_all"

    # wien gn id: http://sws.geonames.org/2761333
    # wels gn id http://sws.geonames.org/2761524
    DOCUMENTS = [{"annotations": [],
                  "content": "Rue Alphonse Daudet en Marseille c\"é un attraction principale.",
                  "format": "text/html",
                  "header": {},  #
                  "id": "1000",
                  "lang": "FR",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]


#
#
# class TestRecognizeOsmNl(TestRecognizeNg):
#     REQUIRED_REGEXPS = [re.compile(r".*openstreetmap.*")]
#     PROFILE_NAME = "nl_full_all"
#     DOCUMENTS = [{"annotations": [],
#                    "content": "Dat was in het pand aan Overdiepse-Polderweg waar nu La Cuisine is gevestigd.",
#                    "format": "text/html",
#                    "header": {},
#                    "id": "1000",
#                    "lang": "NL",
#                    "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C16650B80E6ED",
#                   "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]
#
#
# class TestRecognizeEvents(TestRecognizeNg):
#     REQUIRED_REGEXPS = [re.compile(r".*weblyzard.*event.*")]
#
#     # PROFILE_NAME = "sandbox_events"
#     PROFILE_NAME = "de_full_all"
#     DOCUMENTS = [{"annotations": [],
#                   "content": "Am Ostermontag gibt es es viel zu feiern.",
#                   "format": "text/html",
#                   "header": {},
#                   "id": "1000",
#                   "lang": "DE",
#                   "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
#                   "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]
#
#     def test_annotate_document(self):
#         for year in range(2017, 2023):
#             for countryname, country in {
#                 "austria": "http://sws.geonames.org/2782113/",
#                 "greece": "http://sws.geonames.org/390903/"
#             }.items():
#                 print(countryname, year)
#                 self.DOCUMENTS[0]["header"] = {"{http://www.weblyzard.com/wl/2013#}entity": "http://example.com/example_document",
#                               "{http://weblyzard.com/skb/property/}yearUri": "http://purl.org/dc/terms/date#{year}".format(year=year),
#                               "{http://weblyzard.com/skb/property/}location": country
#                               }
#                 self.REQUIRED_REGEXPS = [re.compile(r".*Easter.*#{year}.*".format(year=year))]
#                 TestRecognizeNg.test_annotate_document(self)
#
#
# class TestRecognizePersonEn(TestRecognizeNg):
#     REQUIRED_REGEXPS = [re.compile("http://www.wikidata.org/entity/.*")]
#

#     PROFILE_NAME = "en_full_all"
#     DOCUMENTS = [{"annotations": [],
#                   # "content": "Boris Becker is a famous tennis player.",
#                   "content": "Tony Blair is a former politician.",
#                   "format": "text/html",
#                   "header": {},
#                   "id": "1000",
#                   "lang": "DE",
#                   "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
#                   "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]
#
#
# class TestRecognizeEventsEn(TestRecognizeNg):
#     REQUIRED_REGEXPS = [re.compile(r".*weblyzard.*event.*")]
#
#     PROFILE_NAME = "en_full_all"
#     DOCUMENTS = [{"annotations": [],
#                   "content": "There\"s a lot to celebrate on Easter Monday.",
#                   "format": "text/html",
#                   "header": {},
#                   "id": "1000",
#                   "lang": "DE",
#                   "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
#                   "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]
#
#     def test_annotate_document(self):
#         for year in range(2017, 2023):
#             for countryname, country in {
#                 "austria": "http://sws.geonames.org/2782113/",
#                 "greece": "http://sws.geonames.org/390903/"}.items():
#                 print(countryname, year)
#                 self.DOCUMENTS[0]["header"] = {"{http://www.weblyzard.com/wl/2013#}entity": "http://example.com/example_document",
#                               "{http://weblyzard.com/skb/property/}yearUri": "http://purl.org/dc/terms/date#{year}".format(year=year),
#                               "{http://weblyzard.com/skb/property/}location": country
#                               }
#                 self.REQUIRED_REGEXPS = [re.compile(r".*Easter.*#{year}.*".format(year=year))]
#                 TestRecognizeNg.test_annotate_document(self)


class TestRecognizeWhiteHouse(TestRecognizeNg):
    # FIXME: Incorrect Kevin O"Connor annotated (not likely that we can fix this one due to too little Wikidata metadata)
    REQUIRED_REGEXPS = [re.compile(r"http://www.wikidata.org/entity/Q6279"),
                        # Biden
                        # re.compile(r"http://www.wikidata.org/entity/Q104881886"),  # Kevin O"Connor
                        re.compile(r"http://www.wikidata.org/entity/Q1355327"),
                        # Executive Office of the President of the United States (White House)
                        ]

    PROFILE_NAME = "en_full_bg"
    DOCUMENTS = [{"annotations": [],
                  "content": "President Biden, at 79, is of advanced age and ostensibly vulnerable to the virus’s worst effects. " +
                             "But his illness never really advanced beyond an occasional cough, elevated temperature and a stuffy nose, " +
                             "according to White House physician Kevin O’Connor. During his recovery he was residing at the presidential mansion.",
                  "format": "text/html",
                  "header": {},
                  "id": "1000",
                  "lang": "DE",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]


@pytest.mark.xfail(
    reason="This test is not working (ideally it should work and be the goal).")
class TestRecognizeUSA(TestRecognizeNg):
    # FIXME: Incorrect annotation of "The U.S.", working for "U.S."
    REQUIRED_REGEXPS = [re.compile(r"http://www.wikidata.org/entity/Q6279"),
                        # Biden
                        re.compile(r"http://sws.geonames.org/6252001/"),
                        # United States
                        re.compile(r"http://sws.geonames.org/5332921/"),
                        # California
                        ]

    PROFILE_NAME = "en_full_bg"
    DOCUMENTS = [{"annotations": [],
                  "content": """
                  California and the nation need President Biden"s vaccination mandate on companies with more than 100 employees. 
                  The new policy, announced Thursday, is necessary to quell COVID-19 and protect workers from getting the virus and spreading it 
                  to their communities. Red states, as expected, are challenging the law"s constitutionality. The U.S. Supreme Court will likely 
                  make the final call. When it does, the court should recognize the law entitles workers to a safe workplace. Biden"s rule does just that. 
                  """,
                  "format": "text/html",
                  "header": {},
                  "id": "1000",
                  "lang": "DE",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]


class TestRecognizeCustomDe(TestRecognizeNg):
    # FIXME: ORF is not annotated
    REQUIRED_REGEXPS = [
        re.compile(r"http://weblyzard.com/skb/entity/term/climate_change"),
        re.compile(r"http://www.wikidata.org/entity/Q688378")]

    PROFILE_NAME = "de_full_all"
    DOCUMENTS = [{"annotations": [],
                  "content": "Armin Wolf ist ein österreichischer Journalist, der für den ORF arbeitet. Immer wieder berichtet er auch über den Klimawandel.",
                  "format": "text/html",
                  "header": {},
                  "id": "1000",
                  "lang": "DE",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]


class TestRecognizeJournalistsDe(TestRecognizeNg):
    REQUIRED_REGEXPS = [re.compile(r"http://www.wikidata.org/entity/Q688378"),
                        re.compile(r"http://www.wikidata.org/entity/Q1342403"),
                        re.compile(
                            r"http://weblyzard.com/skb/entity/person/isabell_widek"),
                        re.compile(
                            r"http://weblyzard.com/skb/entity/person/su_sametinger"),
                        re.compile(r"http://www.wikidata.org/entity/Q1608032"),
                        re.compile(r"http://www.wikidata.org/entity/Q1729359"),
                        re.compile(
                            r"http://weblyzard.com/skb/entity/person/bernd_affenzeller"),
                        re.compile(r"http://www.wikidata.org/entity/Q1729359"),
                        ]

    PROFILE_NAME = "de_full_all"

    DOCUMENTS = [{"annotations": [],
                  "content": "Armin Wolf, Florian Klenk, Isabell Widek, Su Sametinger, Ingrid Thurnher und Karim El-Gawhary sind alle österreichische Journalisten." +
                             "Bernd Affenzeller auch. Vielleicht ist auch Karim El Gawhary ein Journalist?",
                  "format": "text/html",
                  "header": {},
                  "id": "1000",
                  "lang": "DE",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]


# class TestRecognizeBlazegraphDe(TestRecognizeNg):
#     REQUIRED_REGEXPS = [re.compile(r"http://weblyzard.com/skb/entity/term/climate_change"),
#                         re.compile(r"http://www.wikidata.org/entity/Q688378")]
#
#     PROFILE_NAME = "de_full_all_bg"
#     DOCUMENTS = [{"annotations": [],
#                   # "content": "Boris Becker is a famous tennis player.",
#                   "content": "Jenson Button,  , NOAA, Max Verstappen, alles da? Nasa calling",
#                   "format": "text/html",
#                   "header": {},
#                   "id": "1000",
#                   "lang": "DE",
#                   "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
#                   "partitions": {"BODY": [{"@type": "CharSpan",
#                                             "end": 184,
#                                             "start": 20}]}}]


class TestRecognizeEvents(TestRecognizeNg):
    REQUIRED_REGEXPS = [re.compile(r".*weblyzard.*event.*")]
    PROFILE_NAME = "de_full_all"
    DOCUMENTS = [{"annotations": [],
                  "content": "Am Ostermontag gibt es es viel zu feiern.",
                  "format": "text/html",
                  "header": {},
                  "id": "1000",
                  "lang": "DE",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": TestRecognizeNg.DOCUMENTS[0]["partitions"]}]

    def test_annotate_document(self):
        for year in range(2017, 2023):
            for countryname, country in {
                "austria": "http://sws.geonames.org/2782113/",
                "greece": "http://sws.geonames.org/390903/"
            }.items():
                print(countryname, year)
                self.DOCUMENTS[0]["header"] = {
                    "{http://www.weblyzard.com/wl/2013#}entity": "http://example.com/example_document",
                    "{http://weblyzard.com/skb/property/}yearUri": "http://purl.org/dc/terms/date#{year}".format(
                        year=year),
                    "{http://weblyzard.com/skb/property/}location": country
                }
                self.REQUIRED_REGEXPS = [
                    re.compile(r".*Easter.*#{year}.*".format(year=year))]
                TestRecognizeNg.test_annotate_document(self)


class TestRecognizeRoche(TestRecognizeNg):
    REQUIRED_REGEXPS = [
        re.compile(r"http://ontology.roche.com/ROX1301557461838")]

    PROFILE_NAME = "roche_rts_20220204"
    DOCUMENTS = [{"annotations": [],
                  # "content": "Boris Becker is a famous tennis player.",
                  "content": "What is Personalized Type 2 Diabetes Management? Currently, the management of type 2 diabetes (T2D) is driven by established international guidelines, and until recent years these did not take account of individual characteristics and the presence of co-morbidities for individual patients. Much of the treatment options recommended by guidelines are based on evidence accumulated from Phase 3 clinical trials and real-world evidence based on population-based studies. These recommendations have clearly made a difference to overall diabetes care. 1 , 2 These guidelines do not examine the concept of individualized or personalized management. Individuals differ in their presentation of T2D, some have a short duration, others a long duration and other complications at the time of presentation. Therefore, with respect to treatment, \"one size does not fit all\". More recently, the American Diabetes Association (ADA) and European Association for the Study of Diabetes (EASD) (along with other guidelines) have recommended tailoring therapy to be more stringent and less stringent based on patients attitudes, hypoglycemia risk, disease duration, life expectancy, comorbidities and resources. Personalized diabetes management is based on developing a clinical plan that is tailored to the individual. This may take into account many complex factors. These included patient factors, social, medical (including complications) as well as phenotypic, biochemical and genetic factors (see Figure 1 ). Therefore, the concept of personalized management is complex and broad. The therapeutic options for managing T2D have increased considerably in the past 10 years, so perhaps the time has come to focus and tailor therapy to the phenotype and personal characteristics of the patient. Personalized care may provide the opportunity to address two potential reasons for the continued morbidity and mortality associated with T2D. These include firstly, the suboptimal application of evidence-based therapies (eg, due to lack of medication intensification or insufficient lifestyle changes or medication adherence by patients) and secondly inadequate efficacies of current therapies when optimally applied. Figure 1 Personalized diabetes care. This figure summarizes the key considerations that are needed when contemplating the choice of diabetes pharmacotherapy for a patient with T2D.",
                  "format": "text/html",
                  "header": {},
                  "id": "1000",
                  "lang": "DE",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": {"BODY": [{"@type": "CharSpan",
                                           "end": 184,
                                           "start": 20}]}}]


@pytest.mark.skip(reason="For manual testing.")
class TestRecognizeGeonames(TestRecognizeNg):
    REQUIRED_REGEXPS = []

    example = "The United States is a country with a lot of states, such as Alabama or New York County."
    example1 = "At least 10 people have been killed in the US state of Arkansas as storms and tornadoes careered up a swathe of the central United States. The latest victim was found dead in central Arkansas, local police said. Five others died as flood waters swept their cars off the road in the state's north-west, while four more died in a small town ravaged by a tornado. The National Weather Service issued a high risk warning across across Tennesee, Arkansas, and Texas. Meanwhile in Poplar Bluff, Missouri, 17,000 residents are hoping a levee holds and prevents major flooding. Storms have pummelled states across the region for weeks and more rain is due. More than a dozen tornadoes were reported in Texas and Arkansas on Monday night. In eastern Texas, damage was reported in the largely rural Houston County but the extent was unclear because much of the area was without power, the Associated Press quoted Fire Marshal David Lamb as saying."
    example2 = "The Dothan-Houston County Emergency Management Agency is working with Houston County Schools and local law enforcement agencies to perform a drill on Thursday simulating the evacuation of certain areas, including two county schools. The drill will be conducted from 9:30 to 11 a.m., according to a release from Chris Judah, director of the Dothan-Houston County Emergency Management Agency (EMA). The drill will involve Ashford High School and Houston County High School in Columbia and will evaluate several variables, according to Judah. The simulated evacuations will require the transport to a reunification center, and several buses from each school will be escorted from the schools via law enforcement to a reception center located at the Houston County Career Academy on West Main Street in Dothan. There will be no students on the buses. Neither the parents of students in these schools nor residents of the areas involved in drill should be alarmed."
    example3 = "Focus Russia: The year 2014 will be remembered as a transitional year in the political climate of Europe. Following the civil war in eastern Ukraine and the incorporation of Crimea by the Russian Federation, the continent is experiencing a reversal from a system of consensus into a system that is more reminiscent of the past opposition between NATO and the Warsaw Pact. This shift may seem even more surprising, because the new order that had rapidly emerged after the end of the cold war, with its regular conferences and summits, had become the order of the day. Unfortunately, international relations do not follow a uniform path of progress; there is, of course, no “end to history”."

    PROFILE_NAME = "en_full_bg"
    DOCUMENTS = [{"annotations": [],
                  "content": example1,
                  "format": "text/html",
                  "header": {},
                  "id": "1000",
                  "lang": "DE",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": {"BODY": [{"@type": "CharSpan",
                                           "end": 184,
                                           "start": 20}]}}]


class TestRecognizeGeonamesAU(TestRecognizeNg):
    REQUIRED_REGEXPS = ["http://sws.geonames.org/7839347/",  # Broome
                        "http://sws.geonames.org/2075265/",  # Busselton
                        "http://sws.geonames.org/2067119/",  # Mandurah
                        "http://sws.geonames.org/2077963/",  # Albany
                        "http://sws.geonames.org/2077456/",  # Australia
                        "http://sws.geonames.org/7839517/",
                        # Jondaloop (through regex)
                        "http://sws.geonames.org/7839519/",
                        # Kalgoorlie (through regex)
                        "http://sws.geonames.org/2071858/",
                        # Esperance (through regex)
                        ]

    text = """
    Travelling through Australia there are a lot of areas to see: Mandurah, Busselton, Joondalup. Albany is very well known.
    Less well known are Esperance, Broome and Kalgoorlie, but still worth a visit. Shire of Esperance and Kalgoorlie Boulder are regions. 
    """

    PROFILE_NAME = "en_full_bg_A"
    DOCUMENTS = [{"annotations": [],
                  "content": text,
                  "format": "text/html",
                  "header": {},
                  "id": "1000",
                  "lang": "EN",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": {"BODY": [{"@type": "CharSpan",
                                           "end": 184,
                                           "start": 20}]}}]


class TestRecognizeCountries(TestRecognizeNg):
    REQUIRED_REGEXPS = ["http://sws.geonames.org/6254930/",  # Palestine
                        ]

    text = """
    It runs nurseries, soup kitchens, libraries, sporting clubs, a television channel and a children’s magazine.
    Such services meet a need for ordinary Palestinians, who are starved, harassed and murdered by the Israeli occupation.
    The formation of the group was linked to the rise of Islamist groups known as the Muslim Brotherhood across the Middle East. The Muslim Brotherhood in Palestine was formed in 1946.
    From its beginning Hamas has had to transform itself repeatedly, shifting its theory, ideology and politics to be in step with the ordinary Palestinians and maintain popular support.
    The group spelled out its aims in the 1988 covenant, written during the First Intifada.
    """

    PROFILE_NAME = "de_full_bg"
    DOCUMENTS = [{"annotations": [],
                  "content": text,
                  "format": "text/html",
                  "header": {},
                  "id": "1000",
                  "lang": "EN",
                  "nilsimsa": "00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED",
                  "partitions": {"BODY": [{"@type": "CharSpan",
                                           "end": 184,
                                           "start": 20}]}}]


if __name__ == "__main__":
    unittest.main()
