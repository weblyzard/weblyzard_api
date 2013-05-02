#!/usr/bin/python
# -*- coding: utf8 -*-
'''
Created on Jan 4, 2013

moduleauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''

from eWRT.ws.rest import RESTClient
from unittest import main, TestCase
from os import getenv

WEBLYZARD_API_URL  = getenv("WEBLYZARD_API_URL") or "http://localhost:8080"
WEBLYZARD_API_USER = getenv("WEBLYZARD_API_USER")
WEBLYZARD_API_PASS = getenv("WEBLYZARD_API_PASS")

class Recognize(RESTClient):
    '''
    class:: Recognize 
    EntityLyzard/Recognize Web Service
    '''
    
    OUTPUT_FORMATS = ('standard', 'minimal', 'annie')    

    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER, pwd=WEBLYZARD_API_PASS):
        url += '/entityLyzard/rest/recognize'
        RESTClient.__init__(self, url, usr, pwd)

    def list_profiles(self):
        ''' pre-loaded profiles
            e.g. [u'Cities.DACH.10000.de_en', u'People.DACH.de']
        '''
        return self.execute("list_profiles")

    def list_configured_profiles(self):
        ''' profiles supported in the current configuration '''
        return self.execute("list_configured_profiles")

    def add_profile(self, profile_name):
        ''' pre-loads the given profile '''
        return self.execute("add_profile", profile_name)

    def remove_profile(self, profile_name):
        ''' removes a profile from the list of pre-loaded profiles '''
        return self.execute("remove_profile", profile_name)

    def search(self, profile_name, text, debug=False, max_entities=1, buckets=1, limit=1, output_format='minimal'):
        '''
        :param profileName: the profile to search in
        :param text: the text to search in
        :param debug: compute and return an explanation
        :param buckets: only return n buckets of hits with the same score
        :param max_entities: number of results to return (removes the top hit's
                             tokens and rescores the result list subsequently
        :param limit: only return that many results
        :param output_format: the output format to use ('standard', 'minimal'*, 'annie')
        :rtype: the tagged text
        '''
        assert output_format in self.OUTPUT_FORMATS
        if not profile_name in self.list_profiles():
            add_profile(profile_name)
        query_parameters =  {'rescore': max_entities, 'buckets': buckets, 'limit': limit, 'wt': output_format }
        return self.execute("search", profile_name, text, query_parameters=query_parameters)

    def search_documents(self, profile_name, doc_list, debug=False, max_entities=1, buckets=1, limit=1, output_format='minimal'):
        '''
        :param profileName: the profile to search in
        :param doc_list: a list of documents to analyze
        :param debug: compute and return an explanation
        :param buckets: only return n buckets of hits with the same score
        :param max_entities: number of results to return (removes the top hit's
                             tokens and rescores the result list subsequently
        :param limit: only return that many results
        :param output_format: the output format to use ('standard', 'minimal'*, 'annie')
        :rtype: the tagged dictionary
        '''
        assert output_format in self.OUTPUT_FORMATS
        if not profile_name in self.list_profiles():
            add_profile(profile_name)
        query_parameters = { 'rescore': max_entities, 'buckets': buckets, 'limit': limit, 'wt':output_format }
        return self.execute("searchDocuments", profile_name, doc_list, query_parameters=query_parameters)
    
    def status(self):
        return self.execute('status')


class EntityLyzardTest(TestCase):
    
    def test_entity_lyzard(self):
        docs = [ 
                 {'content_id': '12', 'content': u'Franz Klammer fährt Ski'}, 
                 {'content_id':'13', 'content' :u'Peter Müller macht Politik',} 
               ]

        e = Recognize()
        print e.list_profiles()
        e.add_profile('People.DACH.de')
        print e.search_documents("People.DACH.de", docs)
        

if __name__ == '__main__':
    main()

