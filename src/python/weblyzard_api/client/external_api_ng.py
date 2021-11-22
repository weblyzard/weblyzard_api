#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
.. codeauthor:: Rod Coronel 
'''

from weblyzard_api.client import MultiRESTClient
from weblyzard_api.client import (
    WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS)

class ExternalApiNg(MultiRESTClient):
    
    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER,
                 pwd=WEBLYZARD_API_PASS, default_timeout=None):
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd,
                        default_timeout=default_timeout)
    
    def submit_single_document(self, document):
        result = self.request('checkDocumentRelevanceNg', document, pass_through_exceptions=True)
        return result

    def submit_batch_documents(self, documents):
        result = self.request('checkDocumentRelevanceBatch', documents, pass_through_exceptions=True)
        return result
