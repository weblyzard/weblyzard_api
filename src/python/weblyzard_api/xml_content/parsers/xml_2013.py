#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 07.04.2014

@author: heinz-peterlang
'''
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