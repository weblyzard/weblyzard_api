#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
.. codeauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''
import unittest

from weblyzard_api.client.domain_specificity import DomainSpecificity

class TestDomainSpecificity(unittest.TestCase):        
    
    def setUp(self):
        self.client = DomainSpecificity()
        self.service_is_online = self.jesaja.is_online()
        if not self.service_is_online: 
            print('WARNING: Webservice is offline --> not executing all tests!!')
            
    def test_domain_specificity(self):
        if not self.service_is_online: 
            return 
                    
        PROFILE_NAME1 = 'test1'
        PROFILE_MAPPING1 = {'ana': 0.8, 'daniela': 0.7, 'markus': 0.2}
    
        PROFILE_NAME2 = 'test2'
        PROFILE_MAPPING2 = {'jasna': 1.0, 'pool': 0.1, 'ana': -0.2}
        
      
        self.client.add_profile(PROFILE_NAME1, PROFILE_MAPPING1)
        self.client.add_profile(PROFILE_NAME2, PROFILE_MAPPING2)
        
        assert self.client.has_profile(PROFILE_NAME1)
        assert not self.client.has_profile('unknown')
        
        self._test_domain_specifcity(PROFILE_NAME1)

    def _test_domain_specifcity(self, domain_specificity_profile):
        if not self.service_is_online: 
            return 
        TEST_DOCUMENT_LIST = [{'content_id': '1', 
                               'title': 'Ana loves Daniel.', 
                               'content': 'ana knowns daniela and gerhard.'},
                              {'content_id': '2', 
                               'title': 'Jasna knows Ana.', 
                               'content': 'I have met jasna at the pool.'}]
        
        print(self.client.get_domain_specificity(domain_specificity_profile, 
                                       TEST_DOCUMENT_LIST))
        print(self.client.get_domain_specificity(domain_specificity_profile, 
                                                 TEST_DOCUMENT_LIST, 
                                                 is_case_sensitive=False))
   
    def test_meminfo(self):
        if not self.service_is_online: 
            return 
        print(self.client.meminfo())

if __name__ == '__main__':
    unittest.main()
