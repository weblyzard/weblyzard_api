# -*- coding: utf8 -*
'''
.. codeauthor: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
.. codeauthor:: Heinz-Peter Lang <lang@weblyzard.com>
'''
from eWRT.ws.rest import MultiRESTClient

from weblyzard_api.client import WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS


class JesajaNg(MultiRESTClient):
    '''
    Provides access to the Jesaja keyword service which extracts
    associations (i.e. keywords) from text documents.
    '''

    URL_PATH = 'jesaja/rest'

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
                    'min_phrase_significance'        : 2.0,
                    'num_keywords'                   : 5,
                    'keyword_algorithm'              : 'com.weblyzard.backend.jesaja.algorithm.keywords.YatesKeywordSignificanceAlgorithm',
                    'min_token_count'                : 5,
                    'skip_underrepresented_keywords' : True,
                    'stoplists'                      : [],
                }

        .. note:: ``Available keyword_algorithms``

            * ``com.weblyzard.backend.jesaja.algorithm.keywords.YatesKeywordSignificanceAlgorithm``
            * ``com.weblyzard.backend.jesaja.algorithm.keywords.LogLikelihoodKeywordSignificanceAlgorithm``

        '''
        return self.request('set_keyword_profile/{}'.format(profile_name),
                            keyword_calculation_profile)

    def add_csv(self, matview_id, keyword_count_map):
        '''
        Adds reference documents for Jesaja.

        :param matview_id:
            matview_id for which the documents are relevant
        :param keyword_count_map:
            a map of keywords and the corresponding counts
            {'the': 222, 'a': 200, ...}
        '''
        if matview_id is None:
            raise ValueError, 'Please specify the matview for which the documents are designated.'
        return self.request('add_csv/{}'.format(matview_id), keyword_count_map)

    def add_documents(self, matview_id, xml_documents):
        '''
        Adds reference documents for Jesaja.

        :param matview_id:
            matview_id for which the documents are relevant
        :param xml_documents:
            a list of weblyzard_xml documents [ xml_content, ... ]
        '''
        if matview_id is None:
            raise ValueError, 'Please specify the matview for which the documents are designated.'
        return self.request('add_documents/{}'.format(matview_id), xml_documents)

    def get_keyword_annotations(self, matview_id, xml_documents):
        '''
        :param matview_id: the matview id for which the keywords are computed
        :param xml_documents:
            a list of weblyzard_xml documents [ xml_content, ... ]

        '''
        if not self.has_matview(matview_id):
            raise Exception('Cannot compute keywords - unknown matview {}'.format(matview_id))
        return self.request('get_nek_annotations/{}'.format(matview_id), xml_documents)
    
    def get_keywords(self, matview_id, xml_documents):
        '''
        :param matview_id: the matview id for which the keywords are computed
        :param xml_documents:
            a list of weblyzard_xml documents [ xml_content, ... ]

        '''
        if not self.has_matview(matview_id):
            raise Exception('Cannot compute keywords - unknown matview {}'.format(matview_id))
        return self.request('get_keywords/{}'.format(matview_id), xml_documents)

    def has_matview(self, matview_id):
        return matview_id in self.list_matviews()

    def has_corpus(self, matview_id):
        available_completed_shards = self.request('list_shards/complete/{}'.format(matview_id))
        return len(available_completed_shards[matview_id]) > 0

    def get_corpus_size(self, matview_id):
        available_completed_shards = self.request('list_shards/complete/{}'.format(matview_id))
        total = 0
        for shard in available_completed_shards[matview_id]:
            total= total + shard['wordCount']
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
        return self.request('set_matview_profile/{}/{}'.format(matview_id, profile_name))

    def list_stoplists(self):
        '''
        :returns: a list of all available stopword lists.
        '''
        return self.request('list_stoplists')

    def rotate_shard(self, matview_id=None):
        '''
        :param matview_id: an optional matview_id of the shard to be rotated

        .. note::

        All shards are automatically rotated every 24 hourse. Call this
        method to speed up the availablilty of a shart
        '''
        if not matview_id:
            return self.request('rotate_shard')
        else:
            return self.request('rotate_shard/{}'.format(matview_id))
