#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
.. codeauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
import unittest

from sys import argv

from weblyzard_api.client.jeremia import Jeremia
from weblyzard_api.model.xml_content import XMLContent


class JeremiaTest(unittest.TestCase):

    DOCS = [{'id': content_id,
             'body': 'Good day Mr. President! Hello "world" {}'.format(content_id),
             'title': 'Hello "world" more ',
             'format': 'text/html',
             'header': {}} for content_id in range(1000, 1020)]

    def test_single_document_processing(self):
        j = Jeremia()
        print('submitting document...')
        document_annotated = j.submit_document(self.DOCS[1])
        self.assertTrue(document_annotated != "")

    def test_single_document_with_annotations(self):
        '''
        Tests the handling of single document annotations.
        '''
        DOC = {'id': 12,
               'body': 'UBS has finally succeeded. They obtained a 10% share of CS.',
               'title': 'UBS versus Credit Suisse.',
               'format': 'text/html',
               'title_annotation': [{'start': 0, 'end': 3, 'surfaceForm': 'UBS', 'key': 'http://dbpedia.org/UBS'},
                                    {'start': 11, 'end': 24, 'surfaceForm': 'Credit Suisse', 'key': 'http://dbpedia.org/Credit Suisse'}],
               'body_annotation': [{'start': 0, 'end': 3, 'surfaceForm': 'UBS', 'key': 'http://dbpedia.org/UBS'},
                                   {'start': 56, 'end': 58, 'surfaceForm': 'CS', 'key': 'http://dbpedia.org/Credit Suisse'}],
               'header': {},
               }

        j = Jeremia()

        # this test requires Jeremia version 0.0.4+
        if j.version() < b"0.0.4":
            return

        print('submitting document with annotations...')
        result = j.submit_document(document=DOC, wait_time=30)

        # check: all annotations have been preserved
        print(result)
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
        docs = j.submit_documents(documents=self.DOCS, wait_time=30)
        self.assertEqual(len(docs), 20)

    def test_sentence_splitting(self):
        j = Jeremia()

        for doc in j.submit_documents(documents=self.DOCS[:1], wait_time=30):
            # extract sentences
            print(doc)
            xml_obj = XMLContent(doc['xml_content'])
            sentences = [s.sentence for s in xml_obj.sentences]
            print(doc['xml_content'])
            assert 'wl:is_title' in doc['xml_content']
            print(sentences)

            # TODO: check sentence splitting in jeremia!
            # self.assertEqual(len(sentences), 3)

    def test_illegal_xml_format_filtering(self):
        DOCS = [{'id': 'alpha',
                 'body': 'This is an illegal XML Sequence: J\x1amica',
                 'title': 'Hello "world" more ',
                 'format': 'text/html',
                 'header': {}}]

        j = Jeremia()
        for doc in j.submit_documents(documents=DOCS, wait_time=30):
            xml = XMLContent(doc['xml_content'])
            print(doc['xml_content'])
            assert xml.sentences[0].sentence != None

    def test_illegal_input_args(self):
        j = Jeremia()

        with self.assertRaises(ValueError):
            j.submit_documents(documents=[], wait_time=30)

    def test_missing_space_tokenattribute(self):

        def text_as_doc(text):
            docs = [{'id': 'alpha',
                     'body': text,
                     'title': '',
                     'format': 'text/html',
                     'header': {}}]
            return docs

        j = Jeremia()

        test_texts = {
            'Min. 25 000 Kč - řidiči nákladních automobilů, tahačů a… Úřad práce Písek http://t.co/QowX6PQjrR': 17,
            'Retos de la #RSE (II): 1. Más autocrítica en las memorias de sostenibilidad': 17,
        }

        for text, token_number in list(test_texts.items()):
            result = j.submit_documents(documents=text_as_doc(text), wait_time=30)
            res_xml = list(result)[0]['xml_content']
            assert len(
                list(XMLContent(res_xml).sentences[0].tokens)) == token_number

    def _get_sentences(self, jeremia_result):
        ''' extracts the list of sentences (as text) from an
            jeremia result.
        '''
        result = []
        for json_document in jeremia_result:
            result.append([s.sentence for s in XMLContent(
                json_document['xml_content']).sentences])

        return result

    def test_blacklist(self):
        ''' tests the blacklist-based sentence filtering '''
        source_id = 1
        blacklist = ['6e44889df94d6408bbeeab8837bfbe01',
                     '422d7f2000393b8c50a37f9d363ad511']
        docs = [{'id': 123,
                 'body': 'Hier wird die Zensur zuschlagen. Der zweite Satz ist aber okay.',
                 'title': 'Testdokument :)',
                 'format': 'text/html',
                 'header': {}}]

        # use the blacklist
        j = Jeremia()
        j.update_blacklist(source_id=source_id, blacklist=blacklist)
        sentences = self._get_sentences(
            j.submit_documents(documents=docs, source_id=source_id, wait_time=30)).pop()
        assert 'Hier wird die Zensur zuschlagen.' not in sentences
        assert 'Der zweite Satz ist aber okay.' in sentences

        # check blacklist items
        assert blacklist == j.get_blacklist(source_id)

        # no blacklist
        sentences = self._get_sentences(j.submit_documents(documents=docs, wait_time=30)).pop()
        assert 'Hier wird die Zensur zuschlagen.' in sentences
        assert 'Der zweite Satz ist aber okay.' in sentences

        # clear blacklist
        j.clear_blacklist(source_id)
        sentences = self._get_sentences(
            j.submit_documents(documents=docs, source_id=source_id, wait_time=30)).pop()
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
        first, second = j.submit_documents(documents=docs, wait_time=30)
        # swap documents, if required
        if first['content_id'] == '124':
            first, second = second, first

        assert 'dc:source="http://test.org"' in first['xml_content']
        assert 'dc:author="Ana"' in first['xml_content']

        assert '<wl:page xmlns:wl="http://www.weblyzard.com/wl/2013#" xmlns:dc="http://purl.org/dc/elements/1.1/" wl:id="124" dc:format="text/html" xml:lang="de" wl:nilsimsa="8030473ac029f400680409349e47100e00a29585c04a25ec808342b4c0a1aec8">'.lower() in second[
            'xml_content'].lower()

    def test_has_queued_threads(self):
        has_queued_threads = Jeremia().has_queued_threads()
        assert has_queued_threads == True or has_queued_threads == False

    def test_has_queued_threads_exception(self):
        j = Jeremia(url='http://localhost:8080')
        has_queued_threads = j.has_queued_threads()
        assert has_queued_threads == True

    def test_docs_serialization_format(self):
        import json
        from weblyzard_api.util.module_path import get_resource

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
        REFERENCE_MULTI = json.load(
            open(get_resource(__file__, 'data/jeremia_reference_output_documents.json')))
        REFERENCE_SINGLE = json.load(open(get_resource(
            __file__, 'data/jeremia_reference_output_single_document.json')))

        # document list
        j = Jeremia()
        result = j.submit_documents(documents=DOCS, wait_time=30)
        result.sort()
        REFERENCE_MULTI.sort()
        assert REFERENCE_MULTI == result

        # single document
        result = j.submit_document(document=DOCS[0], wait_time=30)
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
        docs['body_annotation'] = [
            {'start': 0, 'end': 3, 'key': 'test annotation'}]
        l = j.submit_document(docs)
        print(l)
    else:
        unittest.main()
