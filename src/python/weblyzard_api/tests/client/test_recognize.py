#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Aug 29, 2016

'''
import unittest

from weblyzard_api.client.recognize import Recognize

class TestRecognize(unittest.TestCase):
 
    DOCS_XML = [
            '''
            <?xml version="1.0" encoding="UTF-8"?>
            <wl:page xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://www.weblyzard.com/wl/2013#" dc:title="" wl:id="99933" dc:format="text/html" xml:lang="de" wl:nilsimsa="030472f84612acc42c7206e07814e69888267530636221300baf8bc2da66b476" dc:related="http://www.heise.de http://www.kurier.at">
               <wl:sentence wl:id="50612085a00cf052d66db97ff2252544" wl:pos="NE NE VAFIN CARD NE NE VVPP $." wl:token="0,5 6,12 13,16 17,19 20,23 24,27 28,36 36,37" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[Georg Müller hat 10 Mio CHF gewonnen.]]></wl:sentence>
               <wl:sentence wl:id="a3b05957957e01060fd58af587427362" wl:pos="NN NE VMFIN APPR ART NN APPR CARD NE NE $, PRELS PPER NE NE VVFIN $, PIS VVINF $." wl:token="0,4 5,12 13,19 20,23 24,27 28,35 36,39 40,42 43,46 47,50 50,51 52,55 56,59 60,65 66,72 73,84 84,85 86,92 93,101 101,102" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[Herr Schmidt konnte mit dem Angebot von 10 Mio CHF, das ihm Georg Müller hinterlegte, nichts anfangen.]]></wl:sentence>
            </wl:page>
            ''',
            '''
            <?xml version="1.0" encoding="UTF-8"?>
            <wl:page xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://www.weblyzard.com/wl/2013#" dc:title="" wl:id="99934" dc:format="text/html" xml:lang="de" wl:nilsimsa="020ee211a20084bb0d2208038548c02405bb0110d2183061db9400d74c15553a" dc:related="http://www.heise.de http://www.kurier.at">
               <wl:sentence wl:id="f98a0c4d2ddffd60b64b9b25f1f5657a" wl:pos="NN NE VVFIN $, KOUS ART NN ADV CARD ADJD VAINF VAFIN $." wl:token="0,6 7,14 15,23 23,24 25,29 30,33 34,37 38,42 43,47 48,59 60,64 65,69 69,70" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[Rektor Kessler erklärte, dass die HTW auch 2014 erfolgreich sein wird.]]></wl:sentence>
            </wl:page>
            ''']
 
    
    #we need to get the recognize client twice (once here and once in setUp)
 
    TESTED_PROFILES = ['de.people.ng', 'en.geo.500000.ng', 'en.organization.ng', 'en.people.ng']
    IS_ONLINE = True
     
    def setUp(self):
        self.available_profiles = []
        #voyager.srv.weblyzard.net
        url = 'http://triple-store.ai.wu.ac.at:8080/recognize/rest/recognize'
        #url = 'localhost:8080/Recognize/rest'
        self.client = Recognize(url)
        self.service_is_online = self.client.is_online()
        if not self.service_is_online:
            print 'WARNING: Webservice is offline --> not executing all tests!!'
            self.IS_ONLINE = False
            return
             
        recognize_profiles = self.client.list_profiles()
        for profile in recognize_profiles:
            if profile in self.TESTED_PROFILES:
                self.available_profiles.append(profile)
  
        self.all_profiles = self.client.list_profiles()
        self.DOCS = [Recognize.convert_document(xml) for xml in self.DOCS_XML]
        

#     def test_adrian(self):
#  
#         from pprint import pprint
#          
#  
#         print "start"
#      
#         #url = 'http://triple-store.ai.wu.ac.at:8080/recognize/rest/recognize'
#         url = 'http://voyager.srv.weblyzard.net:8081/recognize/rest/recognize'
#         client = Recognize(url)
#         profile_names=['de.organization.ng', 'de.people.ng', 'de.geo.500000.ng']
#         text = 'Microsoft is an American multinational corporation headquartered in Redmond, Washington, that develops, manufactures, licenses, supports and sells computer software, consumer electronics and personal computers and services. It was was founded by Bill Gates and Paul Allen on April 4, 1975.'
#         text = "HTL Schulzentrum Weingut Fachhochschule Netzwerk"
#         client.add_profile('en.organization.ng')
#          
#         result = client.search_text(profile_names,
#                                     text,
#                                     output_format='compact',
#                                     max_entities=40,
#                                     buckets=40,
#                                     limit=40)
#         pprint(result)
#         print "end"

    def test_adrian(self):
 
        from pprint import pprint
         
 
        print "start"
     
        #url = 'http://triple-store.ai.wu.ac.at:8080/recognize/rest/recognize'
        url = 'http://voyager.srv.weblyzard.net:8081/recognize/rest/recognize'
        client = Recognize(url)
        profile_names=['de.organization.ng', 'de.people.ng', 'de.geo.500000.ng']
        text = 'Microsoft is an American multinational corporation headquartered in Redmond, Washington, that develops, manufactures, licenses, supports and sells computer software, consumer electronics and personal computers and services. It was was founded by Bill Gates and Paul Allen on April 4, 1975.'
        text = "HTL Schulzentrum Weingut Fachhochschule Netzwerk"
        client.add_profile('en.organization.ng')
         
        result = client.search_text(profile_names,
                                    text,
                                    output_format='compact',
                                    max_entities=40,
                                    buckets=40,
                                    limit=40)
        pprint(result)
        print "end"

            
#     def test_missing_profiles(self):
#         self.missing_profiles = []
#   
#         if self.IS_ONLINE and self.service_is_online:
#             if len(self.available_profiles) == len(self.TESTED_PROFILES):
#                 print "All profiles are available on the current server"
#             else:
#                 for profile in self.TESTED_PROFILES:
#                     if profile not in self.available_profiles:
#                         self.missing_profiles.append(profile)
#                 print "Missing profiles: ", self.missing_profiles
#    
#     def test_entity_lyzard(self):
#         docs = [{'content_id': '12', 'content': u'Franz Klammer fährt Ski'},
#                 {'content_id': '13', 'content' :u'Peter Müller macht Politik'}]
#    
#         required_profile = 'de.people.ng'
#         if required_profile not in self.available_profiles:
#             print "Profile %s not available!" % required_profile
#             return
#         #we test if we can add profiles and if a German profile works
#         if self.IS_ONLINE and self.service_is_online:
#             print self.client.list_profiles()
#             self.client.add_profile('de.people.ng')
#             print self.client.search_documents('de.people.ng', docs)
#              
#     def test_search_xml(self):
#         required_profile = 'de.people.ng'
#         if required_profile not in self.available_profiles:
#             print "Profile %s not available!" % required_profile
#             return
#           
#         if self.IS_ONLINE and self.service_is_online:
#             self.client.add_profile('de.people.ng')
#             result = self.client.search_documents('de.people.ng', self.DOCS)
#             print 'xmlsearch::::', result
#  
#     def test_focus_search(self):
#         required_profile = 'de.people.ng'
#         if required_profile not in self.available_profiles:
#             print "Profile %s not available!" % required_profile
#             return
#           
#         if self.IS_ONLINE and self.service_is_online:
#             pn = 'extras.com.weblyzard.backend.recognize.extras.DataTypeProfile'
#             result = self.client.get_focus(['de.people.ng', pn],
#                                            self.DOCS, max_results=3)
#    
#             # annotated two documents
#             assert len(result) == len(self.DOCS)
#    
#             for res in result.itervalues():
#                 print ':::', res
#                 assert u'focus' in res
#                 assert u'annotations' in res
  
#     def test_geo(self):
#         required_profile = 'en.geo.500000.ng'
#         if required_profile not in self.available_profiles:
#             print "Profile %s not available!" % required_profile
#             return
#  
#         geodocs = [{'content_id': '11',
#                     'content': u'Frank goes to Los Angeles. Los Angeles, Nice, Germany, Munich is a nice city. Why is Vienna not found?'},
#                ]
#   
#         if self.IS_ONLINE and self.service_is_online:
#             profile_name = 'de.geo.500000.ng'
#       
#             print self.client.list_configured_profiles()
#             print self.client.add_profile(profile_name, force=True)
#      
#             print 'list_configured_profiles', self.client.list_configured_profiles()
# #             self.client.add_profile('Cities.10000.en')
#      
# #             self.client.search_documents(profile_names=profile_name,
# #                                          doc_list=geodocs, debug=True,
# #                                          output_format='standard')
#             print 'list_profiles', self.client.list_profiles()
# #             self.client.add_profile('Cities.10000.en', geodocs)
# #             self.client.add_profile('Cities.10000.en')
#             result = self.client.search_documents(profile_name, geodocs, output_format='compact')
#             print result
#             first = result['11']
#             print 'result', len(result), first[0]['preferredName']
 
#     def test_geo_swiss(self):
#         '''
#         Tests the geo annotation service for Swiss media samples.
#          
#         .. note::
#  
#             ``de_CH.geo.5000.ng`` detects Swiss cities with more than 5000
#             and worldwide cities with more than 500,000 inhabitants.
#         '''
#         required_profile = 'de_CH.geo.5000.ng'
#         if required_profile not in self.available_profiles:
#             print("Profile %s not available!" % required_profile)
#             return
#  
#         if 'noah.semanticlab.net' not in self.client.url:
#             print("This test is only run on noah...\n...skipping test.")
#   
#         self.client.add_profile(required_profile)
#  
#    

    def test_organization(self):
        required_profile = 'en.organization.ng'
        if required_profile not in self.available_profiles:
            print "Profile %s not available!" % required_profile
            return
                    
        docs = [{'content_id': '14', 'content': u'Bill Gates was the CEO of Microsoft.'},
                {'content_id': '15', 'content' :u'Facebook is largest social networks.'}]
     
        if self.IS_ONLINE and self.service_is_online:
            print self.client.list_profiles()
            self.client.add_profile('en.organization.ng')
            print self.client.search_documents('en.organization.ng', docs)
