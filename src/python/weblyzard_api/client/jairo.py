#!/usr/bin/python
# -*- coding: utf8 -*-
'''
.. moduleauthor:: Max Goebel <goebel@weblyzard.com>
'''
from eWRT.ws.rest import MultiRESTClient

from weblyzard_api.client import (WEBLYZARD_API_URL, WEBLYZARD_API_USER,
                                  WEBLYZARD_API_PASS)


class JairoClient(MultiRESTClient):

    URL_PATH = 'rest'

    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER,
                 pwd=WEBLYZARD_API_PASS, default_timeout=None):
        '''
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        '''
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd,
                                 default_timeout=default_timeout)

    def set_profile(self, profile_name, profile):
        ''' '''
        return self.request('profiles/add/{}'.format(profile_name), profile)

    def enrich_annotations(self, profile_name, annotations):
        ''' '''
        return self.request('annotations/enrich/{}'.format(profile_name),
                            annotations)

    def list_profiles(self):
        ''' '''
        return self.request('profiles/list', return_plain=True)

    def reload_profiles(self):
        ''' '''
        return self.request('profiles/reload', return_plain=True)

    def status(self):
        ''' '''
        return self.request('status', return_plain=True)
