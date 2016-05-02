# -*- coding: utf8 -*
'''
.. codeauthor: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
.. codeauthor:: Heinz-Peter Lang <lang@weblyzard.com>
'''

import unittest
from gzip import GzipFile
from cPickle import load

from eWRT.ws.rest import MultiRESTClient

from weblyzard_api.client import WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS
from weblyzard_api.test import get_full_path

class JesajaNg(MultiRESTClient):
    '''
    Provides access to the Jesaja keyword service which extracts
    associations (i.e. keywords) from text documents.
    '''

    URL_PATH = 'jesaja/rest'

    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER,
                 pwd=WEBLYZARD_API_PASS, default_timeout=None):
        '''
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        '''
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd,
                                 default_timeout=default_timeout)


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

class JesajaTest(unittest.TestCase):

    PROFILE_NAME = 'default'
    STOPLIST_PROFILE_NAME = 'stoplist'
    CORPUS_NAME  = 'test_corpus'
    MATVIEW_NAME = 'unittest'
    SAMPLE_DATA_FILE = get_full_path('xml_documents.pickle.gz')

    PROFILE = {
        'valid_pos_tags'                 : ['NN', 'NNP', 'NNS'],#['NN', 'P', 'ADJ'],
        'min_phrase_significance'        : 2.0,
        'num_keywords'                   : 5,
        'keyword_algorithm'              : 'com.weblyzard.backend.jesaja.algorithm.keywords.YatesKeywordSignificanceAlgorithm', # com.weblyzard.backend.jesaja.algorithm.keywords.LogLikelihoodKeywordSignificanceAlgorithm
        'min_token_count'                : 5,
        'skip_underrepresented_keywords' : True,
        'stoplists'                      : [],
    }

    def setUp(self):
        '''
        Setup Jesaja Keyword Server
        '''
        self.jesaja = JesajaNg()
        self.service_is_online = self.jesaja.is_online()

        if self.service_is_online:

            STOPLIST_PROFILE = self.PROFILE.copy()
            STOPLIST_PROFILE['stoplists'] = ['testList', 'anotherList']

            with GzipFile(self.SAMPLE_DATA_FILE) as f:
                sample_corpus = load(f)
                print 'Loaded corpus with %d entries' % (len(sample_corpus))

            self.jesaja.set_stoplist('testList',
                                     ('the', 'from', 'there', 'here') )
            self.jesaja.set_stoplist('anotherList',
                                     ('you', 'he', 'she', 'it', 'them'))
            self.jesaja.set_keyword_profile(self.PROFILE_NAME, self.PROFILE)
            self.jesaja.set_keyword_profile(self.STOPLIST_PROFILE_NAME, STOPLIST_PROFILE)
            self.jesaja.set_matview_profile(self.MATVIEW_NAME, self.PROFILE_NAME)

            # create the reference corpus
            if not self.jesaja.has_corpus(matview_id=self.MATVIEW_NAME):
                while self.jesaja.rotate_shard(matview_id=self.MATVIEW_NAME) == 0:
                    csv_corpus = {'keystone':25, 'energy': 123, 'ana': 12, 'tom': 22, 'petra': 3, 'clima':5, 'Shihab': 12, 'Kirche':10}
                    self.jesaja.add_csv(matview_id=self.MATVIEW_NAME, keyword_count_map=csv_corpus )
                    self.jesaja.add_documents(matview_id=self.MATVIEW_NAME, xml_documents=sample_corpus)
        else:
            print 'WARNING: Webservice is offline --> not executing all tests!!'

    def test_server_is_online(self):
        ''' tests if the server is online '''
        assert self.jesaja.is_online(), 'server not online!!!'

