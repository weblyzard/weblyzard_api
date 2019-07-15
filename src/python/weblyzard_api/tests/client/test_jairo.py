#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
.. codeauthor:: Max Goebel <goebel@weblyzard.com>
'''
from __future__ import print_function
from __future__ import unicode_literals
import unittest

from weblyzard_api.client.jairo import JairoClient


class JairoTest(unittest.TestCase):

    SERVICE_URL = 'localhost:63005/rest'

    PROFILES = {
        #         "geonames.seeAlso.wikidata": {
        #             "types": {
        #                 "?entity": "entity"
        #             },
        #             "sparqlEndpoint": "http://gecko9.wu.ac.at:3031/wikidata.20180215/query",
        #             "query": "PREFIX wdt: <http://www.wikidata.org/prop/direct/> SELECT ?entity WHERE { ?entity wdt:P1566 ?geo_id .\n                FILTER (?geo_id = \"<key>\")\n                }"
        #         },
        #         "wikidata_label": {
        #             "types": {
        #                 "?label": "label"
        #             },
        #             "sparqlEndpoint": "http://gecko9.wu.ac.at:3031/wikidata.20180215/query",
        #             "query": "\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\nPREFIX skos: <http://www.w3.org/2004/02/skos/core#>\nPREFIX skbprop: <http://weblyzard.com/skb/property/>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\nPREFIX lang: <http://id.loc.gov/vocabulary/iso639-1/>\nPREFIX dbo: <http://dbpedia.org/ontology/>\nPREFIX schema: <http://schema.org/description>\nPREFIX skbkwfr: <http://weblyzard.com/skb/keyword/fr#>\nPREFIX skbentity: <http://weblyzard.com/skb/entity/>\nPREFIX skblex: <http://weblyzard.com/skb/lexicon/>\nPREFIX agent: <http://weblyzard.com/skb/entity/agent/>\nPREFIX wdt: <http://www.wikidata.org/prop/direct/>\nPREFIX dc: <http://purl.org/dc/elements/1.1/>\nPREFIX lemon: <http://lemon-model.net/lemon#>\nPREFIX skbkwde: <http://weblyzard.com/skb/keyword/de#>\nPREFIX geo: <http://www.opengis.net/ont/geosparql#>\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\nPREFIX skbkwes: <http://weblyzard.com/skb/keyword/es#>\nPREFIX prov: <http://www.w3.org/ns/prov#>\nPREFIX lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#>\nPREFIX owl: <http://www.w3.org/2002/07/owl#>\nPREFIX gn: <http://sws.geonames.org>\nPREFIX dct: <http://purl.org/dc/terms/>\nPREFIX wd: <http://www.wikidata.org/entity/>\nPREFIX skbkwen: <http://weblyzard.com/skb/keyword/en#> \n\nSELECT ?label WHERE { \n <key> rdfs:label ?label . \n\n    FILTER(!isLiteral(?label)\n           || lang(?label) = \"\"\n           || lcase(lang(?label)) IN (\"en\", \"zh\", \"ar\", \"ru\", \"de\", \"fr\", \"es\", \"pt\", \"it\", \"nl\", \"en-gb\", \"en-us\")\n          )\n        \n}"
        #         }
        #         'dbpedia_person_en': {
        #             "sparqlEndpoint":     "http://dbpedia.org/sparql/",
        #             "types": {"?abstract":    "abstract",
        #                       "?sameas":    "sameas",
        #                       "?seeAlso":    "seeAlso"},
        #             "query": """PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        #                                 PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        #                                 PREFIX skbprop: <http://weblyzard.com/skb/property/>
        #                                 PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        #                                 PREFIX lang: <http://id.loc.gov/vocabulary/iso639-1/>
        #                                 PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        #                                 PREFIX : <http://weblyzard.com/skb/lexicon/>
        #                                 PREFIX prov: <http://www.w3.org/ns/prov#>
        #                                 PREFIX lemon: <http://lemon-model.net/lemon#>
        #                                 PREFIX lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#>
        #                                 PREFIX dc: <http://purl.org/dc/elements/1.1/>
        #                                 PREFIX dct: <http://purl.org/dc/terms/>
        #                                 PREFIX dbo: <http://dbpedia.org/ontology/>
        #                                 PREFIX owl: <http://www.w3.org/2002/07/owl#>
        #                                 PREFIX geo: <http://www.opengis.net/ont/geosparql#>
        #                                 SELECT ?sameas ?abstract ?seeAlso WHERE {
        #                                 <key> owl:sameAs ?sameas .
        #                                 <key> dbo:abstract ?abstract .
        #                                 <key> rdfs:seeAlso ?seeAlso . FILTER (lang(?abstract) = 'en')}"""},
        #         'test_dbpedia_geo': {
        #             "sparqlEndpoint": "http://dbpedia.org/sparql",
        #             "types": {
        #                 "?preferredName": "preferredName",
        #                 "?parentCountry": "parentCountry",
        #                 "?latitude": "latitude",
        #                 "?longitude": "longitude"
        #             },
        #             "query": """PREFIX dbo: <http://dbpedia.org/ontology/>
        #                                 PREFIX geo: <http://www.opengis.net/ont/geosparql#>
        #                                 PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        #                                 SELECT ?preferredName ?latitude ?longitude ?parentCountry WHERE {
        #                                 <key> rdfs:label ?preferredName; geo:lat ?latitude; geo:long ?longitude .
        #                                 OPTIONAL { <key>  dbo:country ?parentCountry } .}"""
        #         }
    }

    def setUp(self):
        self.client = JairoClient(url=self.SERVICE_URL)
        self.set_profiles()

    def test_service(self):
        ''' test status of the Jairo service. '''
        print(self.client.status())
        assert 'processedDocuments' in self.client.status()

    def set_profiles(self):
        ''' test setting a profile on the Jairo service. '''
        for profile_name, profile in list(self.PROFILES.items()):
            self.client.set_profile(
                profile_name=profile_name, profile=profile)

            assert profile_name in self.client.list_profiles()

    def test_entity_extension_bad_result_token(self):
        ''' test entity extension of the Jairo service. '''
#         profile_name = 'dbpedia_person_en'
#         input_annotations = [
#             {
#                 "start": 0, "end": 3,
#                 "key": "<http://dbpedia.org/resource/Sophie_Scholl>"
#             },
#             #             {
#             #                 "start": 7, "end": 13,
#             #                 "key": "<http://dbpedia.org/resource/Switzerland>"
#             #             }
#         ]
#         profile_name = 'geonames.seeAlso.wikidata'
#         input_annotations = [{'key': u'2963597'}]
#         result = self.client.enrich_annotations(profile_name=profile_name,
#                                                 annotations=input_annotations)
        from pprint import pprint
#         pprint(result)

        profile_name = 'wikidata_label'
        input_annotations = [{'key': u'<http://www.wikidata.org/entity/Q40>'},
                             {'key': u'<http://www.wikidata.org/entity/Q214>'}]
        result = self.client.enrich_annotations(profile_name=profile_name,
                                                annotations=input_annotations)
        pprint(result)
        assert len(result)


if __name__ == '__main__':
    unittest.main()
