#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 15.12.2014

'''
import logging

from weblyzard_api.client import MultiRESTClient
from weblyzard_api.client import (
    WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS)

SERVER_URL_PATH = '/rest/polarity/document'


logger = logging.getLogger(__name__)


class OpinionClient(MultiRESTClient):
    URL_PATH = '/'.join(SERVER_URL_PATH.split('/')[:-1])

    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER,
                 pwd=WEBLYZARD_API_PASS, default_timeout=None):
        '''
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        '''
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd,
                                 default_timeout=default_timeout)

    def get_polarity(self, content, content_format, annotations=None,
                     allow_unsupported=False, ignored_entity_regexp=None,
                     extra_categories=None, textblob_method=0,
                     textblob_threshold=None):
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
                result = self.request(
                    'document',
                    parameters={'format': content_format,
                                'content': content,
                                'annotations': annotations,
                                'allow_unsupported': allow_unsupported,
                                'ignored_entity_regexp': ignored_entity_regexp,
                                'extra_categories': extra_categories,
                                'use_textblob': textblob_method,
                                'textblob_threshold': textblob_threshold},
                    return_plain=False
                )
                break
            except Exception as e:
                if retries <= retrycount:
                    pass  # silently retry
                else:
                    msg = f'Request to sentiment webservice ' \
                          f'failed {retries} times, latest error was {e}'
                    logger.warning(msg, exc_info=True)
                    result = {
                        'error': msg}
        return result

    def status(self):
        return self.request('config')
