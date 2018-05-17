#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
.. codeauthor:: Max Goebel <goebel@weblyzard.com>
'''
import unittest

from weblyzard_api.client.jairo import JairoClient


class JairoTest(unittest.TestCase):

    SERVICE_URL = 'localhost:63005/rest'

    def setUp(self):
        self.client = JairoClient(url=self.SERVICE_URL)
        self.set_profile()

    def test_service(self):
        ''' test status of the Jairo service. '''
        print(self.client.status())
        assert 'processedDocuments' in self.client.status()

    def set_profile(self):
        ''' test setting a profile on the Jairo service. '''
        profile = {
            "sparqlEndpoint": "http://dbpedia.org/sparql",
            "types": {
                "?preferredName": "preferredName",
                "?parentCountry": "parentCountry",
                "?latitude": "latitude",
                "?longitude": "longitude"
            },
            "query": "PREFIX dbo: <http://dbpedia.org/ontology/>\nPREFIX geo: <http://www.opengis.net/ont/geosparql#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\nSELECT ?preferredName ?latitude ?longitude ?parentCountry WHERE {  <key> rdfs:label ?preferredName; geo:lat ?latitude; geo:long ?longitude . OPTIONAL { <key>  dbo:country ?parentCountry } .}"
        }

        self.client.set_profile(profile_name='test_profile', profile=profile)

        assert 'test_profile' in self.client.list_profiles()

    def test_entity_extension(self):
        ''' test enitity extension of the Jairo service. '''
        input_annotations = [
            {
                "start": 0, "end": 3,
                "key": "<http://dbpedia.org/resource/Barack_Obama>"
            },
            {
                "start": 7, "end": 13,
                "key": "<http://dbpedia.org/resource/Switzerland>"
            }
        ]
        result = self.client.enrich_annotations(profile_name='test_profile',
                                                annotations=input_annotations)
        print(result)
        assert len(result) == 2


if __name__ == '__main__':
    unittest.main()
