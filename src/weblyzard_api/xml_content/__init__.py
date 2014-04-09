#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Feb, 27 2013

@author: heinz-peterlang
         albert weichselbraun

Handles the new (http://www.weblyzard.com/wl/2013#) weblyzard
XML format.

Functions added:
 - support for sentence tokens and pos iterators

Remove functions:
 - compatibility fixes for namespaces, encodings etc.
 - support for the old POS tags mapping.
'''

import logging
from lxml import etree

DOCUMENT_NAMESPACE  = {'wl': 'http://www.weblyzard.com/wl/2013#',
                       'dc': 'http://purl.org/dc/elements/1.1/',
                       'xml': 'http://www.w3.org/XML/1998/namespace',
                       }

SENTENCE_ATTRIBUTES = {
    'pos_tag_string': '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'pos'), 
    'token_indices' : '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'token'),
    'dependencies'  : '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'dependencies'),
    'significance'  : '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'significance'),
    'sem_orient'    : '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'sem_orient'),
    'md5sum'        : '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'id'),
    'is_title'        : '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'is_title'),
}.items()

logger = logging.getLogger('wl_core.xml_content')

class Sentence(object):
    '''
    The sentence class used for accessing single sentences.

    Note: the class provides convenient properties for accessing pos tags 
          and tokens:
            .sentence: sentence text
            .tokens  : provides a list of tokens (e.g. ['A', 'new', 'day'])
            .pos_tags: provides a list of pos tags (e.g. ['DET', 'CC', 'NN'])
    '''
    # 'value' is used for the @XMLValue field
    ATTRIBUTE_TO_DICT_MAPPING = { 'sentence'      : 'value', 
                                  'is_title'      : 'is_title',
                                  'md5sum'        : 'id',
                                  'token_indices' : 'token',
                                  'dependencies'  : 'dependencies',
                                  'pos_tag_string': 'pos',
                                  'sem_orient'    : 'sem_orient',
                                  'significance'  : 'significance' }.items()

    XML_MAPPING = {'is_title': '{%s}is_title'  % DOCUMENT_NAMESPACE['wl'], 
                   'md5sum': '{%s}id' % DOCUMENT_NAMESPACE['wl'], 
                   'token_indices': '{%s}token' % DOCUMENT_NAMESPACE['wl'],
                   'pos_tag_string': '{%s}pos' % DOCUMENT_NAMESPACE['wl'], 
                   'dependencies': '{%s}dependencies' % DOCUMENT_NAMESPACE['wl'],
                   'sem_orient': '{%s}sem_orient' % DOCUMENT_NAMESPACE['wl'], 
                   'significance': '{%s}significance' % DOCUMENT_NAMESPACE['wl']}

    def __init__(self, md5sum, pos_tag_string=None, token_indices=None, 
                 sem_orient=None, sentence=None, significance=None, is_title=False, dependencies=None):
        '''
        @param pos_tag_string: a string containing the sentences pos
                               tags (e.g. 'NN VB NN')
        @param token_indices: a string containing the token indices.
                              (e.g. '0:1 3:12')
        @param dependencies: the dependency structure of the sentence as
                             head_index:dependency_type. An index of -1 is
                             used to indicate that no head is present.
                             (e.g. 1:NMOD 3:NMOD 1:SUFFIX 4:SBJ)
        '''
        self.md5sum = md5sum
        self._sentence = None # access via property 
        self.pos_tag_string = pos_tag_string
        self.sem_orient = sem_orient
        self.sentence = sentence
        self.significance = significance
        self.token_indices = token_indices
        self.dependencies = dependencies
        self.is_title = is_title
    
    def as_dict(self):
        '''
        @return: a dictionary representation of the given sentence object
              that can be used for REST services.
        '''
        return { dictattr: getattr(self, key) for key, dictattr in 
                     self.ATTRIBUTE_TO_DICT_MAPPING if getattr(self, key) }

    def get_xml_attributes(self, skip_none_values=False):
        xml_dict = {}
        
        for obj_attr, xml_attr in self.XML_MAPPING.iteritems():
            value = getattr(self, obj_attr)
            if skip_none_values and not value:
                continue    
            xml_dict[xml_attr] = str(value)
            
        return xml_dict

    def get_pos_tags(self):
        '''
        @return: a list of the sentence's POS tags
        '''
        return [] if not self.pos_tag_string else self.pos_tag_string.split(' ')

    def get_token(self):
        '''
        @return: an iterator providing the sentence's tokens 
        '''
        if not self.token_indices:
            raise StopIteration

        tokens = self.token_indices.split(" ")
        for token_pos in tokens:
            start, end = map(int, token_pos.split(","))
            yield self.sentence[start:end]

    def get_sentence(self):
        return self._sentence
    
    def set_sentence(self, sentence):
        if isinstance(sentence, str):
            sentence = sentence.decode('utf-8')
        self._sentence = sentence

    # convenient functions for directly accessing 
    # pos tags and tokens
    pos_tags = property(get_pos_tags)
    tokens   = property(get_token)
    sentence = property(get_sentence, set_sentence)
    
class XMLContent(object):
    SENTENCE_XPATH = './/{%s}sentence' % DOCUMENT_NAMESPACE['wl']

    def __init__(self, xml_content):
        ''' '''
        if xml_content and xml_content.find(DOCUMENT_NAMESPACE['wl']) == -1:
            raise ValueError("Unsupported XML format.")
        self.root, self.attributes = self._set_root(xml_content)
        self.sentence_objects = []
        self.sentence_objects = self.get_sentences()
    
    def __repr__(self):
        return self.get_xml_document()
    
    def __len__(self):
        return len(self.sentences)
    
    @classmethod
    def get_xml_from_dict(cls, attributes, sentences):
        ''' '''
        root = etree.Element('{%s}page' % DOCUMENT_NAMESPACE['wl'], 
                             attrib=attributes, 
                             nsmap=DOCUMENT_NAMESPACE)
        
        for sentence in sentences: 
            sent_obj = etree.SubElement(root, 
                                        '{%s}sentence' % DOCUMENT_NAMESPACE['wl'], 
                                        attrib=sentence.get_xml_attributes(), 
                                        nsmap=DOCUMENT_NAMESPACE)
            sent_obj.text = etree.CDATA(sentence.sentence)
        
        xml_content = etree.tostring(root, encoding='UTF-8', pretty_print=True)
        
        return XMLContent(xml_content)

    def as_dict(self):
        '''
        @return: a dictionary representation of the given
                 XMLDocument that can be used for REST services
        '''
        return {'id'          : self.content_id,
                'sentence'    : [ s.as_dict() for s in self.sentences ],
                'format'      : self.content_type,
                'xml:lang'    : self.lang,
                'nilsimsa'    : self.nilsimsa }

    def _set_root(self, xml_content):
        ''' parses the xml_content and returns the root object and 
            its attributes
        @param xml_content: XML document string
        @return: (lxml root, attributes) 
        ''' 
        root = None
        attributes = {}
        
        if not xml_content: 
            logger.debug('XML content is empty -> thats ok, if not used')
        else:
            # remove the encoding, because lxml doesn't like that in UTF-8 
            # strings
            parser = etree.XMLParser(recover=True, strip_cdata=False)
            root = etree.fromstring(xml_content.replace('encoding="UTF-8"', ''), 
                                    parser=parser)
            attributes = root.attrib
       
        return root, attributes

    @staticmethod
    def get_text(text):
        ''' encodes the text ''' 
        if isinstance(text, str):
            text = text.decode('utf-8')
        return text

# property functions
      
    def get_sentences(self):
        ''' 'extracts the sentences of the root objects
        @return: list of Sentence objects '''
        if len(self.sentence_objects):
            return self.sentence_objects
        
        processed_sentences = set()
        sentences = []
        
        if self.root is None:
            return sentences
        
        for sent_element in self.root.iterfind(self.SENTENCE_XPATH, 
                                               namespaces=DOCUMENT_NAMESPACE):

            sentence_attr = { obj_attr: sent_element.attrib[xml_attr_name]
                              for obj_attr, xml_attr_name in SENTENCE_ATTRIBUTES
                              if xml_attr_name in sent_element.attrib }

            sentence = Sentence(sentence=self.get_text(sent_element.text), 
                                **sentence_attr)
    
            if sentence.md5sum in processed_sentences:
                logger.info('Skipping double sentence %s' % sentence.md5sum)
                continue
    
            processed_sentences.add(sentence.md5sum)
            sentences.append(sentence)

        return sentences
    # TODO: check if function used and remove it ...  
    def update_sentences(self, sentences):
        ''' updates the values of the existing sentences. if the list of 
        sentence object is empty, sentence_objects will be set to the new
        sentences. 
        WARNING: this function will not add new sentences
        @param sentences: list of Sentence objects 
        '''
        if not self.sentence_objects or self.root is None:
            self.sentence_objects = sentences 
        else:
            sentence_dict = { sent.md5sum: sent for sent in sentences }
            
            for sentence in self.sentence_objects:
                if sentence.md5sum in sentence_dict:
                    new_sentence = sentence_dict[sentence.md5sum]
                    for obj_attr_name, _ in SENTENCE_ATTRIBUTES:
                        new_value = getattr(new_sentence, obj_attr_name)
                        if new_value:
                            setattr(sentence, obj_attr_name, new_value)
                            
                            
    def update_attributes(self, new_attributes):
        ''' updates the existing attributes with new ones '''
        
        # not using dict.update to allow advanced processing
        
        for k, v in self.attributes.iteritems():    
            if k in new_attributes and new_attributes[k] <> v:
                self.attributes[str(k)] = str(new_attributes[k])

# property functions

    def get_plain_text(self):
        ''' returns the plain text of the XML content '''
        if not len(self.sentences):
            return ''
        return '\n'.join([sent.sentence for sent in self.sentences])

    def get_attribute(self, namespace, attr):
        wl_page = self.root.find('.')
        return wl_page.attrib['{%s}%s' % (DOCUMENT_NAMESPACE[namespace], attr)]
        
    def get_content_id(self):
        return self.get_attribute('wl', 'id')

    def get_nilsimsa(self):
        return self.get_attribute('wl', 'nilsimsa')

    def get_title(self):
        ''' @returns: all sentences that have a set is_title flag
                      (i.e. are part of the title).
        '''
        return [s for s in self.sentences if s.is_title] 

    def get_lang(self):
        return self.get_attribute('xml', 'lang')

    def get_content_type(self):
        return self.get_attribute('dc', 'format')

    def get_xml_document(self):
        ''' returns the string representation of the xml content '''
        ns = '{%s}' % DOCUMENT_NAMESPACE['wl']
        root = etree.Element( ns + 'page', nsmap=DOCUMENT_NAMESPACE)
        
        for attr, value in self.attributes.iteritems():
            root.set(attr, value)
            
        for sentence in self.sentences:
            child = etree.SubElement(root, ns + 'sentence')
            child.text = etree.CDATA(sentence.sentence)
            for obj_attr_name, xml_attrib_name in SENTENCE_ATTRIBUTES:
                value = getattr(sentence, obj_attr_name)
                if value:
                    child.set(xml_attrib_name, str(value))

        return etree.tostring(root, encoding='UTF-8', pretty_print=True)

    # TODO: check if update_sentences still required
    sentences    = property(get_sentences, update_sentences)    
    content_id   = property(get_content_id)
    nilsimsa     = property(get_nilsimsa)
    content_type = property(get_content_type)
    plain_text   = property(get_plain_text)
    title        = property(get_title)
    lang         = property(get_lang)
    xml_document = property(get_xml_document)
    
