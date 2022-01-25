#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
text sense service

.. codeauthor:: Mohamad Al Sayed <sayed@weblyzard.com>
'''
import json
import requests
import logging

logger = logging.getLogger(__name__)

SERVICE_URL = "http://text-sense.prod.i.weblyzard.net:8443"


class TextSenseRESTClient():

    VERSION = 1.0
    DOWNLOAD_MODEL_PATH = '{}/config/download_model'.format(VERSION)
    LIST_AVAILABLE_MODELS_PATH = '{}/config/list_available_models'.format(VERSION)
    LIST_ACTIVE_MODELS_PATH = '{}/config/list_active_models'.format(VERSION)
    ACTIVATE_MODEL_PATH = '{}/config/activate?'.format(VERSION)
    ANNOTATE_PATH = '{}/annotate'.format(VERSION)

    def __init__(self, url):
        '''
        :param url: URL of the text-sense web service
        '''
        self.url = url

    def download_model(self, **kwargs):
        """download models to gluster"""
        response = requests.post(
            '%s/%s' % (self.url, self.DOWNLOAD_MODEL_PATH), params=kwargs)
        if response.status_code < 400:
            return response.text
        else:
            return None

    def list_available_models(self):
        """list available models in gluster"""
        response = requests.get(
            '%s/%s' % (self.url, self.LIST_AVAILABLE_MODELS_PATH))
        if response.status_code < 400:
            return response.text
        else:
            return None

    def list_active_models(self):
        """list active models"""
        response = requests.get(
            '%s/%s' % (self.url, self.LIST_ACTIVE_MODELS_PATH))
        if response.status_code < 400:
            return response.content
        else:
            return None

    def activate_model(self, **kwargs):
        """activate a model"""
        response = requests.post(
            '%s/%s' % (self.url, self.ACTIVATE_MODEL_PATH), params=kwargs)
        if response.status_code == 200:
            return True
        else:
            return False

    def tag_text(self, pyload):
        """tag a text for a certain task (e.g., 'pos_en_de')"""

        response = requests.post(
            '%s/%s' % (self.url, self.ANNOTATE_PATH), params=pyload)
        if response.status_code < 400:
            return json.loads(response.text)
        else:
            return None
