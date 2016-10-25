#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Oct 24, 2016

@author: stefan
'''

import requests


class SKBRESTClient():
    
    TRANSLATION_PATH = '1.0/skb/translation?'

    def __init__(self, url):
        '''
        :param url: URL of the SKB web service
        '''
        self.url = url

    def translate(self, **kwargs):
        response = requests.get('%s/%s' % (self.url, self.TRANSLATION_PATH), params=kwargs)
        return(response.text, kwargs['target'])