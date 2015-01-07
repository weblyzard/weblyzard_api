'''
.. codeauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
.. codeauthor:: Heinz-Peter Lang <lang@weblyzard.com>
'''
import unittest
from time import time
from sys import argv

from eWRT.ws.rest import MultiRESTClient
from weblyzard_api.xml_content import XMLContent
from weblyzard_api.client import WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS

class Jeremia(MultiRESTClient):
    '''
    **Jeremia Web Service**

    Pre-processes text documents and returns an annotated webLyzard XML document.

    **Blacklisting**

    Blacklisting is an optional service which removes sentences which occur
    multiple times in different documents from these documents. Examples for such
    sentences are document headers or footers.

    The following functions handle sentence blacklisting:

     * :func:`clear_blacklist`
     * :func:`get_blacklist`
     * :func:`submit_document_blacklist`
     * :func:`update_blacklist`

    Jeremia returns a 
    :doc:`webLyzard XML document <weblyzard_api.data_format.xml_format>`.
    The weblyzard_api provides the class :class:`.XMLContent` to process
    and manipulate the weblyzard XML documents.:

    .. note:: Example usage

        .. code-block:: python

            from weblyzard_api.client.recognize import Recognize
            from pprint import pprint

            docs = {'id': '192292', 
                    'title': 'The document title.', 
                    'body': 'This is the document text...', 
                    'format': 'text/html', 
                    'header': {}}
            client = Jeremia()
            result = client.submit_document(docs)
            pprint(result)
    '''
    URL_PATH = 'jeremia/rest'
    ATTRIBUTE_MAPPING = {'content_id': 'id', 
                         'title': 'title', 
                         'sentences': 'sentence',
                         'lang': 'lang',
                         'sentences_map': {'pos': 'pos',
                                           'token': 'token', 
                                           'value': 'value',
                                           'md5sum': 'id'}}
    
    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER, pwd=WEBLYZARD_API_PASS):
        '''
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        '''
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd)


    def commit(self, batch_id):
        ''' 
        :param batch_id: the batch_id to retrieve 
        :return: a generator yielding all the documents of that particular batch 
        '''
        while True:
            result = self.request('commit/%s' % batch_id)
            if not result:
                break
            else:
                for doc in result:
                    yield doc
                    
    def submit_document(self, document):
        '''
        processes a single document with jeremia (annotates a single document)

        :param document: the document to be processed
        '''
        return self.request('submit_document', document)
    
    def submit_documents(self, batch_id, documents):
        ''' 
        :param batch_id: batch_id to use for the given submission
        :param documents: a list of dictionaries containing the document 
        '''
        if not documents:
            raise ValueError('Cannot process an empty document list')
        return self.request('submit_documents/%s' % batch_id, documents)
    
    def status(self):
        '''
        :returns: the status of the Jeremia web service.
        '''
        return self.request('status', return_plain=True)

    def version(self):
        '''
        :returns: the current version of the jeremia deployed on the server
        '''
        return self.request('version', return_plain=True)
    
    def get_xml_doc(self, text, content_id='1'):
        '''
        Processes text and returns a XMLContent object.

        :param text: the text to process
        :param content_id: optional content id
        '''
        batch = [{'id': content_id, 
                  'title': '', 
                  'body': text, 
                  'format': 'text/plain'}]
        
        batch_id = str(time())
        self.submit_documents(batch_id, batch)
        results = list(self.commit(batch_id))
        result = results[0]
        return XMLContent(result['xml_content'])
    
    def submit_documents_blacklist(self, batch_id, documents, source_id):
        ''' submits the documents and removes blacklist sentences 

        :param batch_id: batch_id to use for the given submission
        :param documents: a list of dictionaries containing the document 
        :param source_id: source_id for the documents, determines the blacklist
        '''
        url = 'submit_documents_blacklist/%s/%s' % (batch_id, source_id)
        return self.request(url, documents)
    
    def update_blacklist(self, source_id, blacklist):
        ''' 
        updates an existing blacklist cache 

        :param source_id: the blacklist's source id
        '''
        url = 'cache/updateBlacklist/%s' % source_id
        return self.request(url, blacklist)
        
    def clear_blacklist(self, source_id):
        ''' 
        :param source_id: the blacklist's source id

        Empties the existing sentence blacklisting cache for the given source_id
        ''' 
        return self.request('cache/clearBlacklist/%s' % source_id)
        
    def get_blacklist(self, source_id):
        ''' 
        :param source_id: the blacklist's source id
        :returns: the sentence blacklist for the given source_id''' 
        return self.request('cache/getBlacklist/%s' % source_id)

    def submit(self, batch_id, documents, source_id=None, use_blacklist=False):
        ''' Convenience function to submit documents. The function will submit
        the list of documents and finally call commit to retrieve the result

        :param batch_id: ID of the batch
        :param documents: list of documents (dict)
        :param source_id: 
        :param use_blacklist: use the blacklist or not 
        :returns: result as a list with dicts
        '''
        if use_blacklist: 
            if not source_id:
                raise Exception('Blacklist requires a source_id')
        
            url = 'submit_documents_blacklist/%s/%s' % (batch_id, source_id)
        else: 
            url = 'submit_documents/%s' % batch_id
            
        self.request(url, documents)
        
        return self.commit(batch_id) 

