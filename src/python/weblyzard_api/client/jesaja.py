# -*- coding: utf8 -*
'''
.. codeauthor: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
.. codeauthor:: Heinz-Peter Lang <lang@weblyzard.com>
'''

from eWRT.ws.rest import MultiRESTClient 

from weblyzard_api.xml_content import XMLContent
from weblyzard_api.client import WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS


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


