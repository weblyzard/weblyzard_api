#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
.. codeauthor:: Max Goebel <goebel@weblyzard.com>
'''
import unittest
from weblyzard_api.client.jairo import JairoClient

class JairoTest(unittest.TestCase):
    
    def setUp(self):
        self.client = JairoClient()
        
    def test_service(self):
        ''' test status of the Jairo service. '''
        print(self.client.status())
        assert 'processedDocuments' in self.client.status()
        
    def test_set_profile(self):
        ''' test setting a profile on the Jairo service. '''
        profile = {
         "sparqlEndpoint": "http://dbpedia.org/sparql",
         "types": {"?type": "type"},
         "query": "SELECT ?type WHERE { <key> rdf:type ?type }"
        }
        
        self.client.set_profile(profile_name='test_profile', profile=profile)
        
        assert 'test_profile' in self.client.list_profiles()
        
    def test_entity_extension(self):
        ''' test enitity extension of the Jairo service. '''
        input_annotations =  [  
                                {
                                    "start":0, "end": 3,  
                                    "key": "<http://dbpedia.org/resource/Barack_Obama>"
                                 },
                                 {
                                    "start":7, "end": 13, 
                                    "key": "<http://dbpedia.org/resource/Switzerland>"
                                 }
                              ]
        result = self.client.extend_annotations(profile_name='test_profile', 
                                                annotations=input_annotations)
        print(result)
        assert len(result) == 2
     
if __name__ == '__main__':
    unittest.main()   