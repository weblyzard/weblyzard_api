#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jun 24, 2012

@author: heinz-peterlang
'''
import unittest
from weblyzard_api.xml_content.parsers.xml_2005 import XML2005

class XMLDeprecated(XML2005):
    
    SUPPORTED_NAMESPACE = 'http://www.weblyzard.com/'
    VERSION = 'deprecated'
    
class TestXMLDeprecated(unittest.TestCase):
    
    def test(self):
        xml = ''' 
            <wl:page xmlns:wl="http://www.weblyzard.com/" content_id="228557824" content_type="text/html" lang="DE" title="Der ganze Wortlaut: Offener Brief an Niko Pelinka  | Heute.at   ">
                <wl:sentence id="7e985ffb692bb6f617f25619ecca39a9"><![CDATA[Der ganze Wortlaut]]></wl:sentence>
                <wl:sentence id="7e985ffb692bb6f617f25619ecca39a9"><![CDATA[Der ganze Wortlaut]]></wl:sentence>
            </wl:page> '''
        
        attributes, sentences = XMLDeprecated.parse(xml)
        assert len(attributes) == 4
        assert len(sentences) == 1
        for sent in sentences: 
            assert 'id' not in sent
            assert 'md5sum' in sent
            
if __name__ == '__main__':
    unittest.main()