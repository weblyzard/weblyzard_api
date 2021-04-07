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

from weblyzard_api.client.recognize.ng import Recognize


class TestRecognizeNg(unittest.TestCase):

    REQUIRED_REGEXPS = []

    SERVICE_URL = 'localhost:63007/rest'
    PROFILE_NAME = 'wl_full_international_en'
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
#         text = 'Vienna is the capital of Austri
    #         a, Berlin is the capital of Germany. Linz also is in Austria'
#         result = self.client.search_text(
#             self.PROFILE_NAME, lang='en', text=text)
#         assert len(result) == 6

    def test_annotate_document(self):
        for document in self.DOCUMENTS:

            result = self.client.search_document(profile_name=self.PROFILE_NAME,
                                                 document=document, limit=0)
            annotations = result['annotations']
            from pprint import pprint
            pprint(annotations)
            assert len(annotations) > 0


            # for url, profile in urls_profiles_mapping:
            #     client =  Recognize(url)
            #     result = client.search_document(profile_name=profile,
            #                                          document=document, limit=0)
            #     annotations = result['annotations']
            #     from pprint import pprint
            #     pprint(annotations)
            #     assert len(annotations) > 0
            #     document = result
            if self.REQUIRED_REGEXPS:
                    for regexp in self.REQUIRED_REGEXPS:
                        assert any([re.match(regexp, entity['key']) for entity in annotations]), "Missing pattern %s" % regexp


