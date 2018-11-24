#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Aug 29, 2016

.. codeauthor: max goebel <mcgoebel@gmail.com>
'''
import unittest

from gzip import GzipFile
from cPickle import load

from weblyzard_api.client.jesaja_ng import JesajaNg
from weblyzard_api.tests.test_helper import get_full_path


class JesajaNgTest(unittest.TestCase):

    JESAJA_URL = 'http://localhost:63002/rest/'
    PROFILE_NAME = 'default'
    STOPLIST_PROFILE_NAME = 'stoplist'
    CORPUS_NAME = 'test_corpus'
    MATVIEW_NAME = 'unittest'
    SAMPLE_DATA_FILE = get_full_path('xml_documents.pickle.gz')
    SAMPLE_DATA_FILE = get_full_path(
        'xml_documents_international_media.pickle.gz')

    PROFILE = {
        'valid_pos_tags': ['NN', 'NNP', 'NNS'],  # ['NN', 'P', 'ADJ'],
        'required_pos_tags': [],
        'min_phrase_significance': 2.0,
        'num_keywords': 5,
        'keyword_algorithm': 'com.weblyzard.backend.jesaja.algorithm.keywords.YatesKeywordSignificanceAlgorithm',
        'min_token_count': 1,
        'min_ngram_length': 1,
        'max_ngram_length': 3,
        'skip_underrepresented_keywords': False,
        'ground_annotations': True,
        'stoplists': [],
    }

    def setUp(self):
        '''
        Setup Jesaja Keyword Server
        '''
        self.jesaja = JesajaNg(url=self.JESAJA_URL)
        self.service_is_online = self.jesaja.is_online()

        if self.service_is_online:

            STOPLIST_PROFILE = self.PROFILE.copy()
            STOPLIST_PROFILE['stoplists'] = ['testList', 'anotherList']

            with GzipFile(self.SAMPLE_DATA_FILE) as f:
                sample_corpus = load(f)
                print('Loaded corpus with %d entries' % (len(sample_corpus)))

            self.jesaja.set_stoplist('testList',
                                     ('the', 'from', 'there', 'here'))
            self.jesaja.set_stoplist('anotherList',
                                     ('you', 'he', 'she', 'it', 'them'))
            self.jesaja.set_keyword_profile(self.PROFILE_NAME, self.PROFILE)
            self.jesaja.set_keyword_profile(
                self.STOPLIST_PROFILE_NAME, STOPLIST_PROFILE)
            self.jesaja.set_matview_profile(
                self.MATVIEW_NAME, self.PROFILE_NAME)

            # create the reference corpus
            if not self.jesaja.has_corpus(matview_id=self.MATVIEW_NAME):
                while self.jesaja.rotate_shard(matview_id=self.MATVIEW_NAME) == 0:
                    csv_corpus = {'keystone': 25, 'energy': 123, 'ana': 12,
                                  'tom': 22, 'petra': 3, 'clima': 5, 'Shihab': 12, 'Kirche': 10}
                    self.jesaja.add_csv(
                        matview_id=self.MATVIEW_NAME, keyword_count_map=csv_corpus)
                    self.jesaja.add_documents(
                        matview_id=self.MATVIEW_NAME, xml_documents=sample_corpus)
        else:
            print('WARNING: Webservice is offline --> not executing all tests!!')

    def test_server_is_online(self):
        ''' tests if the server is online '''
        assert self.jesaja.is_online(), 'server not online!!!'

#     def test_matview_list(self):
#         if self.service_is_online:
#             self.assertTrue(self.jesaja.has_matview(self.MATVIEW_NAME) )
#             self.assertFalse(self.jesaja.has_matview('unknown'))

    def test_get_neks(self):

        xml_documents = ['''<wl:page xmlns:wl="http://www.weblyzard.com/wl/2013#" wl:id="495692737" xml:lang="en" wl:nilsimsa="5bb001c8a610a105b1120bb9c4889d33c62b19e1493245cc2f252a83e270646b" title="Keystone report leaves environmental, energy, safety debates far from settled" source_id="12830" jonas_type="http" description="WASHINGTON &amp;mdash; The State Department minimized the climate change impact of building the Keystone XL pipeline in its final environmental review issued on Friday, a key finding as President Barack Obama decides whether to approve the controversial project. Olivier Douliery | Abaca Press/MCT Activists engage in civil disobedience Wednesday, February 13, 2013 at the White House in Washington, D.C., in hopes of pressuring President Barack Obama to reject the Keystone XL oil sands pipeline. http://media.mcclatchydc.com/smedia/2014/01/31/17/06/SoIRM.La.91.jpg &quot; style=&quot;border-left:2px solid #dddddd; padding-left:5px;max-width:100%;&quot;&gt; More News Read more Politics However, the review leaves the..." feed_url="http://rss.wn.com/english/keyword/" original_request_url="http://article.wn.com/view/2014/02/01/Keystone_report_leaves_environmental_energy_safety_debates_f_1/" content_type="text/html">
                            <wl:sentence wl:pos="NN NN NN" wl:significance="0.0" wl:id="f30f3372bd5ecbebf8dc9ed6a37ea620" wl:token="0,6 7,14 15,18"><![CDATA[Energy Twitter Dog]]></wl:sentence>
                            <wl:annotation
                                wl:entity_type="OrganizationEntity"
                                wl:key="http://dbpedia.org/resource/Twitter"
                                wl:preferredName="Twitter Inc."
                                wl:surfaceForm="Twitter"
                                wl:start="0"
                                wl:end="10"
                                wl:md5sum="0c8cb136073a20a932f2d6748204ce9b">
                            </wl:annotation></wl:page>''']
#
        matview_name = self.MATVIEW_NAME
        if self.service_is_online:
            result = self.jesaja.get_keyword_annotations(
                matview_name, xml_documents)
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
