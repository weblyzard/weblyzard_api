# -*- coding: utf-8 -*-
"""
Created on Jan 16, 2013

@author: Philipp Kuntschik <philipp.kuntschik@htwchur.ch>
"""
from __future__ import unicode_literals
from weblyzard_api.client import MultiRESTClient
import logging
from weblyzard_api.client import (
    WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS)

logger = logging.getLogger(__name__)


class MediaCriticism(MultiRESTClient):

    # base bath to the deployed media criticism mission control
    CLASSIFIER_WS_BASE_PATH = '/rest/'

    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER,
                 pwd=WEBLYZARD_API_PASS, default_timeout=None):
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd,
                                 default_timeout=default_timeout)

    def status(self):
        """
        Return the status of the service.
        """
        return self.request(self.CLASSIFIER_WS_BASE_PATH + 'status')

    def check_domain_relevance(self, api_document):
        """
        Check the domain relevance of a given document.
        :param api_document:
            the api_document to check
        :returns
             a tuple which is composed as follows
               (is_relevant, mediacriticism_score, num_recognized_entities)
        """
        logger.warn("DEPRECATED: please use check_relevance instead")
        result = self.request(self.CLASSIFIER_WS_BASE_PATH
                              + 'checkDocumentRelevance', api_document)
        return result['relevantDocument'], result['mediacriticism']

    def check_relevance(self, api_document, endpoint='checkDocumentRelevance', score_field='mediacriticism'):
        """
        Check the relevance of a document based on a custom API endpoint
        and obtain a `score` based on the return response's field value
        """
        result = self.request(self.CLASSIFIER_WS_BASE_PATH +
                              endpoint, api_document)
        return result['relevantDocument'], result[score_field]
