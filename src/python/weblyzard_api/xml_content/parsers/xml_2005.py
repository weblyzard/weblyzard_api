#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 07.04.2014

@author: heinz-peterlang
'''
import unittest
from weblyzard_api.xml_content.parsers import XMLParser

class XML2005(XMLParser):
    
    SUPPORTED_NAMESPACE = 'http://www.weblyzard.com/wl/2005'
    DOCUMENT_NAMESPACES = {'wl': SUPPORTED_NAMESPACE}
    SENTENCE_MAPPING = {'pos_tags': 'pos'} 
    VERSION = 2005

    @classmethod
    def pre_xml_dump(cls, titles, attributes, sentences):
        
        if not 'title' in attributes: 
            attributes['title'] = ' '.join([t.value for t in titles])
                
        return attributes, sentences

class TestXML2005(unittest.TestCase):
    
    def test(self):
        xml = ''' <wl:page xmlns:wl="http://www.weblyzard.com/wl/2005" 
             lang="de" 
             title="Freihandelsgespr??che - Erleichterungen f??r kleine Firmen geplant" 
             content_type="text/html" 
             content_id="578351358" 
             nilsimsa="73345e38061061454f686ac08fd498e05fa6421175d5a1d5f525ef48d77a322e">
        <wl:sentence 
            pos_tags="None" 
            sem_orient="0.721687836487" 
            significance="839.529561215" 
            md5sum="b6ec48367959b201fb07f421d0743e50" 
            pos="NE $( NE ( NE ) $( ADJA KON ADJA NN VMFIN APPR NN APPRART NN APPR ART NE VVFIN $." 
            token="0,7 7,8 8,18 19,20 20,27 27,28 29,30 31,37 38,41 42,50 51,62 63,69 70,73 74,89 90,94 95,101 102,105 106,109 110,113 114,120 120,121">
                <![CDATA[Br??ssel/Washington (APA/dpa) - Kleine und mittlere Unternehmen k??nnen auf Erleichterungen beim Handel mit den USA hoffen.]]>    
        </wl:sentence></wl:page>'''
        
        attributes, sentences = XML2005.parse(xml)
        assert len(attributes) == 5
        assert len(sentences) == 1
        assert all(attr in attributes for attr in ('content_id', 'content_type',
                                                   'lang', 'nilsimsa'))
        for sent in sentences: 
            assert 'id' not in sent
            assert 'md5sum' in sent
    
if __name__ == '__main__':
    unittest.main()