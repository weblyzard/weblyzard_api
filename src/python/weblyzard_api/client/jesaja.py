# -*- coding: utf8 -*
'''
.. codeauthor: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
.. codeauthor:: Heinz-Peter Lang <lang@weblyzard.com>
'''

import unittest
from gzip import GzipFile
from cPickle import load

from eWRT.ws.rest import MultiRESTClient 

from weblyzard_api.xml_content import XMLContent
from weblyzard_api.client import WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS
from weblyzard_api.test import get_full_path

class Jesaja(MultiRESTClient):
    ''' 
    Provides access to the Jesaja keyword service. 

    Jesaja extracts associations (i.e. keywords) from text documents.
    '''
    
    VALID_CORPUS_FORMATS = ('xml', 'csv')
    URL_PATH = 'jesaja/rest'
    ATTRIBUTE_MAPPING = {'content_id': 'id', 
                         'title': 'title', 
                         'sentences': 'sentence',
                         'body_annotations': 'body_annotation',
                         'lang': 'xml:lang',
                         'sentences_map': {'pos': 'pos',
                                           'token': 'token', 
                                           'value': 'value',
                                           'md5sum': 'id'},
                         'annotations_map': {'start':'start',
                                             'end':'end',
                                             'key':'key',
                                             'surfaceForm':'surfaceForm'
                                             }}
    
    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER, 
                 pwd=WEBLYZARD_API_PASS, default_timeout=None):
        '''
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        '''
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd,
                                 default_timeout=default_timeout)
        
    @classmethod
    def get_documents(cls, xml_content_dict):
        ''' 
        converts a list of weblyzard xml files to the 
        json format required by the jesaja web service.
        '''
        if not isinstance(xml_content_dict, list):
            xml_content_dict = [xml_content_dict]
        return [cls.convert_document(xml) for xml in xml_content_dict]

    @classmethod
    def convert_document(cls, xml):
        ''' converts an XML String to a dictionary with the correct parameters
        (ignoring non-sentences and adding the titles 

        :param xml: str representing the document
        :returns: converted document
        :rtype: dict
        '''
        if isinstance(xml, dict):
            return xml
        
        if not isinstance(xml, XMLContent):
            xml = XMLContent(xml)
        
        return xml.as_dict(mapping=cls.ATTRIBUTE_MAPPING,
                           ignore_non_sentence=True, 
                           add_titles_to_sentences=True)
    
    def add_profile(self, profile_name, keyword_calculation_profile):
        ''' Add a keyword profile to the server

        :param profile_name: the name of the keyword profile
        :param keyword_calculation_profile: the full keyword calculation \
            profile (see below).

        .. note:: Example keyword calculation profile

            ::

                { 
                    'valid_pos_tags'                 : ['NN', 'P', 'ADJ'],
                    'corpus_name'                    : reference_corpus_name,
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
        return self.request('add_or_refresh_profile/%s' % profile_name,
                            keyword_calculation_profile)

    def add_or_update_corpus(self, corpus_name, corpus_format, corpus, 
                             profile_name=None, skip_profile_check=False):
        ''' 
        Adds/updates a corpus at Jesaja.

        :param corpus_name: the name of the corpus
        :param corpus_format: either 'csv', 'xml', or wlxml
        :param corpus: the corpus in the given format.
        :param profile_name: the name of the profile used for tokenization \
            (only used in conjunction with corpus_format 'doc').

        .. note:: Supported ``corpus_format``

            * csv
            * xml
            * wlxml::

                # xml_content: the content in the weblyzard xml format
                corpus = [ xml_content, ... ]  
                 
        .. attention:: uploading documents (corpus_format = doc, wlxml) \
            requires a call to finalize_corpora to trigger the corpus generation!         
        '''
        assert corpus_format in self.VALID_CORPUS_FORMATS
        path = None
        
        if not profile_name: 
            profile_name = corpus_name
        
        # convert the wlxml format to doc, if required
        if corpus_format == 'xml':
            if profile_name is None:
                raise ValueError, 'Corpus_format "xml" requires spezifying a profile for tokenization'
            elif not skip_profile_check and not self.has_profile(profile_name):
                raise ValueError, 'profile "%s" missing!' % (profile_name)

            corpus = self.get_documents(corpus)    
            path = 'add_or_refresh_corpus/doc/%s/%s' % (corpus_name, 
                                                        profile_name) 
        # handle csv corpora
        elif corpus_format == 'csv':
            path = 'add_or_refresh_corpus/csv/%s' % corpus_name
        elif corpus_format == 'doc':
            raise Exception('Format "doc" not supported anymore')
        else:
            raise ValueError, "Unsupported format."
        
        return self.request(path, corpus)

    def get_keywords_xml(self, profile_name, documents):
        ''' converts each document to a dictionary and calculates the \
            keywords''' 
        documents = self.get_documents(documents)
        return self.get_keywords(profile_name, documents)

    def get_keywords(self, profile_name, documents):
        ''' 
        :param profile_name: keyword profile to use 
        :param documents: a list of webLyzard xml documents to annotate

        .. note:: example documents list

            ::

                documents = [
                  {
                     'title': 'Test document',
                     'sentence': [
                         {
                           'id': '27150b5fae553ebab63332fe7b94d518',
                           'pos': 'NNP VBZ VBN IN VBZ NNP . NNP VBZ NNP .',
                           'token': '0,5 6,8 9,16 17,19 20,27 28,43 43,44 45,48 49,54 55,61 61,62',
                           'value': 'CDATA is wrapped as follows <![CDATA[aha]]>. Ana loves Martin.'
                         },
                         {
                           'id': 'f8ddd9b3c8cf4c7764a3348d14e84e79',
                           'pos': 'NN IN CD \' IN JJR JJR JJR JJR CC CC CC : : JJ NN .',
                           'token': '0,4 5,7 8,9 10,11 12,16 17,18 18,19 19,20 20,21 22,23 23,24 25,28 29,30 30,31 32,39 40,45 45,46',
                           'value': '10µm in € ” with <><> && and // related stuff.'
                         }
                     ],
                     'content_id': '123k233',
                     'lang': 'en',
                     }
                ]
        '''
        if not self.has_profile(profile_name):
            raise Exception('Cannot compute keywords - unknown profile %s' % profile_name)
        return self.request('get_keywords/%s' % profile_name, documents)

    def has_profile(self, profile_name):
        return profile_name in self.list_profiles()

    def list_profiles(self):
        return self.request('list_profiles')

    def get_cache_stats(self):
        return self.request('get_cache_stats', return_plain=True)

    def get_cached_corpora(self):
        return self.request('get_cached_corpora')

    def get_corpus_size(self, profile_name):
        return self.request('get_corpus_size/%s' % profile_name) 

    def add_or_update_stoplist(self, name, stoplist):
        '''
        .. deprecated:: 0.1
           Use: :func:`add_stoplist` instead.
        '''
        return self.add_stoplist(name, stoplist) 

    def add_stoplist(self, name, stoplist):
        '''
        :param name: name of the stopword list
        :param stoplist: a list of stopwords for the keyword computation
        '''
        return self.request('add_or_update_stoplist/%s' % name, stoplist) 

    def list_stoplists(self):
        '''
        :returns: a list of all available stopword lists.
        '''
        return self.request('list_stoplists')
    
    def change_log_level(self, level):
        '''
        Changes the log level of the keyword service

        :param level: the new log level to use.
        '''
        return self.request('set_log_level/%s' % level, return_plain=True)

    def finalize_corpora(self):
        '''
        .. note::

           This function needs to be called after uploading 'doc' or 'wlxml'
           corpora, since it triggers the computations of the token counts
           based on the 'valid_pos_tags' parameter.
        '''
        return self.request('finalize_corpora', return_plain=True)

    def finalize_profile(self, profile_name):
        return self.request('finalize_profile/%s' % profile_name, 
                            return_plain=True)

    def meminfo(self):
        return self.request('meminfo')

class JesajaTest(unittest.TestCase):

    PROFILE_NAME = 'default'
    STOPLIST_PROFILE_NAME = 'stoplist'
    CORPUS_NAME  = 'test_corpus'
    SAMPLE_DATA_FILE = get_full_path('xml_documents.pickle.gz')
     
    PROFILE = { 
        'valid_pos_tags'                 : ['NN'],#['NN', 'P', 'ADJ'],
        'corpus_name'                    : CORPUS_NAME,
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
        self.jesaja = Jesaja()
        self.service_is_online = self.jesaja.is_online()
        
        if self.service_is_online:
            
            STOPLIST_PROFILE = self.PROFILE.copy()
            STOPLIST_PROFILE['stoplists'] = ['testList', 'anotherList']
     
            with GzipFile(self.SAMPLE_DATA_FILE) as f:
                sample_corpus = load(f)
                print 'Loaded corpus with %d entries' % (len(sample_corpus))
     
            self.jesaja.add_stoplist('testList', 
                                     ('the', 'from', 'there', 'here') )
            self.jesaja.add_stoplist('anotherList', 
                                     ('you', 'he', 'she', 'it', 'them'))
            self.jesaja.add_profile(self.PROFILE_NAME, self.PROFILE)
            self.jesaja.add_profile(self.STOPLIST_PROFILE_NAME, STOPLIST_PROFILE)
      
            csv_corpus = {'ana': 12, 'tom': 22, 'petra': 3}
            self.jesaja.add_or_update_corpus(self.CORPUS_NAME, 'csv', csv_corpus )
            self.jesaja.add_or_update_corpus(self.CORPUS_NAME, 'xml', sample_corpus, 
                                            self.PROFILE_NAME)
     
            self.jesaja.finalize_corpora()
            size_default = self.jesaja.get_corpus_size(self.PROFILE_NAME)
            size_stoplist = self.jesaja.get_corpus_size(self.STOPLIST_PROFILE_NAME)
            print 'Corpus "default" - corpus size : ', size_default
            print 'Corpus "stoplist" - corpus size: ', size_stoplist
     
        else: 
            print 'WARNING: Webservice is offline --> not executing all tests!!'
            
    def test_server_is_online(self):
        ''' tests if the server is online ''' 
        assert self.jesaja.is_online(), 'server not online!!!'
            
    def test_get_keywords(self):
        ''' tests the keywords computation '''
        if self.service_is_online:
            docs = {'doc12': {'sentences': {'c000': 'Good day to the lord!',
                                            'c001': 'How are you?'},
                              'pos_tags' : {'c000': 'JJ NN TO DT NN',
                                            'c001': 'WRB NNS PRP'} }
                    }
            print self.jesaja.get_keywords(self.PROFILE_NAME, docs)
 
    def test_loglevel(self):
        if self.service_is_online:
            print self.jesaja.change_log_level('severe')
 
    def test_meminfo(self):
        if self.service_is_online:
            print self.jesaja.meminfo()
 
    def test_profile_list(self):
        if self.service_is_online:
            self.assertTrue( self.jesaja.has_profile(self.PROFILE_NAME) )
            self.assertFalse( self.jesaja.has_profile('unknown'))
         
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
