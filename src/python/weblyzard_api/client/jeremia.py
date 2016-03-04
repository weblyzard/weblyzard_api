# -*- coding: utf-8 -*-

'''
.. codeauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
.. codeauthor:: Heinz-Peter Lang <lang@weblyzard.com>
'''
import unittest
import logging
import urllib2
from time import sleep, time
from sys import argv
from random import random

from eWRT.ws.rest import MultiRESTClient
from weblyzard_api.xml_content import XMLContent
from weblyzard_api.client import WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS

logger = logging.getLogger('weblyzard_api.client.jeremia')

# number of seconds to wait if the web service is occupied
# - we stop once either DEFAULT_MAX_RETRY_DELAY or DEFAULT_MAX_RETRY_ATTEMPTS is reached
# . DEFAULT_WAIT_TIME should therefore amount to DEFAULT_MAX_RETRY_DELAY/2 * DEFAULT_MAX_RETRY_ATTEMPTS
DEFAULT_WAIT_TIME = 20 * 60
DEFAULT_MAX_RETRY_DELAY = 20
DEFAULT_MAX_RETRY_ATTEMPTS = 120

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

    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER,
                 pwd=WEBLYZARD_API_PASS, default_timeout=None):
        '''
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        '''
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd,
                                 default_timeout=default_timeout)

    def submit_document(self, document):
        '''
        processes a single document with jeremia (annotates a single document)

        :param document: the document to be processed
        '''
        return self.request('submit_document', document)

    def submit_documents(self, documents, source_id=-1,
                         double_sentence_threshold=10,
                         wait_time=DEFAULT_WAIT_TIME,
                         max_retry_delay=DEFAULT_MAX_RETRY_DELAY,
                         max_retry_attempts=DEFAULT_MAX_RETRY_ATTEMPTS):
        '''
        :param batch_id: batch_id to use for the given submission
        :param documents: a list of dictionaries containing the document
        '''
        if not documents:
            raise ValueError('Cannot process an empty document list')

        request = 'submit_documents/%s/%d' % (source_id, double_sentence_threshold)

        # wait until the web service has available threads for processing
        # the request
        attempts = 0
        start_time = time()
        while time() - start_time < wait_time and attempts < max_retry_attempts:
            # wait until threads are available
            while self.has_queued_threads() and time() - start_time < wait_time:
                sleep(max_retry_delay * random())

            # submit the request
            # - here we need to check for a 502 and 503 error in
            #   case that has_queued_threads has not been
            #   up to date.
            try:
                result = self.request(request, documents,
                                      pass_through_exceptions=True)
                return result
            except (urllib2.HTTPError, urllib2.URLError) as e:
                attempts = attempts + 1

        # this access most certainly causes an exception since the
        # requests above have failed.
        return self.request(request, documents)


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

        results = self.submit_documents(batch)
        result = results[0]
        return XMLContent(result['xml_content'])

    def update_blacklist(self, source_id, blacklist):
        '''
        updates an existing blacklist cache

        :param source_id: the blacklist's source id
        '''
        url = 'cache/update_blacklist/%s' % source_id
        return self.request(url, blacklist)

    def clear_blacklist(self, source_id):
        '''
        :param source_id: the blacklist's source id

        Empties the existing sentence blacklisting cache for the given source_id
        '''
        return self.request('cache/clear_blacklist/%s' % source_id)

    def get_blacklist(self, source_id):
        '''
        :param source_id: the blacklist's source id
        :returns: the sentence blacklist for the given source_id'''
        return self.request('cache/get_blacklist/%s' % source_id)

    def has_queued_threads(self):
        '''
        :returns:
            True if Jeremia still has queued (i.e. unprocessed) threads or
            False otherwise.

        :note:
            Submitting jobs if threads are queued is discouraged, since it
            will slow down the overall performance.
        '''
        try:
            result = self.request('has_queued_threads')
        except Exception as e:
            result = True
        return result


