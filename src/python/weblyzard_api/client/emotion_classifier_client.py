#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on April 15, 2021

@author: jakob <jakob.steixner@modul.ac.at>
'''


from eWRT.ws.rest import MultiRESTClient
from weblyzard_api.client import (
    WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS)

SERVER_URL_PATH = '/rest/emotions/document'



class EmotionClassifierClient(MultiRESTClient):
    URL_PATH = '/'.join(SERVER_URL_PATH.split('/')[:-1])
    DEFAULT_EMOTIONAL_CATEGORIES = 'glove_lemmatized'

    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER,
                 pwd=WEBLYZARD_API_PASS, default_timeout=None):
        '''
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        '''
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd,
                                 default_timeout=default_timeout)

    def get_emotions(self, content, content_format,
                     emotional_categories=DEFAULT_EMOTIONAL_CATEGORIES):
        '''
        Sends the content in the content_format to the opinion mining server
        to calculate the polarity/sentiment of the content.

        :param content str: The string containing the document to analyze.
        :param content_format str: The format of the content. Must be 'xml' or
            'plaintext'
        :returns: The content (modified, if xml) and the content's overall
            polarity in a dict with content and polarity as keys. If an error
            ocurred, it is also contained in the dict with the 'error' key.
        :rtype: dict
        '''
        result = None
        retrycount = 1
        retries = 0
        while retries <= retrycount:
            retries += 1
            try:
                result = self.request('document',
                                      parameters={'format': content_format,
                                                  'content': content,
                                                  'emotional_categories': emotional_categories},
                                      return_plain=False)
                break
            except Exception as e:
                if retries <= retrycount:
                    pass  # silently retry
                else:
                    result = {
                        'error': 'Request to emotions webservice timed out %d times' % retries}
        return result

    def status(self):
        return self.request('config')