class TestRecognizeEvent(TestRecognizeNg):
    # REQUIRED_REGEXPS = ['.*Ascension.*']
    SERVICE_URL = 'http://localhost:63007/rest'
    # SERVICE_URL = 'http://gecko6.wu.ac.at:8089/rest'
    PROFILE_NAME = 'sandbox_events'
    DOCUMENTS = [{u'annotations': [],
                   u'content': u'In der Felbigergasse ist von Ostermontag bis zum Staatsfeiertag eine Baustelle.',
                   u'format': u'text/html',
                   u'header': {
                       '{http://www.weblyzard.com/wl/2013#}entity': 'http://example.com/ns/DefaultEntity',
                       '{http://weblyzard.com/skb/property/}yearUri': 'http://purl.org/dc/terms/date#2021',
                       '{http://weblyzard.com/skb/property/}country': 'http://sws.geonames.org/390903/', # Greece
                       # '{http://weblyzard.com/skb/property/}country': 'http://sws.geonames.org/2782113/', # Austria
                   },

                   u'id': u'1000',
                   u'lang': u'DE',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


class TestRecognizeWien(TestRecognizeNg):

    SERVICE_URL = 'http://gecko6.wu.ac.at:8089/rest'
    # SERVICE_URL = 'http://localhost:63007/rest'
    PROFILE_NAME = 'de_full_all'
    DOCUMENTS = [{u'annotations': [],
                   # u'content':"""Feministische Demo in der Mariahilfer Straße von Polizei aufgelöst. Eine nicht angemeldete, spontane Kundgebung von feministischen Aktivistinnen und Aktivisten hat Donnerstagfrüh den äußeren Gürtel beim Westbahnhof blockiert. Die Polizei löste die Demo am Vormittag auf. Am Nachmittag wurde vor dem Frauenministerium demonstriert. 04.03.2021 11.17. Online seit gestern, 11.17 Uhr (Update: gestern, 16.58 Uhr). Beim Westbahnhof am Mariahilfer Gürtel hatten sich in der Früh laut Polizei rund 20 Teilnehmerinnen und Teilnehmer zusammengefunden. Die Demonstranten sprachen von 70 Personen. Sie wollten auf den internationalen feministischen Kampftag am 8. März aufmerksam machen. Dabei handelte es sich laut Aussendung der Demonstrierenden um einen Zusammenschluss verschiedener Gruppierungen, die mit technischen Blockademitteln sowie einer Sitzblockade Stillstand der Politik symbolisch auf die Straße bringen wollen. Die Blockade zum Auftakt der feministischen Kampftage am Wiener Gürtel steht stabil! 60 Aktivist*innen feiern keinen "fröhlichen Frauentag" sondern fordern den Stopp von #Femiziden! #jederTag8M #femizidestoppen pic.twitter.com/1sRVUmcbR3. — kollektivlauter* (@kollektivlaute1) 4. März 2021. Demonstrationen am 8. März. Sie übten Kritik nicht nur an der österreichischen Politik, sondern auch an der zu wenig geführten öffentlichen Debatte über strukturelle Diskriminierung und sexualisierte Gewalt an Frauen. An der Aktion nahmen Menschen teil, die sich als Frauen, Lesben, intersexuell, nicht-binär, als Trans Personen oder nicht geschlechtlich identifizieren. "Täglich werden Menschen aufgrund ihres Geschlechts bzw. Gender in ihren Lebensbelangen zurückgehalten und unterdrückt. Deswegen reicht es nicht aus nur an einem Tag im Jahr für Gleichberechtigung auf allen Ebenen zu streiken", sagte eine Teilnehmerin in der Aussendung. Für den 8. März sind zwei Demonstrationen mit Start um 14.00 Uhr am Karlsplatz und um 17.00 Uhr am Stephansplatz angekündigt. Am #Europaplaz haben unsere Kolleg*innen mit den Teilnehmer*innen der spontanen Kundgebung Kontakt aufgenommen. Die Kundgebung wurde unsererseits aufgelöst. Entsprechende Durchsagen erfolgten bereits vor Ort. #Westbahnhof. — Polizei Wien (@LPDWien) 4. März 2021. Stau am äußeren Gürtel. "Ein fröhlicher "Weltfrauentag" sei fehl am Platz, wenn Tag für Tag Frauen sowie trans- und nicht binär geschlechtliche Personen Gewalt erfahren, sagte ein weiterer Teilnehmer. Während der Pandemie haben vor allem Frauen die Mehrarbeit durch die Krise getragen, auch die Zahlen von Gewalt gegen Frauen seien gestiegen. Laut den Aktivisten seien im vergangenen Jahr 25 Femizide verübt worden, aber gleichzeitig die finanziellen Mittel für Frauenhäusern reduziert worden. Für den Individualverkehr bedeutete die Aktion allerdings einige Verzögerungen in dem Bereich. Durch die Sitzblockade musste der Verkehr des äußeren Gürtels über die Felberstraße umgeleitet werden. Der Stau reichte laut ÖAMTC etwa einen Kilometer bis zur Jörgerstraße zurück. Am inneren Gürtel kam es ebenfalls zu Problemen, weil die Autofahrer nicht in die Felberstraße abbiegen konnten. Kritik an verstärkter Ungleichheit durch Coronavirus. In Form einer Kundgebung vor dem Frauenministerium haben Aktivistinnen dann am Nachmittag auf die pandemiebedingte verstärkte Benachteiligung der Frauen aufmerksam gemacht. Rund 100 Teilnehmende forderten am Minoritenplatz in der Wiener Innenstadt Schutz- und Entlastungsmaßnahmen. Angeführt wurde die Initiative vom Verein Feministische Alleinerzieherinnen (FEM.A), dem Verein Autonome Österreichische Frauenhäuser (AÖF) und dem Österreichischen Frauenring (ÖFR). 42 Organisationen und Einzelpersonen beteiligten sich – unter Einhaltung von Abstands- und Maskenpflicht – an der Aktion, darunter Nationalratsabgeordnete und Ex-Frauenministerin Gabriele Heinisch-Hosek (SPÖ) und NEOS-Mandatarin Henrike Brandstötter. "Diese Frauenministerin schweigt, sie ist zu leise. Es reicht den Frauen, sie sind belastet. Die Frauen können nicht mehr", kritisierte Heinisch-Hosek die aktuelle Ressortchefin Susanne Raab (ÖVP). Brandstötter betonte vor allem die Wichtigkeit finanzieller Unabhängigkeit: "Unsere Freiheit beginnt mit der eigenen Geldbörse", so die NEOS-Frauensprecherin, die außerdem die Umsetzung des Gender Budgeting forderte. Auch Heinisch-Hosek und Brandstötter als Rednerinnen bei Demo vor Frauenministerium. "Man fühlt sich vom Staat alleine gelassen" Opferschutz und Arbeitsmarktmaßnahmen zählten zu den zentralen Forderungen der Aktivistinnen. "Alle spüren die Überlastung und wir vermissen eine soziale Frauenpolitik", hatte FEM.A-Obfrau Andrea Czak in ihrer Eröffnungsrede beklagt. Sie glaube, es gäbe einen großen Unmut über die "Retropolitik" der Bundesregierung und sparte ebenso nicht mit Kritik an Raab und der ÖVP. AÖF-Geschäftsführerin Maria Rösslhumer hob die vielen krisenbedingten Unsicherheiten hervor. Immer mehr Frauen würden sich melden, weil sie sich etwa Miete und Heizkosten nicht mehr leisten könnten: "Man fühlt sich vom Staat alleine gelassen." Auch ÖFR-Vorsitzende Klaudia Frieben forderte ein Umdenken der Regierung: "Wir brauchen eine Politik, die es Frauen ermöglicht, in Zukunft eine Existenz zu haben." red, wien.ORF.at/Agenturen.""",
                  'content': 'In Eisenach gibt es einen Karlsplatz',
                   u'format': u'text/html',
                   u'header': {},
                   u'id': u'1000',
                   u'lang': u'DE',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]

class TestRecognizeDisambiguateGeorgia(TestRecognizeNg):

    # SERVICE_URL = 'http://gecko6.wu.ac.at:8089/rest'
    SERVICE_URL = 'http://localhost:63007/rest'
    PROFILE_NAME = 'test_georgia'
    DOCUMENTS = [{u'annotations': [],
                   u'content': u'Almost all votes in Georgia are counted, with most of the remainder in Atlanta and a few other major cities.',
                   u'format': u'text/html',
                   u'header': {},
                   u'id': u'1000',
                   u'lang': u'EN',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


class TestRecognizeJobCockpit(TestRecognizeNg):
    PROFILE_NAME = "JOBCOCKPIT_DE_STANF"
    SERVICE_URL = 'http://localhost:63007/rest'
    DOCUMENTS = [{u'annotations': [],
                  u'content': u'Akademiker mit mehrjähriger Berufserfahrung in der Datenaufbereitung, zuletzt in leitender Position, sucht neue Herausforderungen.',
                  u'format': u'text/html',
                  u'header': {},
                  u'id': u'1000',
                  u'lang': u'DE',
                  u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


class TestRecognizeOsmEs(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.
    (WIP as of 2020-10-10)."""
    REQUIRED_REGEXPS = [re.compile(r'.*geonames.*'), re.compile(r'.*openstreetmap.*')]
    # SERVICE_URL = 'http://localhost:63007/rest'
    SERVICE_URL = 'http://gecko6.wu.ac.at:8089'
    # PROFILE_NAME = 'street_names_only_sample_at'

    PROFILE_NAME = 'es_full_all'

    # wien gn id: http://sws.geonames.org/2761333
    # wels gn id http://sws.geonames.org/2761524
    DOCUMENTS = [{u'annotations': [],
                  'content': 'En la Calle del Carpio en Ávila será fiesta.',
                   u'format': u'text/html',
                   u'header': {},#
                   u'id': u'1000',
                   u'lang': u'ES',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
                  u'partitions': TestRecognizeNg.DOCUMENTS[0]['partitions']}]


class TestRecognizeDisambiguation(TestRecognizeNg):
    """Test contextual disambiguation of string-identical streets
    based on their parent attributes (cities) when occurring in the same text.
    (WIP as of 2020-10-10)."""
    REQUIRED_REGEXPS = [re.compile(r'.*geonames.*'), re.compile(r'.*openstreetmap.*')]
    SERVICE_URL = 'http://localhost:63007/rest'
    # SERVICE_URL = 'http://gecko6.wu.ac.at:8089'
    PROFILE_NAME = 'street_names_only_sample_at'

    # PROFILE_NAME = 'de_full_all'

    # wien gn id: http://sws.geonames.org/2761333
    # wels gn id http://sws.geonames.org/2761524
    DOCUMENTS = [{u'annotations': [],
                   # u'content': '''Unsere Filialen mit Käsetheke. 1020 Wien, Heinestraße 24-28. 1020 Wien, Vorgartenstr. 223A-B. 1030 Wien, Landstraßer Hauptstr. 153-155. 1030 Wien, Ungargasse 66. 1070 Wien, Stiftgasse 5-9. 1070 Wien, Zieglergasse 8. 1100 Wien, Laxenburgerstr. 151 A. 1100 Wien, Absberggasse 53. 1100 Wien, Davidgasse 47. 1100 Wien, Gudrunstr. 109-113. 1100 Wien, Gussriegelstraße 63. 1100 Wien, Triesterstr. 40. 1100 Wien, Wienerbergstr. 21. 1110 Wien, Etrichstraße 21. 1110 Wien, Kaiser Ebersdorfer Str. 57. 1110 Wien, Leberstr. 58. 1120 Wien, Sagedergasse 44. 1120 Wien, Tivoligasse 11. 1140 Wien, Linzerstr. 463. 1140 Wien, Waidhausenstr. 25. 1160 Wien, Thaliastraße 102. 1160 Wien, Wattgasse 34. 1170 Wien, Heigerleinstraße 43. 1170 Wien, Hernalser Hauptstr. 59-63. 1200 Wien, Fr.-Engels-Platz 12. 1200 Wien, Klosterneuburgerstr. 79. 1210 Wien, Christian Bucher-G. 35-37. 1210 Wien, Gerasdorfer Str. 9. 1210 Wien, Leopoldauer Str. 165. 1210 Wien, Seyringer Straße 10. 1210 Wien, Shuttleworthstr. 6. 1220 Wien, Breitenleerstr. 2. 1220 Wien, Gewerbeparkstr. 2. 1220 Wien, Lieblgasse 1. 1220 Wien, Quadenstr. 33. 1230 Wien, Breitenfurter Straße 351. 1230 Wien, Sterngasse 11. 1230 Wien, Triester Str. 256. 2000 Stockerau, Wiener Str. 24. 2020 Hollabrunn, Anton Ehrenfried-Str. 3. 2100 Korneuburg, Wiener Straße 42. 2130 Mistelbach, Mitschastr. 35a. 2136 Laa/Thaya, Thayapark 5. 2230 Gänserndorf, Neusiedler Str. 7. 2320 Schwechat, Franz Schubert Str. 5. 2325 Himberg, Gewerbestr. 2. 2331 Vösendorf, Nordring 16-18. 2340 Mödling, Neudorfer Straße 70 - 72. 2345 Brunn am Gebirge, Feldstr. 40. 2345 Brunn/Gebirge - Perchtoldsdorf, L.-Gattringer Str. 115-117. 2410 Hainburg a d Donau, Pressburger Reichsstraße 1. 2421 Kittsee, Eisenstädter Straße 33. 2460 Bruck an der Leitha, Altstadt 125-127. 2483 Ebreichsdorf, Wr. Neustädter Str. 36 - 38. 2490 Ebenfurth, Wr. Neustädter Str. 10. 2500 Baden, Dammgasse 62. 2514 Traiskirchen, Wiener Str. 77. 2540 Bad Vöslau, Badner Str. 100. 2542 Kottingbrunn, Wr. Neustädter Str. 40. 2603 Felixdorf, Wr. Neustädter Str. 46. 2620 Neunkirchen, Schraubenwerkstr. 8. 2640 Gloggnitz, Wiener Str. 54-56. 2700 Wr. Neustadt, Fischauergasse 213. Neustadt, Neudörfler Str. 55. Neustadt, Stadionstr. 44. 3002 Purkersdorf, Wiener Str. 21 / B1. 3021 Pressbaum, Hauptstr. 74b. 3100 St. Pölten, Mariazeller Str. 24-26. 3100 St. Pölten, Hermann Gmeiner-G.1. 3100 St. Pölten, Hermann Winger-G. 14. 3100 St. Pölten, Porschestr. 12. 3130 Herzogenburg, Wiener Str. 25. 3250 Wieselburg, Zeiselgraben 2. 3300 Amstetten, Wiener Strasse 44. 3340 Waidhofen a.d. Ybbs, Wiener Str. 47. 3370 Ybbs, Bahnhofstr. 1. 3430 Tulln, Bahnhofstr. 44-46. 3500 Krems, Hafenstr. 54. 3500 Krems, Wachaustr. 15-31. 3580 Horn, Prager Straße 19. 3830 Waidhofen a. d. Thaya, Brunner Str. 29. 3910 Zwettl, Kremser Str. 50. 4020 Linz, Franckstr. 18. 4020 Linz, Kaisergasse 16a. 4020 Linz, Landwiedstr. 125-127. 4020 Linz, Salzburger Straße 266. 4050 Traun, Kremstalstr. 92. 4052 Ansfelden, Auweg 1. 4070 Eferding, Linzer Str. 16. 4072 Alkoven, Wehrgasse 1. 4100 Ottensheim, Hostauerstr. 87. 4209 Engerwitzdorf, Linzerberg 21. 4240 Freistadt, Scharizer Straße 1. 4300 St. Valentin, Westbahnstraße 76. 4310 Mauthausen, Linzer Straße 71. 4320 Perg, Naarner Str. 54. 4400 Steyr, Eisenstr. 44. 4400 Steyr, Ennser Str. 12. 4470 Enns, Dr.-Karl-Renner-Str. 20. 4481 Asten, Handelsring 2. 4522 Sierning, Lagerhausstraße 19. 4540 Bad Hall, Bahnhofplatz 3. 4560 Kirchdorf, Am Brauteich 8. 4600 Wels, Ginzkeystraße 27. 4600 Wels, Magazinstr. 8-10. 4600 Wels, Oberfeldstraße 117. 4614 Marchtrenk, Viktoria-Weinzierl-Straße 1. 4650 Lambach, Salzburger Str. 50. 4655 Vorchdorf, Neue Landstr. 61. 4663 Laakirchen, Dopplingerstr. 7. 4800 Attnang-Puchheim, Salzburger Str. 90. 4810 Gmunden, Druckereistr. 40. 4840 Vöcklabruck, Rosenweg 2. 4860 Lenzing, Agerstraße 6. 4911 Tumeltsham, Schnalla 17. 5020 Salzburg, Aigner Str. 55a. 5020 Salzburg, Bahnhofstr. 41. 5020 Salzburg, Robinigstraße 9. 5081 Anif, Gewerbeparkstr. 2. 5230 Mattighofen, Gartenstraße 16. 5280 Braunau, Salzburger Straße 70. 5400 Hallein, Bürgermeisterstr. 7. 5500 Bischofshofen, Gasteiner Str. 60. 5580 Tamsweg, Florianistraße 3. 5600 St. Johann / Pg., Bundesstr. 8. 5700 Zell am See, Flugplatzstr. 40. 6020 Innsbruck, Valiergasse 2. 6060 Hall, Getzner Straße 2. 6176 Völs, Cytastraße 12. 6200 Jenbach, Austr. 21a. 6300 Wörgl, Johann Federer-Str. 30. 6330 Kufstein, Rosenheimerstraße 9. 6330 Kufstein, Salurner Str. 36. 6410 Telfs, Untermarktstr. 53. 6460 Imst, Industriezone 34a. 6500 Landeck, Bruggfeldstr. 12-14. 6600 Reutte, Innsbrucker Bundesstr. 12. 6706 Bürs, Hauptstr. 4. 6780 Schruns, Gantschierstr. 15. 6820 Frastanz, Feldkircher Str. 37. 6840 Götzis, Im Buch 47. 6850 Dornbirn, Lustenauer Str. 46. 6890 Lustenau, Kaiser-Franz-Josef Str. 28. 7000 Eisenstadt, Ruster Straße 145. 7100 Neusiedl am See, Wiener Str. 108. 7132 Frauenkirchen, Mönchhoferstr. 5a. 7210 Mattersburg, Arenaplatz 4/1. 7350 Oberpullendorf, Eisenstädter Str. 2. 7400 Oberwart, Wiener Straße 65. 7423 Pinkafeld, Wiener Str. 64. 7540 Güssing, Wiener Str. 27. 8010 Graz, Conrad-von-Hötzendorf Straße 165. 8010 Graz, Koßgasse 10. 8020 Graz, Eggenberger Allee 6. 8020 Graz, Karlauer Str. 26. 8020 Graz, Lauzilgasse 21-23. 8041 Graz, Liebenauer Hauptstrasse 164. 8045 Graz, Weinzöttlstraße 8. 8051 Graz, Wiener Str. 196. 8054 Graz, Kärntner Str. 328. 8054 Seiersberg-Pirka, Feldkirchner Straße 9. 8055 Graz, Puchstr. 199. 8112 Gratwein, Murfeldstr. 1. 8200 Gleisdorf, Hartberger Straße 23. 8225 Pöllau, Bergwald 598. 8230 Hartberg-Ungarvorstadt, Ferdinand-Leihs-Str. 39. 8280 Fürstenfeld, Ledergasse 17. 8330 Feldbach, Gleichenberger Str. 66. 8401 Kalsdorf, Kalsdorfer Ring 1. 8430 Leibnitz, Wasserwerkstr. 30c. 8472 Straß, Reichsstraße 74. 8490 Bad Radkersburg, Kurhausstraße 4. 8530 Deutschlandsberg, Frauentaler Straße 73. 8570 Voitsberg, Conrad v. Hötzendorfstr. 51. 8580 Köflach, Josef-Gauby-Str. 1. 8600 Bruck an der Mur, Leobner Str. 19. 8605 Kapfenberg, Bachgasse 4b. 8670 Krieglach, Hofackerstr. 2. 8680 Mürzzuschlag, Grazer Str. 79E. 8700 Leoben, Kärntner Str. 315. 8700 Leoben, Kärntner Str. 89. 8720 Knittelfeld, Wiener Straße 25. 8740 Zeltweg, Bundesstr. 22. 8753 Fohnsdorf, Arena am Waldfeld 8. 8793 Trofaiach, Langefelderstr. 1. 8940 Liezen, Gesäusestr. 2. 8970 Schladming, Gewerbestraße 687. 9020 Klagenfurt-Welzenegg, Pischeldorferstr. 184. 9020 Klagenfurt, August-Jaksch-Str. 48. 9020 Klagenfurt, Ebentalerstr. 164. 9020 Klagenfurt, Flatschacher Str. 191. 9100 Völkermarkt, Umfahrungsstr. 4. 9141 Eberndorf, An der Bundesstr. 6 (B 82). 9241 Wernberg, Industriestr. 2. 9300 St. Veit a. d. Glan, Lastenstr. 9. 9330 Althofen, Eisenstraße 46. 9400 Wolfsberg, Auenfischerstraße 38. 9400 Wolfsberg, Spanheimerstr. 19. 9500 Villach, Badstubenweg 89. 9500 Villach, Klagenfurter Str. 70. 9560 Feldkirchen in Kärnten, Ossiacher Bundesstraße 6. 9601 Arnoldstein, Kärntner Str. 75. 9710 Feistritz an der Drau, Villacher Str. 456. 9800 Spittal an der Drau, Koschatstraße 39. 9813 Lurnfeld/ Möllbrücke, Altenmarkt 24. 9900 Lienz, Kärntner Straße 63.''',
                   #   'content': 'In der Klederinger Straße ist eine Baustelle.',
                  'content': '''Erneut wurde in Linz ein Zigarettenautomat, vermutlich durch einen pyrotechnischen Satz, aufgesprengt. Ein Zeuge beobachtete gegen 1.15 Uhr mehrere Personen, die in der Nähe des Automaten im Bereich Laaer-Berg-Straße im 10. Bezirk gewesen sein sollen. Anschließend hörte er einen lauten Knall und verständigte umgehend die Polizei. Die unbekannten Tatverdächtigen konnten mit Zigarettenpackungen und Bargeld die Flucht ergreifen. Die Polizei leitete umgehend eine Fahndung nach den Personen ein, bisher ohne Erfolg. Zigarettenautomat in Urfahr gesprengt. Erst vor wenigen Tagen hatten unbekannte Personen einen Zigarettenautomaten in der Prager Straße in Urfahr gesprengt . Auch dort verwendeten die Täter Pyrotechnik als Sprengmittel. Es wurden sowohl Bargeld in unbestimmter Höhe als auch eine unbestimmte Menge an Zigarettenpackungen gestohlen. wil 13.12.2020, 10:04 |. Akt: 13.12.2020, 10:34.''',
                  # 'content': '''Beiträge zum Thema Linie U2. U2-Ausbau und neue Linie U5. U-Bahn-Bau soll im Jänner starten. Der Baustart für die neuen Strecken der U2 und der geplanten Linie U5 hat sich verzögert. Nun ist es aber soweit: "Wir wollen noch im Jänner mit den Bauarbeiten starten", heißt es von den Wiener Linien. WIEN. Die Neuorganisation der U-Bahn-Linien im innerstädtischen Bereich mit dem Ausbau der U2 und der Einführung der U5 ist das wahrscheinlich grö´ßte Infrastruktur-Projekt der Stadt. Die Vorarbeiten haben längst begonnen, bei der U4-Station Pilgramgasse und im Bereich Matzleinsdorfer Platz... Wiener Linien. Störungen bei U2 und 70A. Wegen einer Signalstörung am Karlsplatz fährt die U2 derzeit nur zwischen Seestadt und Schottentor. Wegen einer Signalstörung im Stationsbereich Karlsplatz fährt die Linie U2 nur zwischen den Stationen Seestadt und Schottentor. Die Techniker der Wiener Linien arbeiten daran, das Problem zu beheben. Das Störungsende ist derzeit nicht absehbar, wird aber voraussichtlich bis in die Mittagsstunden andauern. Als Ersatz können die U-Bahn-Linien U1 und U3 sowie die Straßenbahnlinien 1, 2,... Zwischen Karlsplatz und Längenfeldgasse. Im Juli und August ist die U4 teilweise gesperrt. Teilsperre: In den Sommermonaten fährt die U4 nicht zwischen Karlsplatz und Längenfeldgasse. WIEDEN/MARGARETEN. Seit Jänner ist die U4-Station Pilgramgasse gesperrt. Grund dafür ist der Bau der neuen Linien U2 und U5. Im Zuge dessen wird auch die U-Bahnlinie U4 bis 2024 generalsaniert. Viele der Arbeiten konnten bereits während dem laufenden Betrieb durchgeführt werden, heißt es von den Wiener Linien. Für die Modernisierung ist nun jedoch eine Teilsperre während der Sommermonate... Infoabend rund um U2 und U5. Was bedeutet der U-Bahn-Bau für die Josefstadt? Beim Einkaufsstraßenverein "cross 8" informierte man über die anstehenden Bauarbeiten von U2 und U5. JOSEFSTADT. Wie es mit dem Bau der U2 und der U5 in der Josefstadt weitergeht? Um Fragen dazu zu beantworten und auch der Bevölkerung Ängste zu nehmen, lud der Einkaufsstraßenverein "cross 8" zum Infoabend ein. Mit dabei: Bezirksvorsteherin Veronika Mickel-Göttfert (ÖVP) und Vertreter der Wiener Linien. Während der nächsten acht Jahre wird im 8. Bezirk gebaut. Die Fertigstellung der neuen... 1 5 11. Schöne Ausblicke. aus der U-Bahn (U2) unterwegs in die Seestadt Aspern... 1 3 2. Linie U2 und U5: Bezirk Neubau informierte Anrainer über Ausbau. Von 13A-Route bis zur drohenden Parkplatz-Not: Bei der Infoveranstaltung auf Initiative des Bezirks zum Ausbau der Linie U2 wurde viel diskutiert. NEUBAU. "Ich höre die Botschaft, aber ich glaube sie nicht." Das Zitat eines Anrainers bei der U2-Infoveranstaltung könnte passender nicht sein. Viel wurde von Seiten des Bezirks, der Stadt und der Wiener Linien versucht, um die Aufregung rund um den U2-Ausbau zu nehmen. Die Skepsis der Neubauerinnen und Neubauer aber bleibt. Waren es bei der... Linie U2 und U5: Neubau informiert Anrainer über Ausbau. Am 15. Februar findet in der Bezirksvorstehung Neubau eine eigene Informationsveranstaltung zum U-Bahn-Ausbau statt. Auch die ersten Vorarbeiten für das Bauprojekt laufen bereits. Diejenigen, die in der Zollergasse oder Mondscheingasse wohnen, werden es wohl als erstes merken: Langsam, aber sicher starten die Vorarbeiten für den U2-Ausbau. Recht spektakulär ist dies – derweil – noch nicht: Es handelt sich dabei nämlich lediglich um so genannte "Einbauten-Umlegungen". Sprich: Kabel für... Brunnen für die U-Bahn: Details zu den Bauarbeiten an U2 und U5. Die Vorbereitungen für die U2 und U5 laufen auf Hochtouren. Ein Überblick zum aktuellen Stand der Arbeiten. Auch wenn es vielen nicht so vorkommt, tut sich beim U-Bahn-Ausbau doch so einiges. Denn: 2018 soll der Bau beginnen. Rund eine Milliarde Euro wird die erste Ausbaustufe kosten. Bis die U5 dann den Elterleinplatz und die U2 den Wienerberg erreicht, müssen sich die Öffi-Fahrgäste freilich noch gedulden: Frühestens 2020 sollen die Bauarbeiten für diese, zweite Strecke starten. Beim... 5 1 3. Lärmqualen an der Ausstellungsstraße. Die U2 hält die Anrainer nachts wach. Sie fordern einen Schallschutz. Ohrenbetörender Lärm dringt alle drei bis fünf Minuten aus einem Notausstieg der U2 in der Ausstellungsstraße in der Leopoldstadt. Lärm, den es zwar schon seit der Eröffnung der U2-Verlängerung vor nunmehr mehr als fünf Jahren gegeben hat, der aber seit der Eröffnung der Prater Hochgarage auf dem Geländer der ehemaligen Bierinsel unerträglich geworden ist. Mauer als Verstärker Der Grund: Die Schallwellen werden jetzt...''',
                  # 'content': '''Nach mehr als zwei Jahren Bauzeit sind die Umbauarbeiten und Modernisierungen am Bahnhof Braunau nun endgültig abgeschlossen. Die kundenrelevanten Anlagen sind seit Mitte November in Betrieb. BRAUNAU. 31 Millionen investierten das Land Oberösterreich , die ÖBB und die Stadtgemeinde Braunau gemeinsam in die Modernisierung des Braunauer Bahnhofes. Entstanden ist ein moderner, barrierefreier Bahnhof inklusive Busterminal sowie Park&Ride- und Bike&Ride-Anlage. Außerdem wurde eine Geh- und Radwegunterführung mit Liftanlagen und niveaugleiche Bahnsteige errichtet. Alle kundenrelevanten Anlagen sind bereits seit Mitte November in Betrieb. Alles neu am Braunauer Bahnhof. Die alten Bahnsteige wurden durch einen Inselbahnsteig und einen Hausbahnsteig direkt vom Aufnahmegebäude ersetzt. Außerdem wurden die Bahnsteige teils überdacht. Am Inselbahnsteig wurde eine verglaste Wartekoje errichtet. Ein Blindenleitsystem soll blinden und sehbehinderten Menschen die Orientierung am Bahnhof wesentlich erleichtern. Über Informationssystem wie Monitore und Lautsprecher werden die Zugzeiten in Echtzeit übertragen. Das Bahnhofsgebäude, der Wartebereich und die WC-Anlagen wurden modernisiert. Am Bahnhofsvorplatz befindet sich nun das Busterminal. Eine Unterführung für Fußgänger und Radfahrer stellt eine Verbindung zwischen Bahnhof und dem Stadtteil Laab dar. Auch die Park&Ride-Anlage mit 158 Pkw-Stellplätzen und die Bike&Ride-Anlage, die Stellplatz für 90 Räder und zehn Mopeds bietet, ist barrierefrei erreichbar. "Der Bahnhof Braunau ist ein wesentliches Element des Regionalverkehrskonzeptes Innviertel. Daher hat das Land Oberösterreich einen großen Beitrag geleistet, um den Bahnhof Braunau in Verbindung mit dem neuen Busterminal und der P&R-Anlage zu einer der modernsten Verkehrsdrehscheiben des Innviertels umzubauen. Denn multimodale Verkehrsknoten schaffen die notwendigen Verknüpfungspunkte für die Fahrgäste. Busterminals und P&R-Anlagen an den Bahnhöfen erleichtern den Umstieg und ein klar verbesserter Fahrplan schafft neue und bessere Verbindungen. Der modernisierte Bahnhof Braunau bringt eine klare Verbesserung für die Region", betont Oberösterreichs Infrastrukturlandesrat Günther Steinkellner. Für mehr Sicherheit. Im Zuge der Umbauarbeiten wurden die beiden Eisenbahnkreuzungen Josef Reiter-Straße und der Bahnweg aufgelassen. 2018 wurde an der Josef Reiter-Straße bereits eine Unterführung errichtet. Für die Eisenbahnkreuzung am Bahnweg dient die neue Geh- und Radwegunterführung als Ersatz. Die Eisenbahnkreuzung an der Laabstraße wurde für den Straßenverkehr technisch modernisiert und neu gestaltet. Außerdem hat die Stadtgemeinde Braunau mit einem neuen elektronischen Stellwerk die modernste Sicherungstechnik für den Bahnverkehr erhalten: Dieses steuert die Weichen und Signale und sorgt somit für zuverlässige, automatische Betriebsabläufe. Die Fahrgäste profitieren von pünktlicheren Zügen und erhalten in Echtzeit Informationen zu ihren Zugzeiten. "Die Arbeitswelt wird flexibler und die Menschen sind immer mobiler. Mit dem neuen Bahnhof Braunau ist unser Standort noch attraktiver. Braunau hat nicht nur eine moderne Verkehrsdrehscheibe bekommen, von der die Braunauer Bevölkerung und insbesondere Schülerinnen und Schüler der Region profitieren. Der Umbau hat auch die Sicherheit auf der Straße massiv erhöht", freut sich Braunaus Bürgermeister Johannes Waidbacher über den Neubau.''',
                  # 'content': '''Es ist ein Sinnbild für die Bezirkspolitik der vergangenen Jahrzehnte. Die Wiener Lerchenfelder Straße dient als Grenze zwischen siebten und achten Gemeindebezirk. Und sie bildet eine Trennlinie, an der sich sehr deutlich der Unterschied einer rund 20-jährigen grünen Bezirksvorstehung zur türkisen – lange schwarzen – zeigt. Folgt man der Lerchenfelder Straße stadtauswärts, säumen links – auf der Seite des Siebenten – Bäume den Weg, rechts liegen Parkplätze, Grün findet man im Teil der Josefstadt nur in Blumenhandlungen. An Fußgängern rauschen auch in Zeiten des Lockdowns Autos, Straßenbahnen und Radfahrer vorbei. Es ist laut: Bims klingeln bei den Stationen, Mopeds und Autos lassen an der Ampel ihre Motoren aufheulen. Die Lärmkarte des Umweltministeriums weist die Lerchenfelder Straße als lauteste Straße im siebten Bezirk aus. Mit mehr als 75 Dezibel liegt sie in derselben Kategorie wie der Gürtel. Denn wenn es schnell raus aus der oder rein in die City gehen soll, weicht der Verkehr von Neubau nach Lerchenfeld aus. Schließlich gilt im Siebenten auf den Verkehrsadern, die Ring und Gürtel verbinden, Tempo 30. Nur wenige Meter weiter nördlich kommt man mit 50 Stundenkilometern weit flotter voran. Bis zu 9000 Kfz werden laut Bezirk pro Tag gezählt. Türkis wird Grün. Dieses Bild soll bald der Vergangenheit angehören. Mit Martin Fabisch wurde im Oktober ein grüner Bezirksvorsteher für den Achten gewählt. Er löst die türkise Bezirkschefin Veronika Mikl ab. Im Wahlkampf erregte sein Team mit einem Projekt besonderes Aufsehen: der Umgestaltung der Josefstädter Straße in eine Begegnungszone. Wenige Wochen nach der Wahl hat Fabisch gemeinsam mit seinem Parteikollegen, dem Neubauer Bezirksvorsteher Markus Reiter, weitere, die beiden Stadtteile vereinende Pläne geschmiedet: Die Lerchenfelder Straße soll umgestaltet werden. Es brauche mehr Aufenthaltsqualität, Platz für Radler und Fußgänger. Kurz: Verkehrsberuhigung. Trennlinie soll verbinden. "Die Trennlinie der beiden Bezirke soll eine Verbindung werden", betont Fabisch: "Wir haben jetzt die Chance, eine starke Allianz innerhalb des Gürtels zu schmieden." Die Coronavirus-Krise habe gezeigt, wie wichtig hochwertig gestalteter, öffentlicher Raum sei, wo Platz zum Flanieren ist. Ziel sei es, so die lokale Wirtschaft zu stärken und die Lebensqualität der Bewohner zu erhöhen. Jeweils rund 2000 Bewohner zählt die Lerchenfelder Straße auf ihren zwei Bezirksseiten. Im ersten Schritt wolle man auf Begrünung der Straße setzen. "Wir haben diesbezüglich im Achten ein sichtbares Defizit gegenüber dem Siebenten", sagt Fabisch. Und: Beide Bezirksparlamente haben sich für die Reduzierung auf Tempo 30 ausgesprochen – nicht nur in Lerchenfeld: "Flächendeckend Tempo 30 im achten Bezirk" – das will der designierte Bezirksvorsteher Fabisch. Bauliche Maßnahmen. In einem zweiten Schritt sollen auch bauliche Maßnahmen gesetzt werden. Von 2004 auf 2018 stieg die Zahl der Passanten – laut einer Bezirkszählung –, die sich an einem Samstag auf der Lerchenfelder Straße aufhielten, von 3000 auf 5000 Personen. Die Gehsteige sollen darum breiter werden, kühlende Maßnahmen Einzug halten. In den kommenden zwei Jahren müsste dann die Infrastruktur erneuert und die Straße aufgegraben werden. "Wiener Wasser wird kommen, wir können davon ausgehen, dass sich auch andere Projekte der Daseinsvorsorge dem anschließen", sagt Reiter: "Das gibt uns die Chance, mutige Schritte zu setzen." Denn genau für diese "mutige Politik", sagt Reiter, sei er auch als Bezirkschef bestätigt worden. In Neubau konnten die Grünen nicht nur das beste Bezirksergebnis einfahren, sondern auch auf Stadt-Ebene. Wie diese aussehen könnten? Die Lieblingsvariante der zwei Bezirkschefs ist eine Begegnungszone – zumindest in einem Teil der Lerchenfelder Straße. Gleiches fordert bereits eine Bürgerinitiative. Starten könnte die verkehrsberuhigte Zone nach dem Vorbild der Wiener Mariahilfer Straße auf Höhe der Langegasse (achter Bezirk). Enden sollte sie an der Ecke Neubaugasse (siebenter Bezirk). Beide Quergassen sind bereits zum Teil Begegnungszonen. Jene in der Neubaugasse soll im nächsten Jahr bis zur Lerchenfelder Straße verlängert werden. Stadt und Bezirk. Nach dem Koalitionsende auf Stadtebene stelle sich auch die Frage, "was der Beitrag der Grünen in den kommenden fünf Jahren ist", sagt Reiter. In den von den Grünen regierten Bezirken könne man der Bevölkerung zeigen, dass, "wenn Grüne regieren, sie viel voranbringen und umsetzen", sagt Reiter. (Oona Kroisleitner, 26.11.2020).''',
                  # 'conteWaidhausenstraßent': '''Ein Augenzeuge berichtet, dass es in einem Haus in der Obere Bahngasse in Wien binnen 24 Stunden gleich mehrmals brannte. Am Samstag um etwa 10.30 Uhr wurde die Feuerwehr zu einem Kellerbrand in einem Gebäude in der Oberen Bahngasse, im 3. Bezirk. Laut einem Augenzeugen war dies bereits das dritte Feuer binnen eines Tages in dem Haus. Die Polizei bestätigt nun gegenüber oe24, dass es dort sogar zu vier Einsätzen binnen 24 Stunden kam. Die Brandermittler des Landeskriminalamtes haben die Ermittlungen übernommen. Die Feuerwehr bekämpfte das Feuer am Samstag unter Atemschutz. Das Gebäude musste evakuiert werden. Da Samstagvormittag und -mittag besonders viele Bewohner zuhause waren, schickte die Feuerwehr mehr Einsatzwägen als sonst. Laut Feuerwehrsprecher wurde niemand verletzt. Die Einsatzkräfte sind mit den Nachlöscharbeiten beschäftigt. Der Augenzeuge berichtet, dass es in jenem Gebäude auch im vergangenen Jahr öfter gebrannt hatte.''',
                  # 'content': 'In der Mariahilfer Str. 20 in Wien ist nach einem Unfall die rechte Fahrspur gesperrt.',
                  # 'content': 'In der Guffertstraße ist ab dem 25. Januar 2021 eine Baustelle.',
                   u'format': u'text/html',
                   u'header': {},#
                   u'id': u'1000',
                   u'lang': u'DE',
                   u'nilsimsa': u'00FC4CB928D78CB770521A11DFDE0923DC3C19 E1642274E6AC7C06650B80E6ED',
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



if __name__ == '__main__':
    unittest.main()
