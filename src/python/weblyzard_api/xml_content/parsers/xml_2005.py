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
    ATTR_MAPPING = {'content_id': 'content_id',
                    'source_id': 'source_id',
                    'content_type': 'content_type',
                    'title': 'title',
                    'url': 'url',
                    'nilsimsa': 'nilsimsa',
                    'jonas_type': 'jonas_type',
                    'title_de': 'title_de',
                    'title_en': 'title_en',
                    'title_fr': 'title_fr',
                    }
    SENTENCE_MAPPING = {'pos_tags': 'pos',
                        'md5sum': 'md5sum',
                        'content_id': 'content_id',
                        'dependency': 'dependency',
                        'token': 'token',
                        'significance': 'significance',
                        'is_title': 'is_title',
                        'sem_orient': 'sem_orient'} 
    FEATURE_MAPPING = {}
    RELATION_MAPPING = {}
    
    VERSION = 2005

    @classmethod
    def pre_xml_dump(cls, titles, attributes, sentences):
        
        if not 'title' in attributes: 
            attributes['title'] = ' '.join([t.value for t in titles])
                
        return attributes, sentences