#     
#     def test_people(self):
#         required_profile = 'en.people.ng'
#         if required_profile not in self.available_profiles:
#             print "Profile %s not available!" % required_profile
#             return
#            
#         docs = [{'content_id': '16', 'content': u'George W. Bush is a former President.'},
#                 {'content_id': '17', 'content' :u'Mark Zuckerberg speaks Chinese.'}]
#     
#         if self.IS_ONLINE and self.service_is_online:
#             print self.client.list_profiles()
#             self.client.add_profile('en.people.ng')
#             print self.client.search_documents('en.people.ng', docs)
#    
#    
#     def test_date_profile(self):
#         """ """
#         docs = [{'content_id': '12', 'content': u'Franz Klammer fährt gestern Ski, 12th September 2014 are we feeling better'}]
#         #                 {'content_id': '13', 'content' :u'Peter Müller macht Politik'}]
#         profile = 'extras.com.weblyzard.backend.recognize.extras.DateTimeProfile'
#         #         assert self.IS_ONLINE and self.service_is_online
#         #         assert profile in self.available_profiles
#          
#         result = self.client.search_documents(profile_names=[profile], doc_list=docs)
#         print result
#            
#     def test_password(self):
#         test_cases = (
#             ('http://test.net', 'test', 'password'),
#             ('http://test.net', None, None),
#             (['http://test.net', 'http://test2.net'], 'test', 'password'),
#             (['http://test.net', 'http://test2.net'], None, None))
#    
#         for urls, user, password in test_cases:
#             correct_urls = Recognize.fix_urls(urls, user, password)
#             assert isinstance(correct_urls, list)
#    
#             if isinstance(urls, basestring):
#                 assert len(correct_urls) == 1
#             else:
#                 assert len(urls) == len(correct_urls)
#    
#             for correct_url in correct_urls:
#                 assert correct_url.endswith(Recognize.URL_PATH)
#                 user_password = '%s:%s@' % (user, password)
#                 if user and password:
#                     assert user_password in correct_url
#                     ext_url, ext_user, ext_password = Retrieve.get_user_password(correct_url)
#                     assert ext_user == user
#                     assert ext_password == password
#                     assert user_password not in ext_url
#                 else:
#                     assert user_password not in correct_url
#   
#     def test_swiss_profile(self):
#         required_profile = 'de_CH.geo.5000.ng'
#         client = Recognize()
#         # client.remove_profile(required_profile)
#         client.add_profile(required_profile)
#         for text in 'Haldenstein liegt in der Nähe von Landquart.', 'Sargans hat einen wichtigen Bahnhof', 'Vinzenz arbeitet in Winterthur':
#             result = client.search_text(required_profile, text, output_format='compact' )
#             print(result)
#       
#         required_profile = 'snf.media.criticism.project'
#         client.add_profile(required_profile)
#         print client.search_text(required_profile, "Die SRG und die SRF sind sehr kritisch was das Engagement der NZZ betrifft", output_format='compact')
#         print client.search_text(required_profile, "die srg und die srf sind sehr kritisch was das engagement der nzz betrifft", output_format='compact')

if __name__ == '__main__':
    unittest.main()