#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 07.04.2014

@author: heinz-peterlang
'''
from __future__ import print_function

import json
import logging
import hashlib
import unicodedata

from lxml import etree
from datetime import date, datetime


logger = logging.getLogger('weblyzard_api.xml_content.parsers')


class XMLParser(object):
    VERSION = None
    SUPPORTED_NAMESPACE = None
    DOCUMENT_NAMESPACES = None
    ATTR_MAPPING = None
    SENTENCE_MAPPING = None
    ANNOTATION_MAPPING = None
    FEATURE_MAPPING = None
    RELATION_MAPPING = None
    DEFAULT_NAMESPACE = 'wl'

    @classmethod
    def remove_control_characters(cls, value):
        return ''.join(ch for ch in value if unicodedata.category(ch)[0] != 'C')

    @classmethod
    def encode_value(cls, value):
        if isinstance(value, unicode):
            return XMLParser.remove_control_characters(value)
        elif isinstance(value, str):
            return XMLParser.remove_control_characters(value.decode('utf-8'))
        elif isinstance(value, date):
            return value.isoformat()
        elif isinstance(value, datetime):
            return value.isoformat()
        else:
            try:
                return json.dumps(value)
            except Exception, e:
                logger.error('could not encode %s: %s' % (value, e))
                return

    @classmethod
    def decode_value(cls, value):
        try:
            decoded = json.loads(value)
            if decoded in (float('inf'), float('-inf'), float('nan')):
                raise ValueError('deserializing of invalid json values')
            else:
                return decoded
        except ValueError as err:
            return value

    @classmethod
    def is_supported(cls, xml_content):
        return 'xmlns:wl="%s"' % cls.SUPPORTED_NAMESPACE in xml_content

        # if xml_content:
        # return any([ns in xml_content for ns in cls.get_supported_namespaces()])

    @classmethod
    def parse(cls, xml_content, remove_duplicates=True):
        ''' '''
        parser = etree.XMLParser(recover=True, strip_cdata=False)
        root = etree.fromstring(xml_content.replace('encoding="UTF-8"', ''),
                                parser=parser)
        try:
            attributes = cls.load_attributes(root.attrib,
                                             mapping=cls.ATTR_MAPPING)
        except Exception, e:
            attributes = {}

        sentences = cls.load_sentences(root, page_attributes=attributes,
                                       remove_duplicates=remove_duplicates)
        title_sentence_ids = [sentence['md5sum'] for sentence in sentences \
                              if 'is_title' in sentence and sentence['is_title']]
        
        title_annotations = []
        body_annotations = []
        for annotation in cls.load_annotations(root):
            if 'md5sum' in annotation and annotation['md5sum'] in title_sentence_ids:
                title_annotations.append(annotation)
            else:
                body_annotations.append(annotation)
        
        features = cls.load_features(root, page_attributes=attributes)
        relations = cls.load_relations(root, page_attributes=attributes)      
        return attributes, sentences, title_annotations, body_annotations, features, relations

    @classmethod
    def load_attributes(cls, attributes, mapping):
        new_attributes = {}

        for key, value in attributes.iteritems():
            if mapping and key in mapping:
                key = mapping.get(key, key)

            value = cls.decode_value(value)

            if not value == 'None':
                new_attributes[key] = value

        return new_attributes

    @classmethod
    def load_annotations(cls, root):
        ''' '''
        annotations = []
        for annotation_element in root.iterfind('{%s}annotation' % cls.get_default_ns(),
                                          namespaces=cls.DOCUMENT_NAMESPACES):
            annotations.append(cls.load_attributes(annotation_element.attrib,
                                                  mapping=cls.ANNOTATION_MAPPING))

        return annotations

    
    @classmethod
    def load_sentences(cls, root, page_attributes=None, remove_duplicates=True):
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
            elif 'id' in sent_attributes:
                sent_id = sent_attributes['id']
                sent_attributes['md5sum'] = sent_id
                del sent_attributes['id']
            else:
                sent_id = hashlib.md5(sent_element.text.encode('utf-8')).hexdigest()
                sent_attributes['md5sum'] = sent_id

            if not sent_id in seen_sentences:
                sentences.append(sent_attributes)

                if remove_duplicates:
                    seen_sentences.append(sent_id)

        return sentences

    @classmethod
    def cast_item(cls, item):
        if item.lower()=='true':
            return True
        elif item.lower()=='false':
            return False
        
        try:
            return int(item)
        except Exception:
            pass
        
        try:
            return float(item)
        except Exception:
            pass
        
        return item
        
    @classmethod
    def load_features(cls, root, page_attributes):
        ''' '''
        features = {}
        for feat_element in root.iterfind('{%s}feature' % cls.get_default_ns(),
                                          namespaces=cls.DOCUMENT_NAMESPACES):
            feat_attributes = cls.load_attributes(feat_element.attrib,
                                                  mapping=cls.FEATURE_MAPPING)
            if 'key' in feat_attributes and feat_attributes['key'] in features:
                if not isinstance(features[feat_attributes['key']], list):
                    features[feat_attributes['key']] = [features[feat_attributes['key']]]
                if feat_element.text is not None:
                    features[feat_attributes['key']].append(cls.cast_item(feat_element.text.strip()))
            elif feat_element.text is not None:
                features[feat_attributes['key']] = cls.cast_item(feat_element.text.strip())
        return features
    
    @classmethod
    def load_relations(cls, root, page_attributes):
        ''' '''
        relations = {}
        for rel_element in root.iterfind('{%s}relation' % cls.get_default_ns(),
                                          namespaces=cls.DOCUMENT_NAMESPACES):
            rel_attributes = cls.load_attributes(rel_element.attrib,
                                                  mapping=cls.RELATION_MAPPING)
            if 'key' in rel_attributes and rel_attributes['key'] in relations:
                if not isinstance(relations[rel_attributes['key']], list):
                    relations[rel_attributes['key']] = [relations[rel_attributes['key']]]
                if rel_element.text is not None:
                    relations[rel_attributes['key']].append(cls.cast_item(rel_element.text.strip()))
            elif rel_element.text is not None:
                relations[rel_attributes['key']] = cls.cast_item(rel_element.text.strip())
        return relations

    @classmethod
    def dump_xml_attributes(cls, attributes, mapping):
        new_attributes = {}

        for key, value in attributes.iteritems():

            if mapping and key in mapping:
                key = mapping[key]
            elif ':' in key:
                continue

            if value and value not in ('None', 'null', '0.0'):
                new_attributes[key] = cls.encode_value(value)

        return new_attributes

    @classmethod
    def clean_attributes(cls, attributes):
        ''' '''
        result = {}
        for key, val in attributes.iteritems():
            if val is None or isinstance(val, dict):
                continue
            result[key] = val
        return result
    
    @classmethod
    def dump_xml(cls, titles, attributes, sentences, annotations=[], 
                 features={}, relations={}):
        ''' returns a webLyzard XML document '''

        attributes, sentences = cls.pre_xml_dump(titles=titles,
                                                 attributes=attributes,
                                                 sentences=sentences)

        if attributes:
            assert isinstance(attributes, dict), 'dict required'

        if cls.ATTR_MAPPING:
            invert_mapping = dict(zip(cls.ATTR_MAPPING.values(),
                cls.ATTR_MAPPING.keys()))
        else:
            invert_mapping = None

        attributes = cls.dump_xml_attributes(attributes=attributes,
                                             mapping=invert_mapping)
        attributes = cls.clean_attributes(attributes)
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
                
            try:
                sent_elem.text = etree.CDATA(value)
            except Exception, e:
                print('Skipping bad cdata: %s (%s)' % (value, e))
                continue
            
        if cls.ANNOTATION_MAPPING:
            annotation_mapping = dict(zip(cls.ANNOTATION_MAPPING.values(),
                                    cls.ANNOTATION_MAPPING.keys()))
        else:
            annotation_mapping = None

        if annotations:
            # add all annotations as body annotations
            for a_type, a_items in annotations.iteritems():
                for annotation in a_items:    
                    if not isinstance(annotation, dict):
                        continue   
                    assert isinstance(annotation, dict), 'dict required'
                    if 'entities' in annotation:
                        for entity in annotation['entities']:
                            entity['annotation_type'] = a_type
                            entity['key'] = annotation['key']
                            preferred_name = annotation['preferredName']
                            if not isinstance(preferred_name, unicode):
                                preferred_name = preferred_name.decode('utf-8')
                            entity['preferredName'] = preferred_name
    
                            annotation_attributes = cls.dump_xml_attributes(entity,
                                                                            mapping=annotation_mapping)
                            
                            try:
                                etree.SubElement(root,
                                                 '{%s}annotation' % cls.get_default_ns(),
                                                 attrib=annotation_attributes,
                                                 nsmap=cls.DOCUMENT_NAMESPACES)
                            except Exception, e:
                                continue
               
        # featrure mappings if specified             
        if cls.FEATURE_MAPPING and len(cls.FEATURE_MAPPING):
            feature_mapping = dict(zip(cls.FEATURE_MAPPING.values(),
                                       cls.FEATURE_MAPPING.keys()))

            for key, items in features.iteritems():
                feature_attributes = cls.dump_xml_attributes({'key': key},
                                                             mapping=feature_mapping)
                if not isinstance(items, list):
                    items = [items]
                
                for value in items:
                    try:
                        feat_elem = etree.SubElement(root,
                                                     '{%s}feature' % cls.get_default_ns(),
                                                     attrib=feature_attributes,
                                                     nsmap=cls.DOCUMENT_NAMESPACES)
                        if isinstance(value, int) or isinstance(value, list):
                            value = str(value)
                        
                        feat_elem.text = etree.CDATA(value)
                    except Exception, e:
                        print('Skipping bad cdata: %s (%s)' % (value, e))
                        continue

        # relation mappings, if specified            
        if cls.RELATION_MAPPING and len(cls.RELATION_MAPPING):
            relation_mapping = dict(zip(cls.RELATION_MAPPING.values(),
                                       cls.RELATION_MAPPING.keys()))

            for key, items in relations.iteritems():
                rel_attributes = cls.dump_xml_attributes({'key': key},
                                                         mapping=relation_mapping)
                if not isinstance(items, list):
                    items = [items]
                
                for value in items:
                    try:
                        rel_elem = etree.SubElement(root,
                                                    '{%s}relation' % cls.get_default_ns(),
                                                    attrib=rel_attributes,
                                                    nsmap=cls.DOCUMENT_NAMESPACES)
                        if isinstance(value, int) or isinstance(value, list):
                            value = str(value)
                        
                        rel_elem.text = etree.CDATA(value)
                    except Exception, e:
                        print('Skipping bad cdata: %s (%s)' % (value, e))
                        continue
        
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
