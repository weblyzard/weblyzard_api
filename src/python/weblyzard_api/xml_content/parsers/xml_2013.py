#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 07.04.2014

@author: heinz-peterlang
'''
import unittest
from weblyzard_api.xml_content.parsers import XMLParser

class XML2013(XMLParser):
    
    SUPPORTED_NAMESPACE = 'http://www.weblyzard.com/wl/2013#'
    DOCUMENT_NAMESPACES = {'wl': SUPPORTED_NAMESPACE,
                           'dc': 'http://purl.org/dc/elements/1.1/',
                           'xml': 'http://www.w3.org/XML/1998/namespace'}
    VERSION = 2013
    ATTR_MAPPING = {'{%s}nilsimsa' % DOCUMENT_NAMESPACES['wl']: 'nilsimsa',
                    '{%s}format' % DOCUMENT_NAMESPACES['dc']: 'content_type',
                    '{%s}lang' % DOCUMENT_NAMESPACES['xml']: 'lang',
                    '{%s}id' % DOCUMENT_NAMESPACES['wl']: 'content_id',
                    '{%s}source' % DOCUMENT_NAMESPACES['dc']: 'source',}
    SENTENCE_MAPPING = {'{%s}token' % DOCUMENT_NAMESPACES['wl']: 'token',
                        '{%s}sem_orient' % DOCUMENT_NAMESPACES['wl']: 'sem_orient',
                        '{%s}significance' % DOCUMENT_NAMESPACES['wl']: 'significance',
                        '{%s}id' % DOCUMENT_NAMESPACES['wl']: 'md5sum',
                        '{%s}pos' % DOCUMENT_NAMESPACES['wl']: 'pos',
                        '{%s}is_title' % DOCUMENT_NAMESPACES['wl']: 'is_title',
                        '{%s}dependency' % DOCUMENT_NAMESPACES['wl']: 'dependency'}
    ANNOTATION_MAPPING = {'{%s}key' % DOCUMENT_NAMESPACES['wl']: 'key',
                          '{%s}surfaceForm' % DOCUMENT_NAMESPACES['wl']: 'surfaceForm',
                          '{%s}start' % DOCUMENT_NAMESPACES['wl']: 'start',
                          '{%s}end' % DOCUMENT_NAMESPACES['wl']: 'end',
                          '{%s}annotationType' % DOCUMENT_NAMESPACES['wl']: 'annotation_type',
                          '{%s}preferredName' % DOCUMENT_NAMESPACES['wl']: 'preferredName'
                          }

    @classmethod
    def pre_xml_dump(cls, titles, attributes, sentences):
        return attributes, titles + sentences

class TestXML2013(unittest.TestCase):
    
    def test(self):
        xml = '''<wl:page xmlns:wl="http://www.weblyzard.com/wl/2013#" 
             xmlns:dc="http://purl.org/dc/elements/1.1/" 
             wl:id="578351358" 
             dc:format="text/html" 
             xml:lang="de" 
             wl:nilsimsa="37345e380610614cc7696ac08ed098e05fa64211755da1d4f525ef4cd762726e">
        <wl:sentence 
            wl:pos="NN $( NN APPR ADJA NN VVPP" 
            wl:id="b42bb3f2cb7ed667ba311811823f37cf" 
            wl:token="0,20 21,22 23,38 39,42 43,49 50,56 57,64" 
            wl:sem_orient="0.0" 
            wl:significance="0.0"
            wl:is_title="true">
                <![CDATA[Freihandelsgespr??che - Erleichterungen f??r kleine Firmen geplant]]>
        </wl:sentence>
        <wl:annotation
            wl:key="some.url.com"
            wl:surfaceForm="this is the text"
            wl:start="0"
            wl:end="10"
            wl:md5sum="b42bb3f2cb7ed667ba311811823f37cf">
        </wl:annotation></wl:page>'''
        
        attributes, sentences, title_annotations, body_annotations = XML2013.parse(xml)

        assert len(attributes) == 4
        assert len(sentences) == 1
        assert all(attr in attributes for attr in ('content_id', 'content_type',
                                                   'lang', 'nilsimsa'))
        for sent in sentences: 
            assert 'id' not in sent
            assert 'md5sum' in sent

if __name__ == '__main__':
    unittest.main()
    


