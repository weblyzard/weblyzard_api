#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Feb, 27 2013

.. codeauthor: Heinz-Peter Lang <lang@weblyzard.com>
.. codeauthor: Albert Weichselbraun <Weichselbraun@weblyzard.com>
.. codeauthor: Fabian Fischer <fabian.fischer@modul.ac.at>

Handles the new (http://www.weblyzard.com/wl/2013#) weblyzard
XML format.

Functions added:
 - support for sentence tokens and pos iterators

Remove functions:
 - compatibility fixes for namespaces, encodings etc.
 - support for the old POS tags mapping.
'''

from collections import namedtuple
import json
import logging
from lxml import etree
from pprint import pprint

import unittest
import hashlib

from weblyzard_api.xml_content.parsers.xml_2005 import XML2005
from weblyzard_api.xml_content.parsers.xml_2013 import XML2013
from weblyzard_api.xml_content.parsers.xml_deprecated import XMLDeprecated

SENTENCE_ATTRIBUTES = ('pos_tags', 'sem_orient', 'significance', 'md5sum',
                       'pos', 'token', 'dependency')

LabeledDependency = namedtuple("LabeledDependency", "parent pos label")

class Annotation(object):
    
    def __init__(self, annotation_type=None, start=None, end=None, key=None, 
                 sentence=None, surfaceForm=None, md5sum=None, sem_orient=None):
        self.annotation_type = annotation_type
        self.surfaceForm = surfaceForm
        self.start = start
        self.end = end
        self.key = key
        self.sentence = sentence
        self.md5sum = md5sum
        self.sem_orient = sem_orient
    
    def as_dict(self):
        '''
        :returns: a dictionary representation of the sentence object.
        '''
        return dict((k, v) for k, v in self.__dict__.iteritems() if not k.startswith('_'))
    
class Sentence(object):
    '''
    The sentence class used for accessing single sentences.

    .. note::

        the class provides convenient properties for accessing pos tags and tokens:
    
        * s.sentence: sentence text
        * s.tokens  : provides a list of tokens (e.g. ['A', 'new', 'day'])
        * s.pos_tags: provides a list of pos tags (e.g. ['DET', 'CC', 'NN'])
    '''
    #:  Maps the keys of the attributes to the corresponding key for the API JSON
    API_MAPPINGS = {
        1.0: {
            'md5sum': 'id',
            'value': 'value',
            'pos': 'pos_list',
            'sem_orient': 'polarity',
            'token': 'tok_list',
            'is_title': 'is_title',
            'dependency': 'dep_tree',
            }
        }
    
    def __init__(self, md5sum=None, pos=None, sem_orient=None, significance=None, 
                 token=None, value=None, is_title=False, dependency=None):
        
        if not md5sum and value: 
            try:
                m = hashlib.md5()
                m.update(value.encode('utf-8') if isinstance(value, unicode) else str(value))
                md5sum = m.hexdigest()
            except Exception, e: 
                print e
                
        self.md5sum = md5sum
        self.pos = pos
        self.sem_orient = sem_orient
        self.significance = significance
        self.token = token
        self.value = value
        self.is_title = is_title
        self.dependency = dependency

    def as_dict(self):
        '''
        :returns: a dictionary representation of the sentence object.
        '''
        return dict((k, v) for k, v in self.__dict__.iteritems() if not k.startswith('_'))
        
    def get_sentence(self):
        return self.value

    def set_sentence(self, new_sentence):
        self.value = new_sentence

    def get_pos_tags(self):
        '''
        Get the POS Tags as list.

        >>> sentence = Sentence(pos = 'PRP ADV NN')
        >>> sentence.get_pos_tags()
        ['PRP', 'ADV', 'NN']
        '''
        if self.pos:
            return self.pos.strip().split()
        else:
            return None

    def set_pos_tags(self, new_pos_tags):
        if isinstance(new_pos_tags, list):
            new_pos_tags = ' '.join(new_pos_tags)
        self.pos = new_pos_tags
    
    def get_pos_tags_list(self):
        '''
        :returns: list of the sentence's POS tags

        >>> sentence = Sentence(pos = 'PRP ADV NN')
        >>> sentence.get_pos_tags_list()
        ['PRP', 'ADV', 'NN']
        '''
        return [] if not self.pos_tag_string else self.get_pos_tags()
    
    def set_pos_tags_list(self, pos_tags_list):
        self.set_pos_tags(pos_tags_list)
    
    def get_pos_tags_string(self):
        '''
        :returns: String of the sentence's POS tags

        >>> sentence = Sentence(pos = 'PRP ADV NN')
        >>> sentence.get_pos_tags_string()
        'PRP ADV NN'
        '''
        return self.pos
    
    def set_pos_tags_string(self, new_value):
        self.pos = new_value
    
    def get_tokens(self):
        '''
        :returns: an iterator providing the sentence's tokens 
        '''
        if not self.token:
            raise StopIteration

        for token_pos in self.token.split(' '):
            start, end = map(int, token_pos.split(','))
            #yield self.sentence.decode('utf8')[start:end]
            yield unicode(self.sentence)[start:end]

    def get_dependency_list(self):
        '''
        :returns: the dependencies of the sentence as a list of \
            `LabeledDependency` objects
        :rtype: :py:class:`list` of :py:class:\
            `weblyzard_api.xml_content.LabeledDependency` objects

        >>> s = Sentence(pos='RB PRP MD', dependency='1:SUB -1:ROOT 1:OBJ')
        >>> s.dependency_list
        [LabeledDependency(parent='1', pos='RB', label='SUB'), LabeledDependency(parent='-1', pos='PRP', label='ROOT'), LabeledDependency(parent='1', pos='MD', label='OBJ')]
        '''
        if self.dependency:
            result = []
            deps = self.dependency.strip().split(' ')
            for index, dep in enumerate(deps):
                [parent, label] = dep.split(':') if ':' in dep else [dep, None]
                result.append(LabeledDependency(parent, 
                                                self.pos_tags_list[index],
                                                label))
            return result
        else:
            return None

    def set_dependency_list(self, dependencies):
        '''
        Takes a list of :py:class:`weblyzard_api.xml_content.LabeledDependency`

        :param dependencies: The dependencies to set for this sentence.
        :type dependencies: list

        .. note:: The list must contain items of the type \
            :py:class:`weblyzard_api.xml_content.LabeledDependency`

        >>> s = Sentence(pos='RB PRP MD', dependency='1:SUB -1:ROOT 1:OBJ')
        >>> s.dependency_list
        [LabeledDependency(parent='1', pos='RB', label='SUB'), LabeledDependency(parent='-1', pos='PRP', label='ROOT'), LabeledDependency(parent='1', pos='MD', label='OBJ')]
        >>> s.dependency_list = [LabeledDependency(parent='-1', pos='MD', label='ROOT'), ]
        >>> s.dependency_list
        [LabeledDependency(parent='-1', pos='MD', label='ROOT')]
        '''
        if not dependencies:
            return
        deps = []
        new_pos = []
        for dependency in dependencies:
            deps.append(dependency.parent + ':' + dependency.label)
            new_pos.append(dependency.pos)
        self.pos = ' '.join(new_pos)
        self.dependency = ' '.join(deps)

    def to_json(self, version=1.0):
        '''
        Converts the Sentence object to the corresponding JSON string
        according to the given API version (default 1.0).

        :param version: The API version to target.
        :type version: float
        :returns: A JSON string.
        :rtype: str
        '''
        return json.dumps(self.to_api_dict(version))

    def to_api_dict(self, version=1.0):
        '''
        Serializes the Sentence object to a dict conforming to the
        specified API version (default 1.0).

        :param version: The API version to target.
        :type version: float
        :returns: A dict with the correct keys as defined in the API.
        :rtype: dict
        '''
        key_map = self.API_MAPPINGS[version]
        return {key_map[key]: value for key, value in
                self.as_dict().iteritems() if key in key_map and \
                value is not None}
            
    sentence = property(get_sentence, set_sentence)
    pos_tags = property(get_pos_tags, set_pos_tags)
    tokens = property(get_tokens)
    pos_tags_list = property(get_pos_tags_list, set_pos_tags_list)
    pos_tag_string = property(get_pos_tags_string, set_pos_tags_string)
    dependency_list = property(get_dependency_list, set_dependency_list)
    
class XMLContent(object):
    
    SUPPORTED_XML_VERSIONS = {XML2005.VERSION: XML2005, 
                              XML2013.VERSION: XML2013, 
                              XMLDeprecated.VERSION: XMLDeprecated}
    API_MAPPINGS = {
        1.0: {
            'lang': 'language_id',
            'title': 'title',
            }
        }
    
    def __init__(self, xml_content, remove_duplicates=True):
        self.xml_version = None
        self.attributes = {}
        self.sentence_objects = []
        self.titles = []
        self.remove_duplicates = remove_duplicates
        
        self.body_annotations = []
        self.title_annotations = []
        self.features = {}
        self.relations = {}

        result = self.parse_xml_content(xml_content, remove_duplicates)
        
        if result: 
            self.xml_version, self.attributes, self.sentence_objects, \
            self.title_annotations, self.body_annotations, self.titles, \
            self.features, self.relations = result
        pass

    @classmethod
    def convert(cls, xml_content, target_version):
        xml = XMLContent(xml_content)
        return xml.get_xml_document(xml_version=target_version)

    @classmethod
    def parse_xml_content(cls, xml_content, remove_duplicates=True):
        xml_version = cls.get_xml_version(xml_content)
        
        if not xml_version or not xml_content:
            return None
        
        sentence_objects = []
        annotation_objects = []
        parser = cls.SUPPORTED_XML_VERSIONS[xml_version]
        
        attributes, sentences, title_annotations, body_annotations, features, \
            relations = parser.parse(xml_content, remove_duplicates)
        
        if 'title' in attributes:
            titles = [Sentence(value=attributes['title'], is_title=True)]
        else: 
            titles = []
        
        for sentence in sentences:
            sent_obj = Sentence(**sentence) 
            
            if sent_obj.is_title: 
                titles.append(sent_obj)
            else: 
                sentence_objects.append(sent_obj)
                
        for annotation in body_annotations:
            annotation_obj = Annotation(**annotation) 
            annotation_objects.append(annotation_obj)
        return xml_version, attributes, sentence_objects, title_annotations, \
                annotation_objects, titles, features, relations
    
    @classmethod
    def get_xml_version(cls, xml_content):
        if not xml_content: 
            return None
        
        for version, xml_parser in cls.SUPPORTED_XML_VERSIONS.iteritems():
            if xml_parser.is_supported(xml_content):
                return version
            
    def get_xml_document(self, header_fields='all', 
                         sentence_attributes=SENTENCE_ATTRIBUTES, 
                         annotations=None,
                         xml_version=XML2013.VERSION):

        '''
        :param header_fields: the header_fields to include
        :param sentence_attributes: sentence attributes to include
        :param annotations, optionally
        :param xml_version: version of the webLyzard XML format to use (XML2005.VERSION, *XML2013.VERSION*)
        :returns: the XML representation of the webLyzard XML object
        '''
        
        if not xml_version: 
            xml_version = self.xml_version

        if not hasattr(self, 'features'):
            self.features = {}
            
        if not hasattr(self, 'relations'):
            self.relations = {}
            
        return self.SUPPORTED_XML_VERSIONS[xml_version].dump_xml(titles=self.titles,
                                                                 attributes=self.attributes, 
                                                                 sentences=self.sentences,
                                                                 annotations=annotations,
                                                                 features=self.features,
                                                                 relations=self.relations)

    def get_plain_text(self):
        ''' :returns: the plain text of the XML content '''
        if not len(self.sentences):
            return ''
        return '\n'.join([s.value for s in self.sentences if not s.is_title])
    
    @classmethod
    def get_text(cls, text):
        ''' :returns: the utf-8 encoded text ''' 
        if isinstance(text, str):
            text = text.decode('utf-8')
        return text

    def add_attribute(self, key, value):
        if not self.attributes: 
            self.attributes = {}
        self.attributes[key] = value

    def update_attributes(self, new_attributes):
        '''
        Updates the existing attributes with new ones 
        
        :param new_attributes: The new attributes to set.
        :type new_attributes: dict
        '''
        
        # not using dict.update to allow advanced processing
        
        if not new_attributes or not isinstance(new_attributes, dict):
            return
        
        for k, v in new_attributes.iteritems():
            self.attributes[str(k)] = v

    def as_dict(self, mapping=None, 
                ignore_non_sentence=False, add_titles_to_sentences=False):
        ''' convert the XML content to a dictionary.

        :param mapping: an optional mapping by which to restrict/rename \
            the returned dictionary
        :param ignore_non_sentence: if true, sentences without without POS tags \
            are omitted from the result
        '''
        try:
            assert mapping, 'got no mapping'
            result = self.apply_dict_mapping(self.attributes, mapping)
            sentence_attr_name = mapping['sentences'] if 'sentences' in mapping else 'sentences' 
            
            if 'sentences_map' in mapping:
                result[sentence_attr_name] = []
                sent_mapping = mapping['sentences_map']
                
                if add_titles_to_sentences and len(self.titles): 
                    sentences = self.titles + self.sentences
                else: 
                    sentences = self.sentences
            
                for sent in sentences: 
                    
                    if ignore_non_sentence and not sent.pos: 
                            continue
                    
                    sent_attributes = self.apply_dict_mapping(sent.as_dict(),
                                                              sent_mapping)
                    result[sentence_attr_name].append(sent_attributes)
                    
            annotation_attr_name = mapping['body_annotations'] \
                    if 'body_annotations' in mapping else 'body_annotations' 
            if 'annotations_map' in mapping:
                result[annotation_attr_name] = []
                annotation_mapping = mapping['annotations_map']            
                for annotation in self.body_annotations:                     
                    annotation_attributes = self.apply_dict_mapping(annotation.as_dict(),
                                                              annotation_mapping)
                    result[annotation_attr_name].append(annotation_attributes)
        except Exception:
            result = self.attributes
            result.update({'sentences': [sent.as_dict() for sent in self.sentences]})
        
        return result

    @classmethod
    def apply_dict_mapping(cls, attributes, mapping=None):
        result = attributes
        
        if mapping:
            result = {} 
            for attr, value in attributes.iteritems():
                if attr in mapping:
                    result[mapping[attr]] = value
            
        return result

    def to_api_dict(self, version=1.0):
        '''
        Transforms the XMLContent object to a dict analoguous to the
        API JSON definition in the given version.

        :param version: The version to conform to.
        :type version: float
        :returns: A dict.
        :rtype: dict
        '''
        document_dict = self.as_dict()
        api_dict = {}
        for key in self.API_MAPPINGS[version]:
            if key in document_dict:
                api_dict[self.API_MAPPINGS[version][key]] = \
                         document_dict[key]
        if self.sentences and len(self.sentences) > 0:
            sentences = [s.to_api_dict(version) for s in self.sentences]
            api_dict['sentences'] = sentences
        if self.titles and len(self.titles) > 0:
            for t in self.titles:
                api_dict['sentences'] = [t.to_api_dict(version)] + api_dict.get('sentences', [])
                if 'title' not in api_dict:
                    api_dict['title'] = t.value
#                 elif api_dict['title'] != t.value:
#                     raise Exception('Mismatch between sentence marked as title and '+\
#                                     'title attribute:\n'+\
#                                     '%s != %s' % (t.value, api_dict['title']))
        annotations = document_dict.get('annotations', None)
        if annotations:
            api_dict['annotations'] = annotations
            
        return api_dict


    def to_json(self, version=1.0):
        '''
        Serializes the XMLContent object to JSON according to the
        specified version.

        :param version: The version to conform to.
        :type version: float
        :returns: A JSON string.
        :rtype: str
        '''
        return json.dumps(self.to_api_dict(version=version))

    def _get_attribute(self, attr_name):
        ''' ::returns: the attribute for the given name '''
        return self.attributes.get(attr_name, None)
    
    def get_nilsimsa(self):
        return self._get_attribute('nilsimsa')
    
    def get_content_type(self):
        return self._get_attribute('content_type')
    
    def get_title(self):
        return self._get_attribute('title')
    
    def get_lang(self):
        return self._get_attribute('lang')

    def get_content_id(self):
        content_id = self._get_attribute('content_id') 
        return int(content_id) if content_id else content_id
     
    def get_sentences(self):
        return self.sentence_objects
    
    def update_sentences(self, sentences):
        ''' 
        updates the values of the existing sentences. if the list of 
        sentence object is empty, sentence_objects will be set to the new
        sentences. 

        :param sentences: list of Sentence objects 

        .. warning:: this function will not add new sentences
        '''
        if not self.sentence_objects:
            self.sentence_objects = sentences 
        else:
            sentence_dict = dict((sent.md5sum, sent) for sent in sentences)
            
            for sentence in self.sentence_objects:
                if sentence.md5sum in sentence_dict:
                    new_sentence = sentence_dict[sentence.md5sum]
                    for attrib in SENTENCE_ATTRIBUTES:
                        new_value = getattr(new_sentence, attrib)
                        if new_value:
                            setattr(sentence, attrib, new_value)

    sentences = property(get_sentences, update_sentences)    
    plain_text = property(get_plain_text)
    nilsimsa = property(get_nilsimsa)
    content_type = property(get_content_type)
    title = property(get_title)
    lang = property(get_lang)    
    content_id   = property(get_content_id) 