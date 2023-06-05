#!/usr/bin/python
# -*- coding: utf8 -*-
"""
.. moduleauthor:: Max Goebel <goebel@weblyzard.com>
"""
from __future__ import unicode_literals
from weblyzard_api.client import MultiRESTClient

from weblyzard_api.client import (WEBLYZARD_API_URL, WEBLYZARD_API_USER,
                                  WEBLYZARD_API_PASS)


class JairoClient(MultiRESTClient):

    URL_PATH = 'rest'

    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER,
                 pwd=WEBLYZARD_API_PASS, default_timeout=None):
        """
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        """
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd,
                                 default_timeout=default_timeout)

    def set_profile(self, profile_name, profile):
        """ """
        # latest jairo no longer supports profile types
        if 'types' in profile:
            del profile['types']
        return self.request('add_profile/{}'.format(profile_name), profile)

    def enrich_annotations(self, profile_name, annotations):
        """
        Enrich a list/dict of annotations with a given profile_name.
        :param profile_name: the profile to use for enrichment
        :param annotations: the annotations to enricht
        :returns: the enriched annotations, or None
        """
        annotations_to_send = []
        if isinstance(annotations, dict):
            annotations = list(annotations.values())
        for annotation in annotations:
            if len(annotation.get('key', '')) > 3:
                annotations_to_send.append(annotation)
        if len(annotations_to_send) > 0:
            return self.request('extend_annotations/{}'.format(profile_name),
                                annotations_to_send)
        else:
            return None

    def list_profiles(self):
        """ """
        return self.request('list_profiles')

    def reload_profiles(self):
        """ """
        return self.request('reload_profiles')

    def status(self):
        """ """
        return self.request('status')
