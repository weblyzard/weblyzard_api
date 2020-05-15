#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on May 15, 2020;

@author: jakob <jakob.steixner@modul.ac.at>

Client for OpenThesaurus, a community generated tool for generating
synonyms for German. The pulbic API endpoint is available at
https://www.openthesaurus.de/, so this client can be used out of a box
by initializing it with
http://gecko8.wu.ac.at:8081/synonyme/search?format=application/json&q=lockerung
'''
from collections import defaultdict
from itertools import chain

from eWRT.ws.rest import MultiRESTClient

class OpenThesaurusClient(MultiRESTClient):
    """Client for OpenThesaurus, a community generated tool for generating
    synonyms for German. The pulbic API endpoint is available at
    https://www.openthesaurus.de/, so this client can be used out of a box
    as with `OpenThesaurusClient('https://www.openthesaurus.de/')`. However,
    the public API currently has a limit of 60 terms per minute, so for
    more regular usage, it is recommended to install your own instance
    following the instructions in
    https://github.com/OpenTaal/opentaal-openthesaurus/blob/master/README.md
    """
    VERSION: float = 1.0
    URL_PATH = '/synonyme'
    NORMALIZE_FUNCTION = lambda x, y: y.lower()
    BLOCKED_LEVELS = []

    def get_synsets(self, term: str):
        """Get a dict with synonyms sorted by synset id"""
        term = self.NORMALIZE_FUNCTION(term)
        result = self.request(path='search',
                              query_parameters={
                                  'format': 'application/json',
                                  'q': term
                              })
        synonymous_terms = defaultdict(list)
        for synset in result.get('synsets', []):
            for syn in synset.get('terms', []):
                if not syn.get('level') in self.BLOCKED_LEVELS:
                    synonymous_terms[synset['id']].append(syn.get('term'))

        return synonymous_terms

    def get_plain_synonyms(self, term):
        """get an unordered set of all potential synonyms"""
        return set(chain(*self.get_synsets(term).values()))
