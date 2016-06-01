#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 07.04.2014

@author: heinz-peterlang
'''
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