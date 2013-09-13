'''
Created on Jan 16, 2013

@author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''

from unittest import main, TestCase

from eWRT.ws.rest import RESTClient
from weblyzard_api.client import WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS


class DomainSpecificity(RESTClient):
    '''
    Domain Specificity Web Service
    '''
    
    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER, pwd=WEBLYZARD_API_PASS):
        url += '/rest/domain_specificity'
        RESTClient.__init__(self, url, usr, pwd)

    def add_profile(self, profile_name, profile_mapping):
        '''
        Adds a domain-specificity profile to the Web service.
        @param profile_name: the name of the domain specificity profile
        @param profile_mapping: a dictionary of keywords and their
                               respective domain specificity values.
        '''
        return self.execute("add_or_refresh_profile", 
                             profile_name, profile_mapping )

    
    def get_domain_specificity( self, profile_name, documents, 
                                is_case_sensitive=True ):
        ''' 
        @param profile_name: the name of the domain specificity profile to
                            use.
        @param documents: a list of dictionaries containing the document
        @param is_case_sensitive: whether to consider case or not (default: True) 
        '''
        return self.execute( "parse_documents", 
                             "%s/%s" % (profile_name, is_case_sensitive),
                             documents) 

    def has_profile(self, profile_name):
        '''
        Returns whether the given profile exists on the server.
        @param profile_name: the name of the domain specificity profile to
                             check. 
        '''
        profiles = self.execute("list_profiles")
        return profile_name in profiles
    
    def meminfo(self):
        return self.execute("meminfo")    


class TestDomainSpecificity(TestCase):        
    
    def test_domain_specificity(self):            
        PROFILE_NAME1 = 'test1'
        PROFILE_MAPPING1 = {'ana': 0.8, 'daniela': 0.7, 'markus': 0.2 }
    
        PROFILE_NAME2 = 'test2'
        PROFILE_MAPPING2 = {'jasna': 1.0, 'pool': 0.1, 'ana': -0.2 }
        
      
        d = DomainSpecificity( )
        d.add_profile(PROFILE_NAME1, PROFILE_MAPPING1)
        d.add_profile(PROFILE_NAME2, PROFILE_MAPPING2)
        
        assert d.has_profile(PROFILE_NAME1)
        assert not d.has_profile('unknown')
        
        self._test_domain_specifcity(PROFILE_NAME1)

        
    def _test_domain_specifcity(self, domain_specificity_profile):
        TEST_DOCUMENT_LIST = [{'content_id': "1", 
                               'title': 'Ana loves Daniel.', 
                               'content': 'ana knowns daniela and gerhard.'} ,
                              {'content_id': "2", 
                               'title': 'Jasna knows Ana.', 
                               'content': 'I have met jasna at the pool.'} ]
        
        d = DomainSpecificity( )
        print d.get_domain_specificity(domain_specificity_profile, TEST_DOCUMENT_LIST)
        print d.get_domain_specificity(domain_specificity_profile, TEST_DOCUMENT_LIST, 
                                       is_case_sensitive=False)
   
    def test_meminfo(self):
        d = DomainSpecificity()
        print d.meminfo()


if __name__ == '__main__':
    main()