#     def test_matview_list(self):
#         if self.service_is_online:
#             self.assertTrue(self.jesaja.has_matview(self.MATVIEW_NAME) )
#             self.assertFalse(self.jesaja.has_matview('unknown'))

    def test_get_neks(self):
     
        xml_documents = ['''<wl:page xmlns:wl="http://www.weblyzard.com/wl/2013#" wl:id="495692737" xml:lang="en" wl:nilsimsa="5bb001c8a610a105b1120bb9c4889d33c62b19e1493245cc2f252a83e270646b" title="Keystone report leaves environmental, energy, safety debates far from settled" source_id="12830" jonas_type="http" description="WASHINGTON &amp;mdash; The State Department minimized the climate change impact of building the Keystone XL pipeline in its final environmental review issued on Friday, a key finding as President Barack Obama decides whether to approve the controversial project. Olivier Douliery | Abaca Press/MCT Activists engage in civil disobedience Wednesday, February 13, 2013 at the White House in Washington, D.C., in hopes of pressuring President Barack Obama to reject the Keystone XL oil sands pipeline. http://media.mcclatchydc.com/smedia/2014/01/31/17/06/SoIRM.La.91.jpg &quot; style=&quot;border-left:2px solid #dddddd; padding-left:5px;max-width:100%;&quot;&gt; More News Read more Politics However, the review leaves the..." feed_url="http://rss.wn.com/english/keyword/" original_request_url="http://article.wn.com/view/2014/02/01/Keystone_report_leaves_environmental_energy_safety_debates_f_1/" content_type="text/html">
                            <wl:sentence wl:pos="NN NN NN" wl:significance="0.0" wl:id="f30f3372bd5ecbebf8dc9ed6a37ea620" wl:token="0,6 7,12 13,19"><![CDATA[Energy Obama Barack]]></wl:sentence>
                            <wl:annotation
                                wl:annotationType="PersonEntity"
                                wl:key="some.url.com"
                                wl:surfaceForm="Obama"
                                wl:start="0"
                                wl:end="10"
                                wl:md5sum="0c8cb136073a20a932f2d6748204ce9b">
                            </wl:annotation></wl:page>''']
# 
        matview_name = 'climate2_media'
        if self.service_is_online:
            result = self.jesaja.get_keyword_annotations(matview_name, xml_documents)
            assert len(result)
            assert '495692737' in result
            assert len(result['495692737'])

#     def test_get_keywords(self):
#         xml_documents = ['''<wl:page xmlns:wl="http://www.weblyzard.com/wl/2013#" wl:id="495692737" xml:lang="en" wl:nilsimsa="5bb001c8a610a105b1120bb9c4889d33c62b19e1493245cc2f252a83e270646b" title="Keystone report leaves environmental, energy, safety debates far from settled" source_id="12830" jonas_type="http" description="WASHINGTON &amp;mdash; The State Department minimized the climate change impact of building the Keystone XL pipeline in its final environmental review issued on Friday, a key finding as President Barack Obama decides whether to approve the controversial project. Olivier Douliery | Abaca Press/MCT Activists engage in civil disobedience Wednesday, February 13, 2013 at the White House in Washington, D.C., in hopes of pressuring President Barack Obama to reject the Keystone XL oil sands pipeline. http://media.mcclatchydc.com/smedia/2014/01/31/17/06/SoIRM.La.91.jpg &quot; style=&quot;border-left:2px solid #dddddd; padding-left:5px;max-width:100%;&quot;&gt; More News Read more Politics However, the review leaves the..." feed_url="http://rss.wn.com/english/keyword/" original_request_url="http://article.wn.com/view/2014/02/01/Keystone_report_leaves_environmental_energy_safety_debates_f_1/" content_type="text/html">
#                             <wl:sentence wl:pos="NN NN NN" wl:significance="0.0" wl:id="f30f3372bd5ecbebf8dc9ed6a37ea620" wl:token="0,6 7,12 13,19"><![CDATA[Energy Obama Barack]]></wl:sentence>
#                         </wl:page>''']
#  
#         matview_name = 'climate2_media'
#         if self.service_is_online:
#             result = self.jesaja.get_keywords(matview_name, xml_documents)
#             assert len(result)
#             assert '495692737' in result
#             assert len(result['495692737'])
        
if __name__ == '__main__':
    unittest.main()

