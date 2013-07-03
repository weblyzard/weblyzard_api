#!/usr/bin/python
# -*- coding: utf8 -*-
'''
Created on Jan 4, 2013

moduleauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>

New supported calls:
- recognize/focus?profiles=ofwi.people&profiles=ofwi.organizations.context
- recognize/searchXml/ofwi.people

'''

from eWRT.ws.rest import RESTClient
from unittest import main, TestCase
from os import getenv

from weblyzard_api.xml_content import XMLContent

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
        url += '/recognize/rest/recognize'
        RESTClient.__init__(self, url, usr, pwd)

    def list_profiles(self):
        ''' pre-loaded profiles
            e.g. [u'Cities.DACH.10000.de_en', u'People.DACH.de']
        '''
        return self.execute("list_profiles")

    def list_configured_profiles(self):
        ''' profiles supported in the current configuration '''
        return self.execute("list_configured_profiles")

    def add_profile(self, profile_name, force=False):
        ''' pre-loads the given profile '''
        if profile_name in self.list_profiles() and not force:
            return
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
            self.add_profile(profile_name)
        query_parameters =  {'rescore': max_entities, 'buckets': buckets, 'limit': limit, 'wt': output_format }
        return self.execute("search", profile_name, text, query_parameters=query_parameters)

    def search_documents(self, profile_name, doc_list, debug=False, max_entities=1, buckets=1, limit=1, output_format='minimal'):
        '''
        :param profileName: the profile to search in
        :param doc_list: a list of documents to analyze in one of the 
                         following formats:
                         (a) dict: ( {'content_id': 12, 
                                      'content': u'the text to analyze'})
                         (b) weblyzardXML: ( XMLContent('<?xml version="1.0"...').as_list(),
                                             XMLContent('<?xml version="1.0"...').as_list(), )

        :param debug: compute and return an explanation
        :param buckets: only return n buckets of hits with the same score
        :param max_entities: number of results to return (removes the top hit's
                             tokens and rescores the result list subsequently
        :param limit: only return that many results
        :param output_format: the output format to use ('standard', 'minimal'*, 'annie')
        :rtype: the tagged dictionary
        '''
        assert output_format in self.OUTPUT_FORMATS
        if not doc_list:
            return 

        if 'content_id' in doc_list[0]:
            search_command = 'searchDocuments'
            content_type = 'application/json'
        elif 'id' in doc_list[0]:
            search_command = 'searchXmlDocuments'
            content_type = 'application/json'
        else:
            raise ValueError("Unsupported input format.")

        if not profile_name in self.list_profiles():
            self.add_profile(profile_name)
        query_parameters = { 'rescore': max_entities, 'buckets': buckets, 'limit': limit, 'wt':output_format }
        return self.execute(search_command, profile_name, doc_list, 
                            query_parameters=query_parameters, 
                            content_type=content_type)
    
    def get_focus(self, profile_names, doc_list):
        ''' 
        Returns the focus and annotations of the given document 

        :param profile_names: a list of profile names
        :param doc_list: a list of documents to analyze based on the weblyzardXML format

        query: recognize/focus?profiles=ofwi.people&profiles=ofwi.organizations.context
        '''
        assert( isinstance(profile_names, list) or isinstance(profile_names, tuple) )
        if not doc_list:
            return
        elif 'id' not in doc_list[0]:
            raise ValueError("Unsupported input format.")

        profile_name = '?profiles=' + '&profiles'.join(profile_names)
        return self.execute('focus', profile_name, doc_list)

    def status(self):
        return self.execute('status')


class EntityLyzardTest(TestCase):

    DOCS = [
            XMLContent(
            """<?xml version="1.0" encoding="UTF-8"?> <wl:page xmlns:wl="http://www.weblyzard.com/wl/2013#" xmlns:dc="http://purl.org/dc/elements/1.1/" wl:id="www.awp.ch/msg/20100831000483" dc:format="text/html" xml:lang="de" wl:nilsimsa="73bc3a300602edc022682a717af9b9e015af88d1411373e59c334b9aca36d26d" dc:title="" date="201008310900" teledata_id="18180">\n  <wl:sentence wl:pos="( NN ADV VVFIN APPR NN APPR ART ADJA NN KON APPR ADJA NN APPRART NN ) NE $( ART NN NE VMFIN ART ADJA NN APPRART ADJA NN CARD APPR ADV APPR NN VVINF $." wl:token="0,1 1,8 9,21 22,29 30,32 33,40 41,43 44,47 48,57 58,67 68,71 72,74 75,82 83,91 93,96 97,105 105,106 107,112 114,115 116,119 120,127 128,134 135,141 142,145 146,159 160,166 167,169 170,176 177,185 186,190 191,193 195,199 200,203 204,219 220,226 226,227" wl:id="6fbbd8032f0d722b0cbcbb5490e77fcc"><![CDATA[(Meldung insbesondere erg\xc3\xa4nzt um Angaben zu den laufenden Projekten und um weitere Aussagen  zum Ausblick) Basel  - Die Warteck Invest konnte den betrieblichen Ertrag im ersten Halbjahr 2010 in  etwa auf Vorjahresniveau halten.]]></wl:sentence>\n  <wl:sentence wl:pos="APPR ART ADJA $, APPR NN APPR NN ADJA NN VVFIN ADV ART ADJA NN $." wl:token="0,8 9,14 15,22 22,23 24,27 28,36 37,40 41,63 65,74 75,95 96,107 108,118 119,122 123,129 130,144 144,145" wl:id="60b7482cdb8dfc0d4f943859cff84be9"><![CDATA[Aufgrund eines starken, von Gewinnen aus Liegenschaftsverk\xc3\xa4ufen  gepr\xc3\xa4gten Vorjahresergebnisses resultierte allerdings ein klarer Gewinnr\xc3\xbcckgang von 10 Millionen CHF.]]></wl:sentence>\n</wl:page>""").as_dict()
               ]
     
    def test_entity_lyzard(self):
        docs = [ 
                 {'content_id': '12', 'content': u'Franz Klammer fährt Ski'}, 
                 {'content_id': '13', 'content' :u'Peter Müller macht Politik',} 
               ]

        e = Recognize()
        print e.list_profiles()
        e.add_profile('People.DACH.de')
        print e.search_documents('People.DACH.de', docs)

    def test_search_xml(self):
        e = Recognize()
        e.add_profile('People.DACH.de')
        print 'xmlsearch::::',e.search_documents('People.DACH.de', self.DOCS)

    def test_focus_search(self):
        e = Recognize()
        e.add_profile('People.DACH.de', 'extras.com.weblyzard.backend.recognize.extras.DataTypeProfile')
        result =  e.get_focus(['People.DACH.de', ], self.DOCS)
        print 'xmlfocus:::', result
        assert u'focus' in result[0]
        assert u'annotations' in result[0]
        

if __name__ == '__main__':
    main()

