#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
.. codeauthor: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
.. codeauthor:: Heinz-Peter Lang <lang@weblyzard.com>
'''
from __future__ import print_function
from __future__ import unicode_literals
from eWRT.ws.rest import MultiRESTClient

from weblyzard_api.client import (
    WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS)


class JesajaNg(MultiRESTClient):
    '''
    Provides access to the Jesaja keyword service which extracts
    associations (i.e. keywords) from text documents.
    '''

    URL_PATH = 'rest'

    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER,
                 pwd=WEBLYZARD_API_PASS, default_timeout=None,
                 use_random_server=True):
        '''
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        '''
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd,
                                 default_timeout=default_timeout,
                                 use_random_server=use_random_server)

    def set_keyword_profile(self, profile_name, keyword_calculation_profile):
        ''' Add a keyword profile to the server

        :param profile_name: the name of the keyword profile
        :param keyword_calculation_profile: the full keyword calculation \
            profile (see below).

        .. note:: Example keyword calculation profile

            ::

                {
                    'valid_pos_tags'                 : ['NN', 'P', 'ADJ'],
                    'required_pos_tags'              : [],
                    'corpus_name'                    : reference_corpus_name,
                    'min_phrase_significance'        : 2.0,
                    'num_keywords'                   : 5,
                    'skip_underrepresented_keywords' : True,
                    'keyword_algorithm'              : 'com.weblyzard.backend.jesaja.algorithm.keywords.YatesKeywordSignificanceAlgorithm', 
                    'min_token_count'                : 5,
                    'min_ngram_length'               : 1,
                    'max_ngram_length'               : 3,
                    'stoplists'                      : [],
                    'groundAnnotations'              : False,
                    'ignore_titles'                  : False,
                }

        .. note:: ``Available keyword_algorithms``

            * ``com.weblyzard.backend.jesaja.algorithm.keywords.YatesKeywordSignificanceAlgorithm``
            * ``com.weblyzard.backend.jesaja.algorithm.keywords.LogLikelihoodKeywordSignificanceAlgorithm``

        '''
        return self.request('set_keyword_profile/{}'.format(profile_name),
                            keyword_calculation_profile)

    def add_csv(self, profile_name, keyword_count_map):
        '''
        Adds reference documents for Jesaja.

        :param profile_name:
            profile_name for which the documents are relevant
        :param keyword_count_map:
            a map of keywords and the corresponding counts
            {'the': 222, 'a': 200, ...}
        '''
        if profile_name is None:
            raise ValueError('Please specify the profile_name which the documents are designated.')
        return self.request('add_csv/{}'.format(profile_name), keyword_count_map)

    def add_documents(self, profile_name, documents):
        '''
        Adds reference documents for Jesaja.

        :param matview_id:
            matview_id for which the documents are relevant
        :param documents:
            a list of weblyzard documents
        '''
        if profile_name is None:
            raise ValueError('Please specify the profile_name for which the documents are designated.')
        return self.request('add_documents/{}'.format(profile_name), documents)

    def get_keyword_annotations(self, profile_name, documents,
                                num_keywords:int=None, add_ngrams=True):
        '''
        :param matview_id: the profile_name for which the keywords are computed
        :param documents:  a list of weblyzard documents
        :param num_keywords: the amount of keywords to be returned
        :param add_ngrams: if set, new ngrams are added to the reference corpus
        '''
        if not self.has_profile(profile_name):
            raise Exception(
                'Cannot compute keywords - unknown profile_name {}'.format(profile_name))

        endpoint = f'get_nek_annotations/{profile_name}'
        if num_keywords is not None and int(num_keywords) > 0:
            endpoint = f'{endpoint}?num_keywords={num_keywords}'
        if not add_ngrams:
            separator = '?'
            if '?' in endpoint:
                separator = '&'
            endpoint = f'{endpoint}{separator}add_ngrams=false'

        return self.request(endpoint, documents)

    def get_keywords(self, profile_name, documents):
        '''
        :param profile_name: the profile_name for which the keywords are computed
        :param documents:
            a list of weblyzard_xml documents [ xml_content, ... ]

        '''
        if not self.has_profile(profile_name):
            raise Exception(
                'Cannot compute keywords - unknown profile_name {}'.format(profile_name))
        return self.request('get_keywords/{}'.format(profile_name), documents)

    def has_profile(self, profile_name):
        return profile_name in self.list_profiles()

    def has_corpus(self, profile_name):
        available_completed_shards = self.request(
            'list_shards/complete/{}'.format(profile_name))
        return len(available_completed_shards[profile_name]) > 0

    def remove_matview_profile(self, profile_name):
        if not self.has_profile(profile_name):
            print('No profile {} found'.format(profile_name))
            return
        return self.request('remove_profile/{}'.format(profile_name),
                            return_plain=True)

    def get_corpus_size(self, profile_name):
        available_completed_shards = self.request(
            'list_shards/complete/{}'.format(profile_name))
        total = 0
        for shard in available_completed_shards[profile_name]:
            total = total + shard['wordCount']
        return total

    def list_profiles(self):
        return self.request('list_profiles')

    def list_matviews(self):
        return self.request('list_matview_profiles')

    def get_cache_stats(self):
        return self.request('get_cache_stats', return_plain=True)

    def get_cached_corpora(self):
        return self.request('get_cached_corpora')

    def set_stoplist(self, name, stoplist):
        '''
        :param name: name of the stopword list
        :param stoplist: a list of stopwords for the keyword computation
        '''
        return self.request('set_stoplist/{}'.format(name), stoplist)

    def set_matview_profile(self, matview_id, profile_name):
        '''
        Determines which profile to use for the given matview
        '''
        return self.request('set_matview_profile/{}/{}'.format(matview_id,
                                                               profile_name))

    def list_stoplists(self):
        '''
        :returns: a list of all available stopword lists.
        '''
        return self.request('list_stoplists')

    def rotate_shard(self, profile_name=None):
        '''
        :param profile_name: an optional profile_name of the shard to be rotated

        .. note::

        All shards are automatically rotated every 24 hours. Call this
        method to speed up the availability of a shard.
        '''
        if not profile_name:
            return self.request('rotate_shard')
        else:
            return self.request('rotate_shard/{}'.format(profile_name))
