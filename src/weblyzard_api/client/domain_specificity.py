'''
Created on Jan 16, 2013

@author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''
from unittest import main, TestCase

from eWRT.ws.rest import  MultiRESTClient
from weblyzard_api.client import WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS

class DomainSpecificity(MultiRESTClient):
    '''
    Domain Specificity Web Service
    '''
    URL_PATH = 'rest/domain_specificity' 
    
    def __init__(self, url=WEBLYZARD_API_URL, 
                 usr=WEBLYZARD_API_USER, pwd=WEBLYZARD_API_PASS):
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd)

    def add_profile(self, profile_name, profile_mapping):
        '''
        Adds a domain-specificity profile to the Web service.
        @param profile_name: the name of the domain specificity profile
        @param profile_mapping: a dictionary of keywords and their
                               respective domain specificity values.
        '''
        return self.request('add_or_refresh_profile/%s' % profile_name,
                            profile_mapping, execute_all_services=True)
    
    def get_domain_specificity(self, profile_name, documents, 
                               is_case_sensitive=True):
        ''' 
        @param profile_name: the name of the domain specificity profile to
                            use.
        @param documents: a list of dictionaries containing the document
        @param is_case_sensitive: whether to consider case or not (default: True) 
        '''
        return self.request('parse_documents/%s/%s' % (profile_name, 
                                                       is_case_sensitive),
                             documents) 

    def parse_documents(self, matview_name, documents, is_case_sensitive=False):
        ''' 
        @param matview_name: a comma separated list of matview_names to check 
                             for domain specificity.
        @param documents: a list of dictionaries containing the document
        @param is_case_sensitive: case sensitive or not
        @return: dict (profilename: (content_id, dom_spec))  
        '''
        found_tags = {}
        for document_batch in self.get_document_batch(documents):
            result = self.request('parse_documents/%s/%s' % 
                                  (matview_name, is_case_sensitive), 
                                  document_batch)
            if result:
                found_tags.update(result[matview_name])
                
        return found_tags

    def search_documents(self, profile_name, documents, is_case_sensitive=False):
        return self.request('search_documents/%s/%s' % (profile_name, 
                                                        is_case_sensitive), 
                            documents)

    def list_profiles(self):
        return self.request('list_profiles')

    def has_profile(self, profile_name):
        '''
        Returns whether the given profile exists on the server.
        @param profile_name: the name of the domain specificity profile to
                             check. 
        '''
        return profile_name in self.list_profiles()
    
    def meminfo(self):
        return self.request('meminfo')    

class TestDomainSpecificity(TestCase):        
    
    def test_domain_specificity(self):            
        PROFILE_NAME1 = 'test1'
        PROFILE_MAPPING1 = {'ana': 0.8, 'daniela': 0.7, 'markus': 0.2}
    
        PROFILE_NAME2 = 'test2'
        PROFILE_MAPPING2 = {'jasna': 1.0, 'pool': 0.1, 'ana': -0.2}
        
      
        d = DomainSpecificity()
        d.add_profile(PROFILE_NAME1, PROFILE_MAPPING1)
        d.add_profile(PROFILE_NAME2, PROFILE_MAPPING2)
        
        assert d.has_profile(PROFILE_NAME1)
        assert not d.has_profile('unknown')
        
        self._test_domain_specifcity(PROFILE_NAME1)

    def _test_domain_specifcity(self, domain_specificity_profile):
        TEST_DOCUMENT_LIST = [{'content_id': '1', 
                               'title': 'Ana loves Daniel.', 
                               'content': 'ana knowns daniela and gerhard.'},
                              {'content_id': '2', 
                               'title': 'Jasna knows Ana.', 
                               'content': 'I have met jasna at the pool.'}]
        
        d = DomainSpecificity( )
        print d.get_domain_specificity(domain_specificity_profile, 
                                       TEST_DOCUMENT_LIST)
        print d.get_domain_specificity(domain_specificity_profile, 
                                       TEST_DOCUMENT_LIST, 
                                       is_case_sensitive=False)
   
    def test_meminfo(self):
        d = DomainSpecificity()
        print d.meminfo()


if __name__ == '__main__':
    main()
