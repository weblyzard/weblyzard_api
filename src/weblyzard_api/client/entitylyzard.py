#!/usr/bin/python
# -*- coding: utf8 -*-
'''
Created on Jan 4, 2013

@author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''

from eWRT.ws.rest import RESTClient
from unittest import main, TestCase

JEREMIA_URL = "http://localhost:8080/entityLyzard"

class EntityLyzard(RESTClient):
    '''
    EntityLyzard Web Service
    '''
    def __init__(self, url=JEREMIA_URL, usr=None, pwd=None):
        RESTClient.__init__(self, url, usr, pwd)

    def list_profiles(self):
        """ pre-loaded profiles
            e.g. [u'Cities.DACH.10000.de_en', u'People.DACH.de']
        """
        return self.execute("list_profiles")

    def list_configured_profiles(self):
        """ profiles supported in the current configuration """
        return self.execute("list_configured_profiles")

    def add_profile(self, profile_name):
        """ pre-loads the given profile """
        return self.execute("add_profile", profile_name)

    def remove_profile(self, profile_name):
        """ removes a profile from the list of pre-loaded profiles """
        return self.execute("remove_profile", profile_name)

    def search(self, profile_name, text):
        return self.execute("/minimalSearch/", profile_name, text)

    def search_documents(self, profile_name, doc_list):
        return self.execute("searchDocuments", profile_name, doc_list)
    
    def annie_search(self, profile_name, doc_list):
        """ Returns the ANNIE annotations for the given documents
        @param profile_name: the name of the matching profile to use
        @param doc_list: a list of document objects
        """
        return self.execute("annieSearchDocuments", profile_name, doc_list)
        
    def status(self):
        return self.execute('status')


class EntityLyzardTest(TestCase):
    
    def test_entity_lyzard(self):
        docs = [ 
                 {'id': '12', 'content': u'Franz Klammer fährt Ski'}, 
                 {'id':'13', 'content' :u'Peter Müller macht Politik',} 
               ]

        e = EntityLyzard()
        print e.list_profiles()
        e.search_documents("People.DACH.de", docs)
        

if __name__ == '__main__':
    main()

