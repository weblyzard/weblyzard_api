'''
.. codeauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''
from eWRT.ws.rest import  MultiRESTClient
from weblyzard_api.client import WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS

class DomainSpecificity(MultiRESTClient):
    '''
    **Domain Specificity Web Service**

    Determines whether documents are relevant for a given domain by searching for
    domain relevant terms in these documents.

    **Workflow**

     1. submit a domain-specificity profile with 
        :func:`add_profile`
     2. obtain the domain-speificity of text documents with 
        :func:`get_domain_specificity`, 
        :func:`parse_documents` or 
        :func:`search_documents`.
    '''
    URL_PATH = 'rest/domain_specificity' 
    
    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER, 
                 pwd=WEBLYZARD_API_PASS, default_timeout=None):
        '''
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        '''
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd,
                                 default_timeout=default_timeout)


    def add_profile(self, profile_name, profile_mapping):
        '''
        Adds a domain-specificity profile to the Web service.

        :param profile_name: the name of the domain specificity profile
        :param profile_mapping: a dictionary of keywords and their \
                               respective domain specificity values.
        '''
        return self.request('add_or_refresh_profile/%s' % profile_name,
                            profile_mapping, execute_all_services=True)
    
    def get_domain_specificity(self, profile_name, documents, 
                               is_case_sensitive=True):
        ''' 
        :param profile_name: the name of the domain specificity profile to \
                            use.
        :param documents: a list of dictionaries containing the document
        :param is_case_sensitive: whether to consider case or not (default: True) 
        '''
        return self.request('parse_documents/%s/%s' % (profile_name, 
                                                       is_case_sensitive),
                             documents) 

    def parse_documents(self, matview_name, documents, is_case_sensitive=False, 
                        batch_size=None):
        ''' 
        :param matview_name: a comma separated list of matview_names to check \
                             for domain specificity.
        :param documents: a list of dictionaries containing the document
        :param is_case_sensitive: case sensitive or not
        :returns: dict (profilename: (content_id, dom_spec))  
        '''
        found_tags = {}
        for document_batch in self.get_document_batch(documents=documents, 
                                                      batch_size=batch_size):
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
        '''
        :returns: a list of all available domain specificity profiles.
        '''
        return self.request('list_profiles')

    def has_profile(self, profile_name):
        '''
        Returns whether the given profile exists on the server.

        :param profile_name: the name of the domain specificity profile to \
                             check. 
        :returns: ``True`` if the given profile exists on the server.
        '''
        return profile_name in self.list_profiles()
    
    def meminfo(self):
        '''
        :returns: Information on the web service's memory consumption
        '''
        return self.request('meminfo')    

