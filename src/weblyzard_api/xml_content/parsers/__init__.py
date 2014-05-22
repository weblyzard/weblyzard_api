#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 07.04.2014

@author: heinz-peterlang
'''
from pprint import pprint
import hashlib
import json
import logging
import re
from lxml import etree

logger = logging.getLogger('weblyzard_api.xml_content.parsers')

class XMLParser(object):
    
    VERSION = None
    SUPPORTED_NAMESPACE = None
    DOCUMENT_NAMESPACES = None
    ATTR_MAPPING = None
    SENTENCE_MAPPING = None
    DEFAULT_NAMESPACE = 'wl'
    
    @classmethod
    def encode_value(cls, value):
        if isinstance(value, basestring):
            return value
        else: 
            try:
                return json.dumps(value)
            except Exception, e:
                logger.error('could not encode %s: %s' % (value, e)) 
                return 
            
    @classmethod
    def decode_value(cls, value):
        try:
            return json.loads(value)
        except ValueError: 
            return value
    
    @classmethod
    def is_supported(cls, xml_content):
        return 'xmlns:wl="%s"' % cls.SUPPORTED_NAMESPACE in xml_content
#         if xml_content:
#             return any([ns in xml_content for ns in cls.get_supported_namespaces()])
    
    @classmethod
    def parse(cls, xml_content):
        ''' ''' 
        parser = etree.XMLParser(recover=True, strip_cdata=False)
        root = etree.fromstring(xml_content.replace('encoding="UTF-8"', ''), 
                                parser=parser)
        attributes = cls.load_attributes(root.attrib,
                                          mapping=cls.ATTR_MAPPING)
        
        sentences = cls.load_sentences(root, page_attributes=attributes)
        
        return attributes, sentences
    
    @classmethod
    def load_attributes(cls, attributes, mapping):
        new_attributes = {}
        
        for key, value in attributes.iteritems():
            if mapping:                
                key = mapping.get(key, key)
                
            value = cls.decode_value(value)
            
            if not value == 'None': 
                new_attributes[key] = value

        return new_attributes
    
    @classmethod
    def load_sentences(cls, root, page_attributes=None):
        ''' '''
        sentences = []
        seen_sentences = []

        for sent_element in root.iterfind('{%s}sentence' % cls.get_default_ns(),
                                          namespaces=cls.DOCUMENT_NAMESPACES):
            
            sent_attributes = cls.load_attributes(sent_element.attrib, 
                                                  mapping=cls.SENTENCE_MAPPING)
            sent_attributes['value'] = sent_element.text.strip()
            
            if 'md5sum' in sent_attributes: 
                sent_id = sent_attributes['md5sum']
            else: 
                sent_id = sent_attributes['id']
                sent_attributes['md5sum'] = sent_id
                del sent_attributes['id']
                
            if not sent_id in seen_sentences:
                sentences.append(sent_attributes)
                seen_sentences.append(sent_id)
        
        return sentences
    
    @classmethod
    def dump_xml_attributes(cls, attributes, mapping, keep_none_values=False):
        new_attributes = {}
        
        for key, value in attributes.iteritems():
            
            if mapping and key in mapping: 
                key = mapping[key]
                
            if value and value not in ('None', 'null', '0.0'):
                new_attributes[key] = cls.encode_value(value) 
            
        return new_attributes
        
    @classmethod
    def dump_xml(cls, titles, attributes, sentences):
        ''' returns attribute / sentence as a webLyzard XML document '''
        
        attributes, sentences = cls.pre_xml_dump(titles=titles,
                                                 attributes=attributes, 
                                                 sentences=sentences)
        
        if attributes: 
            assert isinstance(attributes, dict), 'dict required'
        
        if cls.ATTR_MAPPING:
            invert_mapping = dict (zip(cls.ATTR_MAPPING.values(),
                                       cls.ATTR_MAPPING.keys()))
        else: 
            invert_mapping = None
            
        attributes = cls.dump_xml_attributes(attributes, 
                                             mapping=invert_mapping)
        root = etree.Element('{%s}page' % cls.get_default_ns(), 
                             attrib=attributes, 
                             nsmap=cls.DOCUMENT_NAMESPACES)
        
        if cls.SENTENCE_MAPPING:
            sent_mapping = dict(zip(cls.SENTENCE_MAPPING.values(),
                                    cls.SENTENCE_MAPPING.keys()))
        else: 
            sent_mapping = None
            
        for sent in sentences: 
            sent = sent.as_dict()
            assert isinstance(sent, dict), 'dict required'
            value = sent['value']
            del sent['value']
            
            
            if not value:
                continue
            
            sent_attributes = cls.dump_xml_attributes(sent, 
                                                      mapping=sent_mapping)
            sent_elem = etree.SubElement(root, 
                                         '{%s}sentence' % cls.get_default_ns(), 
                                         attrib=sent_attributes, 
                                         nsmap=cls.DOCUMENT_NAMESPACES)
            if isinstance(value, int):
                value = str(value)
            sent_elem.text = etree.CDATA(value)
        
        return etree.tostring(root, encoding='UTF-8', pretty_print=True)
    
    @classmethod
    def pre_xml_dump(cls, titles, attributes, sentences):
        ''' overriding this functions allows to perform custom cleanup tasks'''
        return attributes, sentences
    
    @classmethod
    def get_supported_namespaces(cls):
        if not isinstance(cls.SUPPORTED_NAMESPACES, list):
            return [cls.SUPPORTED_NAMESPACES]
        return cls.SUPPORTED_NAMESPACES
    
    @classmethod
    def get_default_ns(cls):
        return cls.SUPPORTED_NAMESPACE
    
    