class JeremiaTest(unittest.TestCase):

    DOCS = [ {'id': content_id,
              'body': 'Good day Mr. President! Hello "world" {}'.format(content_id),
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
        docs = j.submit_documents(self.DOCS)
        self.assertEqual(len(docs), 20)


    def test_sentence_splitting(self):
        j = Jeremia()


        for doc in j.submit_documents(self.DOCS[:1]):
            # extract sentences
            print doc
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
        for doc in j.submit_documents(DOCS):
            xml = XMLContent(doc['xml_content'])
            print doc['xml_content']
            assert xml.sentences[0].sentence != None

    def test_illegal_input_args(self):
        j = Jeremia()

        with self.assertRaises(ValueError):
            j.submit_documents([])

    def test_missing_space_tokenattribute(self):
        def text_as_doc(text):
            docs = [ {'id': 'alpha',
                      'body': text,
                      'title': '',
                      'format': 'text/html',
                      'header': {}} ]
            return docs

        j = Jeremia()

        test_texts = {
                'Min. 25 000 Kč - řidiči nákladních automobilů, tahačů a… Úřad práce Písek http://t.co/QowX6PQjrR': 17,
                'Retos de la #RSE (II): 1. Más autocrítica en las memorias de sostenibilidad': 17,
                }

        for text, token_number in test_texts.iteritems():
            result = j.submit_documents(documents=text_as_doc(text))
            res_xml = list(result)[0]['xml_content']
            assert len(list(XMLContent(res_xml).sentences[0].tokens)) == token_number

    def _get_sentences(self, jeremia_result):
        ''' extracts the list of sentences (as text) from an
            jeremia result.
        '''
        result = []
        for json_document in jeremia_result:
            result.append([ s.sentence for s in XMLContent(json_document['xml_content']).sentences ])

        return result

    def test_blacklist(self):
        ''' tests the blacklist-based sentence filtering '''
        source_id = 1
        blacklist = ['6e44889df94d6408bbeeab8837bfbe01', '422d7f2000393b8c50a37f9d363ad511']
        docs = [{'id': 123,
                 'body': 'Hier wird die Zensur zuschlagen. Der zweite Satz ist aber okay.',
                 'title': 'Testdokument :)',
                 'format': 'text/html',
                 'header': {}}]

        # use the blacklist
        j = Jeremia()
        j.update_blacklist(source_id=source_id, blacklist=blacklist)
        sentences = self._get_sentences(j.submit_documents(docs, source_id=source_id)).pop()
        assert 'Hier wird die Zensur zuschlagen.' not in sentences
        assert 'Der zweite Satz ist aber okay.' in sentences

        # check blacklist items
        assert blacklist == j.get_blacklist(source_id)

        # no blacklist
        sentences = self._get_sentences(j.submit_documents(docs)).pop()
        assert 'Hier wird die Zensur zuschlagen.' in sentences
        assert 'Der zweite Satz ist aber okay.' in sentences

        # clear blacklist
        j.clear_blacklist(source_id)
        sentences = self._get_sentences(j.submit_documents(docs, source_id=source_id)).pop()
        assert 'Hier wird die Zensur zuschlagen.' in sentences
        assert 'Der zweite Satz ist aber okay.' in sentences

        # check empty blacklist
        assert [] == j.get_blacklist(source_id)

    def test_custom_headers(self):
        ''' verifies that custom headers are preserved and no headers added '''
        docs = ({'id': 123,
                 'body': 'Hier wird die Zensur zuschlagen. Der zweite Satz ist aber okay.',
                 'title': 'Testdokument :)',
                 'format': 'text/html',
                 'header': {'dc:author': 'Ana', 'dc:source': 'http://test.org'}
                },
                {'id': 124,
                 'body': 'Das zweite Dokument.',
                 'title': 'Zweites Testdokument :)',
                 'format': 'text/html',
                 'header': {},
                },
               )

        j = Jeremia()
        first, second = j.submit_documents(docs)
        # swap documents, if required
        if first['content_id'] == '124':
            first, second = second, first

        assert 'dc:source="http://test.org"' in first['xml_content']
        assert 'dc:author="Ana"' in first['xml_content']

        assert '<wl:page xmlns:wl="http://www.weblyzard.com/wl/2013#" xmlns:dc="http://purl.org/dc/elements/1.1/" wl:id="124" dc:format="text/html" xml:lang="de" wl:nilsimsa="8030473ac029f400680409349e47100e00a29585c04a25ec808342b4c0a1aec8">' in second['xml_content']

    def test_has_queued_threads(self):
        has_queued_threads = Jeremia().has_queued_threads()
        assert has_queued_threads == True or has_queued_threads == False

    def test_has_queued_threads_exception(self):
        j = Jeremia(url='http://localhost:6666')
        has_queued_threads = j.has_queued_threads()
        assert has_queued_threads == True

    def test_docs_serialization_format(self):
        import json
        from eWRT.util.module_path import get_resource

        DOCS = [{'id': 7,
                 'body': 'Ehre sei Gott.',
                 'title': '',
                 'format': 'text/html',
                 'header': {'test': 'testvalue'}},
                {'id': 8,
                 'body': '',
                 'title': 'Guten Tag!',
                 'format': 'text/html',
                 'header': {}}]
        REFERENCE_MULTI = json.load(open(get_resource(__file__, 'data/jeremia_reference_output_documents.json')))
        REFERENCE_SINGLE = json.load(open(get_resource(__file__, 'data/jeremia_reference_output_single_document.json')))

        # document list
        j = Jeremia()
        result = j.submit_documents(DOCS)
        result.sort()
        REFERENCE_MULTI.sort()
        assert REFERENCE_MULTI == result

        # single document
        result = j.submit_document(DOCS[0])
        assert REFERENCE_SINGLE == result


def test_suite():
    '''
    add support for calling Jeremia tests as part of a test suite
    '''
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(JeremiaTest, 'test'))
    return suite


if __name__ == '__main__':
    if len(argv) > 1:
        txt = argv[1]
        docs = {'id': '192292',
                'body': txt,
                'title': '',
                'format': 'text/html',
                'header': {'test': 'testvalue'}}
        j = Jeremia()
        docs['body_annotation'] = [{'start':0, 'end': 3, 'key': 'test annotation'}]
        l = j.submit_document(docs)
        print l
    else:
        unittest.main()
