# -*- coding: utf8 -*
'''
Created on Jan 23, 2013

@author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''

from unittest import main, TestCase
from gzip import GzipFile
from cPickle import load
from os.path import join as os_join, dirname

from eWRT.ws.rest import MultiRESTClient 
from weblyzard_api.xml_content import XMLContent
from weblyzard_api.client import WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS

class Jesaja(MultiRESTClient):
    ''' 
    @class Jesaja
    Provides access to the Jesaja keyword service. 
    '''

    VALID_CORPUS_FORMATS = ('xml', 'csv')
    URL_PATH = 'jesaja/rest'
    
    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER, pwd=WEBLYZARD_API_PASS):
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd)

    @staticmethod
    def get_documents(xml_content_dict):
        ''' 
        converts a list of weblyzard xml files to the 
        json format required by the jesaja web service.
        '''
        return [XMLContent(xml).as_dict() for xml in xml_content_dict]

    def add_profile(self, profile_name, keyword_calculation_profile):
        ''' Add a keyword profile to the server
        @param profile_name: the name of the keyword profile
        @param keyword_calculation_profile: the full keyword calculation
                                            profile (example see below).
        <code>
        { 
            'valid_pos_tags'                 : ['NN', 'P', 'ADJ'],
            'corpus_name'                    : reference_corpus_name,
            'min_phrase_significance'        : 2.0,
            'num_keywords'                   : 5,
            'keyword_algorithm'              : 'com.weblyzard.backend.jesaja.algorithm.keywords.YatesKeywordSignificanceAlgorithm', # com.weblyzard.backend.jesaja.algorithm.keywords.LogLikelihoodKeywordSignificanceAlgorithm
            'min_token_count'                : 5,
            'skip_underrepresented_keywords' : True,
            'stoplists'                      : [],
        }
        </code>
        '''
        return self.request('add_or_refresh_profile/%s' % profile_name,
                            keyword_calculation_profile)

    def add_or_refresh_corpus(self,profile_name, corpus, corpus_format, 
                              corpus_name=None):
        ''' for compability reasons ''' 
        
        if not corpus_name: 
            corpus_name = profile_name
            
        return self.add_or_update_corpus(corpus_name=corpus_name, 
                                         corpus_format=corpus_format, 
                                         corpus=corpus, 
                                         profile_name=profile_name)

    def add_or_update_corpus(self, corpus_name, corpus_format, corpus, 
                             profile_name=None):
        ''' 
        Adds/updates a corpus at Jesaja.
        @param corpus_name: the name of the corpus
        @param corpus_format: either 'csv', or 'xml'
        @param corpus: the corpus in the given format.
        @param profile_name: the name of the profile used for tokenization 
                           (only used in conjunction with corpus_format 'doc').

        Supported formats:
        wlxml: [ xml_content, ... ]
                xml_content: the content in the weblyzard xml format
                 
        @attention: uploading documents (corpus_format = doc, wlxml) requires
                    a call to finalize_corpora to trigger the corpus generation!         
        '''
        assert corpus_format in self.VALID_CORPUS_FORMATS
        path = None
        
        # convert the wlxml format to doc, if required
        if corpus_format == 'xml':
            if profile_name is None:
                raise ValueError, 'Corpus_format "doc" requires spezifying a profile for tokenization'
            elif not self.has_profile( profile_name ):
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

    def get_keywords( self, profile_name, documents ):
        ''' 
        @param profile_name: keyword profile to use 
        @param documents: a list of webLyzard xml documents to annotate

        documents = [
          {
             "title": "Test document",
             "sentence": [
                 {
                   "id": "27150b5fae553ebab63332fe7b94d518",
                   "pos": "NNP VBZ VBN IN VBZ NNP . NNP VBZ NNP .",
                   "token": "0,5 6,8 9,16 17,19 20,27 28,43 43,44 45,48 49,54 55,61 61,62",
                   "value": "CDATA is wrapped as follows <![CDATA[aha]]>. Ana loves Martin."
                 },
                 {
                   "id": "f8ddd9b3c8cf4c7764a3348d14e84e79",
                   "pos": "NN IN CD \" IN JJR JJR JJR JJR CC CC CC : : JJ NN .",
                   "token": "0,4 5,7 8,9 10,11 12,16 17,18 18,19 19,20 20,21 22,23 23,24 25,28 29,30 30,31 32,39 40,45 45,46",
                   "value": "10µm in € ” with <><> && and // related stuff."
                 }
             ],
             "content_id": '123k233',
             "lang": "en",
             }
        ]
        '''
        if not self.has_profile(profile_name):
            raise Exception('Cannot compute keywords - unknown profile %s.' % profile_name)
        return self.request('get_keywords/%s' % profile_name, documents)

    def has_profile(self, profile_name):
        return profile_name in self.list_profiles()

    def list_profiles(self):
        return self.request('list_profiles')

    def get_cache_stats(self):
        return self.request('get_cache_stats', return_plain=True)

    def get_cached_corpora(self):
        return self.request("get_cached_corpora")

    def get_corpus_size(self, profile_name):
        return self.request('get_corpus_size', profile_name) 

    def add_or_update_stoplist(self, name, stoplist):
        ''' for backward compability ''' 
        return self.add_stoplist(name, stoplist) 

    def add_stoplist(self, name, stoplist):
        return self.request('add_or_update_stoplist/%s' % name, stoplist) 

    def list_stoplists(self):
        return self.request('list_stoplists')
    
    def change_log_level(self, level):
        '''
        Changes the log level of the keyword service
        '''
        return self.request('set_log_level/%s' % level, return_plain=True)

    def finalize_corpora(self):
        '''
        This function needs to be called after uploading 'doc' or 'wlxml'
        corpora, since it triggers the computations of the token counts
        based on the 'valid_pos_tags' parameter.
        '''
        return self.request('finalize_corpora', return_plain=True)

    def meminfo(self):
        return self.request('meminfo')


class JesajaTest(TestCase):

    PROFILE_NAME = 'default'
    STOPLIST_PROFILE_NAME = 'stoplist'
    CORPUS_NAME  = 'test_corpus'
    SAMPLE_DATA_FILE = os_join(dirname(__file__), 'test/xml_documents.pickle.gz')
    
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
    
        STOPLIST_PROFILE = self.PROFILE.copy()
        STOPLIST_PROFILE['stoplists'] = ['testList', 'anotherList']

        with GzipFile(self.SAMPLE_DATA_FILE) as f:
            sample_corpus = load(f)
            print 'Loaded corpus with %d entries' % (len(sample_corpus))

        

        self.jesaja.add_stoplist('testList',    ('the', 'from', 'there', 'here') )
        self.jesaja.add_stoplist('anotherList', ('you', 'he', 'she', 'it', 'them') )
        self.jesaja.add_profile(self.PROFILE_NAME, self.PROFILE)
        self.jesaja.add_profile(self.STOPLIST_PROFILE_NAME, STOPLIST_PROFILE)
 
        csv_corpus = {'ana': 12, 'tom': 22, 'petra': 3}
        self.jesaja.add_or_update_corpus(self.CORPUS_NAME, 'csv', csv_corpus )
        self.jesaja.add_or_update_corpus(self.CORPUS_NAME, 'xml', sample_corpus, 
                                        self.PROFILE_NAME)

        self.jesaja.finalize_corpora()

        print 'Corpus "default" - corpus size : ', self.jesaja.get_corpus_size(self.PROFILE_NAME)
        print 'Corpus "stoplist" - corpus size: ', self.jesaja.get_corpus_size(self.STOPLIST_PROFILE_NAME)

    #def test_get_keywords(self):
    #    ''' tests the keywords computation '''
    #    docs = {'doc12': {'sentences': {'c000': 'Good day to the lord!',
    #                                    'c001': 'How are you?'},
    #                      'pos_tags' : {'c000': 'JJ NN TO DT NN',
    #                                    'c001': 'WRB NNS PRP'} }
    #            }
    #    print self.jesaja.get_keywords(self.PROFILE_NAME, docs)

    def test_loglevel(self):
        print self.jesaja.change_log_level('severe')

    def test_meminfo(self):
        print self.jesaja.meminfo()

    def test_profile_list(self):
        self.assertTrue( self.jesaja.has_profile(self.PROFILE_NAME) )
        self.assertFalse( self.jesaja.has_profile('unknown'))
        
if __name__ == '__main__':
    main()