class JeremiaTest(unittest.TestCase):

    DOCS = [ {'id': content_id,
              'body': 'Good day Mr. President! Hello "world" ' + str(content_id),
              'title': 'Hello "world" more ',
              'format': 'text/html',
              'header': {}}  for content_id in xrange(1000,1020)]
    
                      
    def test_single_document_processing(self):
        j = Jeremia()
        print 'submitting document...'
        document_annotated = j.submit_document(self.DOCS[1])
        self.assertTrue(document_annotated != "")
    
    def test_single_document_with_annotations(self):
        '''
        Tests the handling of single document annotations.
        '''
        DOC = {'id'    : 12,
               'body'  : 'UBS has finally succeeded. They obtained a 10% share of CS.',
               'title' : 'UBS versus Credit Suisse.',
               'format': 'text/html',
               'title_annotation': [{'start': 0, 'end': 3, 'surfaceForm': 'UBS', 'key': 'http://dbpedia.org/UBS'},
                                    {'start':11, 'end':24, 'surfaceForm': 'Credit Suisse', 'key': 'http://dbpedia.org/Credit Suisse'}],
               'body_annotation' : [{'start': 0, 'end': 3, 'surfaceForm': 'UBS', 'key': 'http://dbpedia.org/UBS'},
                                    {'start':56, 'end':58, 'surfaceForm': 'CS', 'key': 'http://dbpedia.org/Credit Suisse'}],
               'header': {},
              }


        j = Jeremia()

        # this test requires Jeremia version 0.0.4+ 
        if j.version() < "0.0.4":
            return


        print 'submitting document with annotations...'
        result = j.submit_document(DOC)

        # check: all annotations have been preserved
        print result
        assert len(result['annotation']) == 4

        # check: annotations
        for annotation in result['annotation']:
            # title
            if annotation['md5sum'] == '8e3f3deac5e6c01dab521c07e3a60d7b':
                assert annotation['start'] == 0 or annotation['start'] == 11
                assert annotation['end'] == 3 or annotation['end'] == 24
            # first body sentence
            elif annotation['md5sum'] == 'ffafdc744dcda3d58ab6eafc86ad99b1':
                assert annotation['start'] == 0
                assert annotation['end'] == 3
            # second body sentence with adjusted indices
            elif annotation['md5sum'] == '25faaf0960a68ae741125ca436b330ee':
                assert annotation['start'] == 29
                assert annotation['end'] == 31

    def test_batch_processing(self):
        j = Jeremia()
        print 'Submitting documents...'
        j.submit_documents('1234', self.DOCS[:10])
        j.submit_documents('1234', self.DOCS[10:])
        
        # retrieve initial patch 
        print 'Retrieving results...'
        docs = list(j.commit('1234'))
        self.assertEqual(len(docs), 20)
        
        # no more results are available
        self.assertEqual(len(list(j.commit('1234'))), 0)

    def test_sentence_splitting(self):
        j = Jeremia()
        j.submit_documents( '1222', self.DOCS[:1] )

        for doc in j.commit('1222'):
            # extract sentences
            xml_obj = XMLContent(doc['xml_content'])
            sentences = [s.sentence for s in xml_obj.sentences]
            print doc['xml_content']
            assert 'wl:is_title' in doc['xml_content']
            print sentences
            
            # TODO: check sentence splitting in jeremia! 
            # self.assertEqual(len(sentences), 3)

    def test_illegal_xml_format_filtering(self):
        DOCS = [ {'id': 'alpha',
                  'body': 'This is an illegal XML Sequence: J\x1amica',
                  'title': 'Hello "world" more ',
                  'format': 'text/html',
                  'header': {}} ]

        j = Jeremia()
        j.submit_documents( '12234', DOCS )
        for doc in list(j.commit('12234')):
            xml = XMLContent(doc['xml_content'])
            print doc['xml_content']
            assert xml.sentences[0].sentence != None
       
    def test_illegal_input_args(self):
        j = Jeremia()

        with self.assertRaises(ValueError):
            j.submit_documents('1223', [])
    
    def test_submit(self):
        j = Jeremia()
        result = j.submit(batch_id='meh1234', 
                          documents=self.DOCS, 
                          use_blacklist=False)
        assert len(list(result)), 'result is empty'
        
if __name__ == '__main__':
    if len(argv) > 1:
        txt = argv[1]
        docs = {'id': '192292', 
                'body': txt, 
                'title': '', 
                'format': 'text/html', 
                'header': {}}
        j = Jeremia()
        docs['body_annotation'] = [{'start':0, 'end': 3, 'key': 'test annotation'}]
        l = j.submit_document(docs)
        print l
    else:
        unittest.main()
