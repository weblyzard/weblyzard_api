# -*- coding: UTF-8 -*-
#!/usr/bin/env python

""" barebone domain-specificity service """
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import object

import urllib.request
from json import dumps, loads

from weblyzard_api.client import (
    WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS)


class Annotator(object):

    def __init__(self, service_url=WEBLYZARD_API_URL):
        self.service_url = service_url

    @staticmethod
    def _json_request(url, parameters):
        if parameters:
            req = urllib.request.Request(url , dumps(parameters),
                                   {'Content-Type': 'application/json'})
        else:
            req = urllib.request.Request(url)

        f = urllib.request.urlopen(req)
        response = f.read()
        f.close()

        if response:
            return loads(response)

    def add_profile(self, annotation_profile_name, mapping):
        return self._json_request(
            self.service_url + "/add_or_refresh_profile/" + annotation_profile_name,
            mapping)

    def annotate_text(self, annotation_profile_name, documents):
        """ 
        @param annotation_profile_name: a dictionary of replacement patterns
            and the list of corresponding search patterns.
            e.g. {'<s>%s</s>': ['ana', 'daniela', 'markus'],
                  '<l>%s</l>': ['jasna']} 
        @param documents: a list of dictionaries containing the document 
        """
        return self._json_request(
            self.service_url + "/annotate_text/" + annotation_profile_name,
            documents)

    def annotate_xml(self, annotation_profile_name, documents, search_tag,
                      is_cdata_encapsulated):
        """ 
        @param annotation_profile_name: a dictionary of replacement patterns
            and the list of corresponding search patterns.
            e.g. {'<s>%s</s>': ['ana', 'daniela', 'markus'],
                  '<l>%s</l>': ['jasna']} 
        @param documents: a list of dictionaries containing the document
        @param search_tag: the tag which contains the text to scan
        @param is_cdata_encapsulated: whether the data is cdata encapsulated 
        """
        return self._json_request(
            "%s/annotate_xml/%s/%s/%s" % (self.service_url, annotation_profile_name,
                                           search_tag, is_cdata_encapsulated), documents)

    def has_profile(self, profile_name):
        profiles = self._json_request(self.service_url + "/list_profiles", None)
        return profile_name in profiles

