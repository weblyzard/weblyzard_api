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


class DatesToStrings(json.JSONEncoder):
    def _encode(self, obj):
        if isinstance(obj, dict):
            def transform_date(o):
                return self._encode(o.isoformat() if isinstance(o, datetime) else o)
            return {transform_date(k): transform_date(v) for k, v in obj.items()}
        else:
            return obj

    def encode(self, obj):
        return super(DatesToStrings, self).encode(self._encode(obj))


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
    def get_default_ns(cls):
        return cls.SUPPORTED_NAMESPACE

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
            except Exception as e:
                logger.error('could not encode {}: {}'.format(value, e))
                return

    @classmethod
    def decode_value(cls, value):
        try:
            decoded = json.loads(value)
            if decoded in (float('inf'), float('-inf'), float('nan')):
                raise ValueError('deserializing of invalid json values')
            else:
                return decoded
        except ValueError:
            # ignore silently (expected behaviour)
            return value

    @classmethod
    def cast_item(cls, item):
        ''' '''
        if item.lower() == 'true':
            return True
        elif item.lower() == 'false':
            return False

        try:
            return int(item)
        except Exception:
            pass

        try:
            return float(item)
        except Exception:
            pass

        try:
            return json.loads(item)
        except Exception:
            pass
        return item

    @classmethod
    def get_xml_value(cls, value):
        ''' '''
        try:
            if isinstance(value, int) or isinstance(value, float) or \
                    isinstance(value, datetime):
                value = str(value)
            elif isinstance(value, list) or isinstance(value, dict):
                value = json.dumps(value, cls=DatesToStrings)
        except Exception as e:
            logger.error('could not encode {}: {}'.format(value, e))
            value = str(value)
        return value

    @classmethod
    def is_supported(cls, xml_content):
        return 'xmlns:wl="{}"'.format(cls.SUPPORTED_NAMESPACE) in xml_content

    @classmethod
    def invert_mapping(cls, mapping):
        result = {}

        if mapping == None:
            return result
        invert_mapping = dict(zip(mapping.values(),
                                  mapping.keys()))
        for key, value in invert_mapping.iteritems():
            if isinstance(key, tuple):
                key, namespace = key
                if namespace is not None:
                    key = '{%s}%s' % (cls.DOCUMENT_NAMESPACES[namespace], key)
            result[key] = value
        return result

    @classmethod
    def parse(cls, xml_content, remove_duplicates=True):
        ''' '''
        parser = etree.XMLParser(recover=True, strip_cdata=False)
        root = etree.fromstring(xml_content.replace('encoding="UTF-8"', ''),
                                parser=parser)
        try:
            invert_mapping = cls.invert_mapping(cls.ATTR_MAPPING)
            attributes = cls.load_attributes(root.attrib,
                                             mapping=invert_mapping)
        except Exception as e:
            logger.warn('could not process mapping {}: {}'.format(
                cls.ATTR_MAPPING, e))
            attributes = {}

        sentences = cls.load_sentences(
            root, remove_duplicates=remove_duplicates)
        title_sentence_ids = [sentence['md5sum'] for sentence in sentences
                              if 'is_title' in sentence and sentence['is_title']]

        title_annotations = []
        body_annotations = []
        for annotation in cls.load_annotations(root):
            if 'md5sum' in annotation and annotation['md5sum'] in title_sentence_ids:
                title_annotations.append(annotation)
            else:
                body_annotations.append(annotation)

        features = cls.load_features(root)
        relations = cls.load_relations(root)
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

        annotation_mapping = cls.invert_mapping(cls.ANNOTATION_MAPPING)

        for annotation_element in root.iterfind('{%s}annotation' % cls.get_default_ns(),
                                                namespaces=cls.DOCUMENT_NAMESPACES):
            annotations.append(cls.load_attributes(annotation_element.attrib,
                                                   mapping=annotation_mapping))

        return annotations

    @classmethod
    def load_sentences(cls, root, remove_duplicates=True):
        ''' '''
        sentences = []
        seen_sentences = []

        sentence_mapping = cls.invert_mapping(cls.SENTENCE_MAPPING)

        for sent_element in root.iterfind('{%s}sentence' % cls.get_default_ns(),
                                          namespaces=cls.DOCUMENT_NAMESPACES):

            sent_attributes = cls.load_attributes(sent_element.attrib,
                                                  mapping=sentence_mapping)
            sent_attributes['value'] = sent_element.text.strip()

            if 'md5sum' in sent_attributes:
                sent_id = sent_attributes['md5sum']
            elif 'id' in sent_attributes:
                sent_id = sent_attributes['id']
                sent_attributes['md5sum'] = sent_id
                del sent_attributes['id']
            else:
                sent_id = hashlib.md5(
                    sent_element.text.encode('utf-8')).hexdigest()
                sent_attributes['md5sum'] = sent_id

            if not sent_id in seen_sentences:
                sentences.append(sent_attributes)

                if remove_duplicates:
                    seen_sentences.append(sent_id)

        return sentences

    @classmethod
    def load_features(cls, root):
        ''' '''
        features = {}

        # inverse feature mapping for loading
        feature_mapping = cls.invert_mapping(cls.FEATURE_MAPPING)
        for feat_element in root.iterfind('{%s}feature' % cls.get_default_ns(),
                                          namespaces=cls.DOCUMENT_NAMESPACES):
            feat_attributes = cls.load_attributes(feat_element.attrib,
                                                  mapping=feature_mapping)
            if 'key' in feat_attributes and feat_attributes['key'] in features:
                if not isinstance(features[feat_attributes['key']], list):
                    features[feat_attributes['key']] = [
                        features[feat_attributes['key']]]
                if feat_element.text is not None:
                    features[feat_attributes['key']].append(
                        cls.cast_item(feat_element.text.strip()))
            elif feat_element.text is not None:
                features[feat_attributes['key']] = cls.cast_item(
                    feat_element.text.strip())
        return features

    @classmethod
    def load_relations(cls, root):
        ''' '''
        relations = {}

        # inverse relation mapping for loading
        relation_mapping = cls.invert_mapping(cls.RELATION_MAPPING)
        for rel_element in root.iterfind('{%s}relation' % cls.get_default_ns(),
                                         namespaces=cls.DOCUMENT_NAMESPACES):
            rel_attributes = cls.load_attributes(rel_element.attrib,
                                                 mapping=relation_mapping)
            if 'key' in rel_attributes and rel_attributes['key'] in relations:
                if not isinstance(relations[rel_attributes['key']], list):
                    relations[rel_attributes['key']] = [
                        relations[rel_attributes['key']]]
                if rel_element.text is not None:
                    relations[rel_attributes['key']].append(
                        cls.cast_item(rel_element.text.strip()))
            elif rel_element.text is not None:
                relations[rel_attributes['key']] = cls.cast_item(
                    rel_element.text.strip())
        return relations

    @classmethod
    def dump_xml_attributes(cls, attributes, mapping):
        new_attributes = {}

        for key, value in attributes.iteritems():

            if mapping and key in mapping:
                key = mapping[key]
            elif ':' in key:
                continue

            if isinstance(key, tuple):
                key, namespace = key
                if namespace is not None:
                    key = '{%s}%s' % (
                        cls.DOCUMENT_NAMESPACES[namespace], key)
            if value and value not in ('None', 'null', '0.0'):
                new_attributes[key] = cls.encode_value(value)

        return new_attributes

    @classmethod
    def clean_attributes(cls, attributes):
        ''' '''
        result = {}
        for key, val in attributes.iteritems():
            if key is None or val is None or isinstance(val, dict):
                continue
            result[key] = val
        return result

    @classmethod
    def map_by_annotationtype(cls, itemlist):
        result = {}
        for item in itemlist:
            if not item['annotationType'] in result:
                result[item['annotationType']] = []
            result[item['annotationType']].append(item)
        return result

    @classmethod
    def get_required_namespaces(cls, attributes):
        ''' '''
        result = {}
        try:
            for att in attributes:
                ns_prefix = None
                if att in cls.ATTR_MAPPING:
                    _, ns_prefix = cls.ATTR_MAPPING[att]
                elif att in cls.SENTENCE_MAPPING:
                    _, ns_prefix = cls.SENTENCE_MAPPING[att]
                elif cls.ANNOTATION_MAPPING and att in cls.ANNOTATION_MAPPING:
                    _, ns_prefix = cls.ANNOTATION_MAPPING[att]
                elif cls.FEATURE_MAPPING and att in cls.FEATURE_MAPPING:
                    _, ns_prefix = cls.FEATURE_MAPPING[att]
                elif cls.RELATION_MAPPING and att in cls.RELATION_MAPPING:
                    _, ns_prefix = cls.RELATION_MAPPING[att]
                elif not att in cls.ATTR_MAPPING:
                    continue  # skip unknown attributes

                if ns_prefix is not None and ns_prefix in cls.DOCUMENT_NAMESPACES:
                    namespace = cls.DOCUMENT_NAMESPACES[cls.ATTR_MAPPING[att][1]]
                    result[ns_prefix] = namespace
        except Exception as e:
            pass
        if not 'wl' in result:
            result['wl'] = cls.DOCUMENT_NAMESPACES['wl']
        return result

    @classmethod
    def dump_xml(cls, titles, attributes, sentences, annotations=[],
                 features={}, relations={}):
        ''' returns a webLyzard XML document '''
        required_namespaces = cls.get_required_namespaces(attributes)
        attributes, sentences = cls.pre_xml_dump(titles=titles,
                                                 attributes=attributes,
                                                 sentences=sentences)

        if attributes:
            assert isinstance(attributes, dict), 'dict required'

        attributes = cls.dump_xml_attributes(attributes=attributes,
                                             mapping=cls.ATTR_MAPPING)
        try:
            attributes = cls.clean_attributes(attributes)
        except Exception as e:
            logger.warn(e)
        root = etree.Element('{%s}page' % cls.get_default_ns(),
                             attrib=attributes,
                             nsmap=required_namespaces)

        for sent in sentences:
            sent = sent.as_dict()
            assert isinstance(sent, dict), 'dict required'
            value = sent['value']
            del sent['value']

            if not value:
                continue

            value = cls.get_xml_value(value)
            sent_attributes = cls.dump_xml_attributes(sent,
                                                      mapping=cls.SENTENCE_MAPPING)
            sent_elem = etree.SubElement(root,
                                         '{%s}sentence' % cls.get_default_ns(),
                                         attrib=sent_attributes,
                                         nsmap={})
            try:
                sent_elem.text = etree.CDATA(value)
            except Exception as e:
                print('Skipping bad cdata: %s (%s)' % (value, e))
                continue

        if annotations:
            if isinstance(annotations, list):
                annotations = cls.map_by_annotationtype(annotations)

            # add all annotations as body annotations
            for a_type, a_items in annotations.iteritems():

                if a_items is None or len(a_items) == 0:
                    continue

                for annotation in a_items:
                    if not isinstance(annotation, dict):
                        continue
                    assert isinstance(annotation, dict), 'dict required'
                    if 'entities' in annotation:
                        for entity in annotation['entities']:
                            entity = entity.copy()
                            entity['annotation_type'] = a_type
                            entity['key'] = annotation['key']
                            preferred_name = annotation['preferredName']
                            if not isinstance(preferred_name, unicode):
                                preferred_name = preferred_name.decode('utf-8')
                            entity['preferredName'] = preferred_name

                            annotation_attributes = cls.dump_xml_attributes(
                                entity, mapping=cls.ANNOTATION_MAPPING)

                            try:
                                etree.SubElement(root,
                                                 '{%s}annotation' % cls.get_default_ns(),
                                                 attrib=annotation_attributes,
                                                 nsmap={})
                            except Exception as e:
                                continue

        # feature mappings if specified
        if cls.FEATURE_MAPPING and len(cls.FEATURE_MAPPING):
            for key, items in features.iteritems():
                feature_attributes = cls.dump_xml_attributes({'key': key},
                                                             mapping=cls.FEATURE_MAPPING)
                if not isinstance(items, list):
                    items = [items]

                for value in items:
                    try:
                        value = cls.get_xml_value(value)
                        feat_elem = etree.SubElement(root,
                                                     '{%s}feature' % cls.get_default_ns(
                                                     ),
                                                     attrib=feature_attributes,
                                                     nsmap={})
                        feat_elem.text = etree.CDATA(value)

                    except Exception as e:
                        print('Skipping bad cdata: %s (%s)' % (value, e))
                        continue

        # relation mappings, if specified
        if cls.RELATION_MAPPING and len(cls.RELATION_MAPPING):
            for key, items in relations.iteritems():
                rel_attributes = cls.dump_xml_attributes({'key': key},
                                                         mapping=cls.RELATION_MAPPING)
                if not isinstance(items, list):
                    items = [items]

                for value in items:
                    try:
                        value = cls.get_xml_value(value)
                        rel_elem = etree.SubElement(root,
                                                    '{%s}relation' % cls.get_default_ns(
                                                    ),
                                                    attrib=rel_attributes,
                                                    nsmap={})
                        rel_elem.text = etree.CDATA(value)

                    except Exception as e:
                        print('Skipping bad cdata: %s (%s)' % (value, e))
                        continue

        return etree.tostring(root, encoding='UTF-8', pretty_print=True)

    @classmethod
    def pre_xml_dump(cls, titles, attributes, sentences):
        ''' overriding this functions allows to perform custom cleanup tasks'''
        return attributes, sentences
