#!/usr/bin/python
# -*- coding: utf-8 -*-
'''

'''
import unittest

from gzip import GzipFile
from cPickle import load

from weblyzard_api.client.jesaja import Jesaja
from weblyzard_api.xml_content import XMLContent

from weblyzard_api.tests.test_helper import get_full_path


class JesajaTest(unittest.TestCase):

    PROFILE_NAME = 'default'
    STOPLIST_PROFILE_NAME = 'stoplist'
    CORPUS_NAME = 'test_corpus'
    SAMPLE_DATA_FILE = get_full_path('xml_documents.pickle.gz')

    PROFILE = {
        'valid_pos_tags': ['NN'],  # ['NN', 'P', 'ADJ'],
        'corpus_name': CORPUS_NAME,
        'min_phrase_significance': 2.0,
        'num_keywords': 5,
        # com.weblyzard.backend.jesaja.algorithm.keywords.LogLikelihoodKeywordSignificanceAlgorithm
        'keyword_algorithm': 'com.weblyzard.backend.jesaja.algorithm.keywords.YatesKeywordSignificanceAlgorithm',
        'min_token_count': 5,
        'skip_underrepresented_keywords': True,
        'stoplists': [],
    }

    def setUp(self):
        '''
        Setup Jesaja Keyword Server
        '''
        self.jesaja = Jesaja()
        self.service_is_online = self.jesaja.is_online()

        if self.service_is_online:

            STOPLIST_PROFILE = self.PROFILE.copy()
            STOPLIST_PROFILE['stoplists'] = ['testList', 'anotherList']

            with GzipFile(self.SAMPLE_DATA_FILE) as f:
                sample_corpus = load(f)
                print('Loaded corpus with %d entries' % (len(sample_corpus)))

            self.jesaja.add_stoplist('testList',
                                     ('the', 'from', 'there', 'here'))
            self.jesaja.add_stoplist('anotherList',
                                     ('you', 'he', 'she', 'it', 'them'))
            self.jesaja.add_profile(self.PROFILE_NAME, self.PROFILE)
            self.jesaja.add_profile(
                self.STOPLIST_PROFILE_NAME, STOPLIST_PROFILE)

            csv_corpus = {'ana': 12, 'tom': 22, 'petra': 3}
            self.jesaja.add_or_update_corpus(
                self.CORPUS_NAME, 'csv', csv_corpus)
            self.jesaja.add_or_update_corpus(self.CORPUS_NAME, 'xml', sample_corpus,
                                             self.PROFILE_NAME)

            self.jesaja.finalize_corpora()
            size_default = self.jesaja.get_corpus_size(self.PROFILE_NAME)
            size_stoplist = self.jesaja.get_corpus_size(
                self.STOPLIST_PROFILE_NAME)
            print('Corpus "default" - corpus size : ', size_default)
            print('Corpus "stoplist" - corpus size: ', size_stoplist)

        else:
            print('WARNING: Webservice is offline --> not executing all tests!!')

    def test_server_is_online(self):
        ''' tests if the server is online '''
        assert self.jesaja.is_online(), 'server not online!!!'

    def test_get_keywords(self):
        ''' tests the keywords computation '''
        if self.service_is_online:
            docs = {'doc12': {'sentences': {'c000': 'Good day to the lord!',
                                            'c001': 'How are you?'},
                              'pos_tags': {'c000': 'JJ NN TO DT NN',
                                           'c001': 'WRB NNS PRP'}}
                    }
            print(self.jesaja.get_keywords(self.PROFILE_NAME, docs))

    def test_loglevel(self):
        if self.service_is_online:
            print(self.jesaja.change_log_level('severe'))

    def test_meminfo(self):
        if self.service_is_online:
            print(self.jesaja.meminfo())

    def test_profile_list(self):
        if self.service_is_online:
            self.assertTrue(self.jesaja.has_profile(self.PROFILE_NAME))
            self.assertFalse(self.jesaja.has_profile('unknown'))

    def test_convert_document(self):
        xml = '''<wl:page xmlns:wl="http://www.weblyzard.com/wl/2005" content_id="495692737" lang="en" nilsimsa="5bb001c8a610a105b1120bb9c4889d33c62b19e1493245cc2f252a83e270646b" title="Keystone report leaves environmental, energy, safety debates far from settled" source_id="12830" jonas_type="http" description="WASHINGTON &amp;mdash; The State Department minimized the climate change impact of building the Keystone XL pipeline in its final environmental review issued on Friday, a key finding as President Barack Obama decides whether to approve the controversial project. Olivier Douliery | Abaca Press/MCT Activists engage in civil disobedience Wednesday, February 13, 2013 at the White House in Washington, D.C., in hopes of pressuring President Barack Obama to reject the Keystone XL oil sands pipeline. http://media.mcclatchydc.com/smedia/2014/01/31/17/06/SoIRM.La.91.jpg &quot; style=&quot;border-left:2px solid #dddddd; padding-left:5px;max-width:100%;&quot;&gt; More News Read more Politics However, the review leaves the..." feed_url="http://rss.wn.com/english/keyword/" original_request_url="http://article.wn.com/view/2014/02/01/Keystone_report_leaves_environmental_energy_safety_debates_f_1/" content_type="text/html">
   <wl:sentence pos_tags="None" sem_orient="0.0" significance="0.0" md5sum="f30f3372bd5ecbebf8dc9ed6a37ea620" pos="None" token="0,6"><![CDATA[Kirche]]></wl:sentence>     
   <wl:sentence pos_tags="None" sem_orient="0.0" significance="12951.7567942" md5sum="0c8cb136073a20a932f2d6748204ce9b" pos="NNP CD ( NN ) : DT NNP NNP POS JJ JJ NN IN DT NN NN IN DT JJ NN NNS TO DT NNP NNP NNP VBZ VBN PRP VBP IN DT JJ CC JJ NN IN NNP NNP VBZ DT NN IN DT NN ." token="0,4 5,7 8,9 9,18 18,19 20,22 23,26 27,32 33,43 43,45 46,51 52,65 66,76 77,79 80,83 84,92 93,101 102,106 107,110 111,119 120,123 124,129 130,132 133,136 137,141 142,146 147,152 153,155 156,158 159,161 162,166 167,169 170,173 174,187 188,191 192,201 202,208 209,211 212,221 222,227 228,239 240,243 244,256 257,259 260,263 264,272 272,273"><![CDATA[Dec. 23 (Bloomberg) -- The State Department's final environmental assessment of the Keystone pipeline from the Canadian tar sands to the U.S. Gulf Coast is c. We look at the environmental and political impact if President Obama greenlights the construction of the pipeline.]]></wl:sentence>
   <wl:sentence pos_tags="None" sem_orient="0.0" significance="0.0" md5sum="cdc2b1edeec27081819ca4f50e067240" pos="NNP NNP VBZ VBN IN NNS : NNS ." token="0,6 7,15 16,18 19,25 26,28 29,35 35,36 37,42 42,43"><![CDATA[Shihab Rattansi is joined by guests: clima.]]></wl:sentence>
   </wl:page>'''

        result1 = Jesaja.convert_document(xml)
        assert len(result1['sentence']) == 2
        assert 'id' in result1

        xml_obj = XMLContent(xml)
        result2 = Jesaja.convert_document(xml_obj)
        assert result1 == result2


if __name__ == '__main__':
    unittest.main()
