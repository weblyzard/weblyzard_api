#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jun 24, 2012

@author: heinz-peterlang
'''
import json
import unittest
import logging
from lxml import etree

RDF_NS = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}
WL_NS = {'wl': 'http://www.weblyzard.com/wl/2005'}

DEFAULT_NS = 'xmlns:wl="http://www.weblyzard.com/wl/2005"'
SENTENCE_ATTRIBUTES = ('pos_tags', 'sem_orient', 'significance', 'md5sum',
                       'pos', 'token')

logger = logging.getLogger('wl_core.xml_content')

class Sentence(object):
    
    def __init__(self, md5sum, pos_tags=None, sem_orient=None, 
                 sentence=None, significance=None, pos=None, token=None):
        self.md5sum = md5sum
        self.pos_tags = pos_tags
        self.sem_orient = sem_orient
        self.sentence = sentence
        self.significance = significance
        self.token = token
        self.pos = pos

    def as_dict(self):
        '''
        @return: a dictionary representation of the given sentence object
              that can be used for REST services.
        '''
        return {'value': self.sentence.encode('utf-8'), # used for the @XMLValue field
                'id': self.md5sum,
                'token': self.token,
                'pos': self.pos }


class XMLContent(object):
    sentence_xpath = './/wl:sentence'
    id_attribute = 'id'
    
    def __init__(self, xml_content):
        ''' '''
        self.root, self.attributes = self._set_root(xml_content)
        self.sentence_objects = []
        self.sentence_objects = self.get_sentences()
        
    def as_dict(self):
        '''
        @return: a dictionary representation of the given
                 XMLDocument that can be used for REST services
        '''
        return {'content_id': self.content_id,
                'title': self.title,
                'sentence': [s.as_dict() for s in self.sentences],
                'content_type': self.content_type,
                'lang': self.lang,
                'nilsimsa': self.nilsimsa }

    def _set_root(self, xml_content):
        ''' parses the xml_content and returns the root object and its attributes
        @param xml_content: XML document string
        @return: (lxml root, attributes) 
        ''' 
        root = None
        attributes = {}

        if not xml_content: 
            logger.debug('XML content is empty -> thats ok, if not used')
        else:
            if not 'xmlns:wl' in xml_content:
                xml_content = xml_content.replace('<wl:page', 
                                                  '<wl:page %s' % DEFAULT_NS)
            else: 
                xml_content = xml_content.replace('xmlns:wl="http://www.weblyzard.com/"',
                                                  'xmlns:wl="%s"' % WL_NS['wl'])
            # replace the encoding, because lxml doesn't like that in UTF-8 strings
            parser = etree.XMLParser(recover=True, strip_cdata=False)
            xml_content = xml_content.replace("encoding='UTF-8'", 
                                              'encoding="UTF-8"')
            root = etree.fromstring(xml_content.replace('encoding="UTF-8"', ''), 
                                    parser=parser)
            attributes = root.attrib
            if 'content_type' in attributes:
                # TODO: temporal fix: removes double content_type entry
                del root.attrib['content_type']
                root.set('content_type', 'text/html')
        
        return root, attributes
    
    def get_plain_text(self):
        ''' returns the plain text of the XML content '''
        if not len(self.sentences):
            return ''
        return '\n'.join([sent.sentence for sent in self.sentences])
    
    def get_text(self, text):
        ''' encodes the text ''' 
        if isinstance(text, str):
            text = text.decode('utf-8')
        return text
    
    def get_sentences(self):
        ''' 'extracts the sentences of the root objects
        @return: list of Sentence objects '''
        if len(self.sentence_objects):
            return self.sentence_objects
        
        processed_sentences = []
        sentences = []
        
        if self.root is None:
            return sentences
        
        for sent_element in self.root.iterfind(self.sentence_xpath, 
                                               namespaces=WL_NS):
            if 'id' in sent_element.attrib:
                sent_id_attr = 'id'
            else: 
                sent_id_attr = 'md5sum'
                
            sentence = Sentence(md5sum=sent_element.attrib[sent_id_attr],
                                sentence=self.get_text(sent_element.text)) 
    
            if sentence.md5sum in processed_sentences:
                logger.info('Skipping double sentence %s' % sentence.md5sum)
                continue
    
            processed_sentences.append(sentence.md5sum)
    
            for sentence_attr in SENTENCE_ATTRIBUTES:
                if sentence_attr in sent_element.attrib:
                    value = sent_element.attrib[sentence_attr]
                    if not value or value == 'None':
                        value = None
                    else:
                        try:
                            # try to convert strings
                            value = json.loads(value)
                        except ValueError:
                            value = value
                    setattr(sentence, sentence_attr, value)
                
            sentences.append(sentence)

        return sentences
    
    def update_sentences(self, sentences):
        ''' updates the values of the existing sentences. if the list of 
        sentence object is empty, sentence_objects will be set to the new
        sentences. WARNING: this function will not add new sentences
        @param sentences: list of Sentence objects 
        '''
        if not self.sentence_objects or self.root is None:
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

    def update_attributes(self, new_attributes):
        ''' updates the existing attributes with new ones '''
        
        # not using dict.update to allow advanced processing
        
        for k, v in self.attributes.iteritems():    
            if k in new_attributes and new_attributes[k] <> v:
                self.attributes[str(k)] = str(new_attributes[k])
        
    def get_xml_document(self, header_fields='all', 
                         sentence_attributes=SENTENCE_ATTRIBUTES):
        ''' returns the string representation of the xml content '''
        ns = '{%s}' % WL_NS['wl']
        root = etree.Element(ns + 'page', nsmap=WL_NS)
        
        if header_fields == 'all':
            for attr, value in self.attributes.iteritems():
                root.set(attr, value)
        else: 
            for attr in header_fields: 
                if attr in self.attributes: 
                    root.set(attr, self.attributes[attr]) 
                    
        for sentence in self.sentences:
            child = etree.SubElement(root, ns + 'sentence')
            child.text = etree.CDATA(sentence.sentence)
            for sentence_attr in sentence_attributes:
                child.set(sentence_attr, str(getattr(sentence, sentence_attr)))

        return etree.tostring(root, encoding='UTF-8', pretty_print=True)

    def get_pos_tags(self):
        ''' returns the pos_tags as XML/RDF '''
        ns = '{%s}' % RDF_NS['rdf']
        root = etree.Element(ns + 'RDF', nsmap=RDF_NS)

        for sentence in self.sentences:
            child = etree.SubElement(root, ns + 'Description')
            child.text = sentence.pos_tags
            child.set(ns + 'about', sentence.md5sum)

        return '%s\n%s'.strip() % ('<?xml version="1.0" encoding="UTF-8"?>',
                                   etree.tostring(root, encoding='UTF-8', 
                                                  pretty_print=True))

    def _get_attribute(self, attr_name):
        ''' @return: the attribute for the given name '''
        return self.root.get(attr_name, None)
    
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
     
    sentences = property(get_sentences, update_sentences)    
    plain_text = property(get_plain_text)
    nilsimsa = property(get_nilsimsa)
    content_type = property(get_content_type)
    title = property(get_title)
    lang = property(get_lang)    
    content_id   = property(get_content_id) 
    
class TestXMLContent(unittest.TestCase):
    
    def setUp(self):
        '''
        :
        '''
        self.xml_content = '''
            <wl:page xmlns:wl="http://www.weblyzard.com/" content_id="228557824" content_type="text/html" lang="DE" title="Der ganze Wortlaut: Offener Brief an Niko Pelinka  | Heute.at   ">
                <wl:sentence id="7e985ffb692bb6f617f25619ecca39a9"><![CDATA[Ich hasse scheiß encodings .... ]]></wl:sentence>
                <wl:sentence id="7e985ffb692bb6f617f25619ecca3910"><![CDATA[Pöses ärbeiten am Wochenende ... scheiß encodings ]]></wl:sentence>
            </wl:page> '''
    
    def test_update_sentences(self):
        xml_content = self.xml_content
        sentences = (Sentence('7e985ffb692bb6f617f25619ecca39a9'),
                     Sentence('7e985ffb692bb6f617f25619ecca3910'))
        
        for s in sentences: 
            s.pos_tags = 'nn nn'
            s.significance = 3
            s.sem_orient = 1
        
        xml = XMLContent(xml_content)

        print xml.get_xml_document()
    
        for sentence in xml.sentences:
            print sentence.md5sum, sentence.sentence, sentence.significance
            
        xml.sentences = sentences
        
        xml_out = xml.get_xml_document()
        
        for sentence in xml.sentences:
            assert sentence.significance == 3
            assert sentence.sem_orient == 1
            
        assert 'CDATA' in xml_out

    def test_double_sentences(self):
        xml_content = ''' 
            <wl:page xmlns:wl="http://www.weblyzard.com/" content_id="228557824" content_type="text/html" lang="DE" title="Der ganze Wortlaut: Offener Brief an Niko Pelinka  | Heute.at   ">
                <wl:sentence id="7e985ffb692bb6f617f25619ecca39a9"><![CDATA[Der ganze Wortlaut]]></wl:sentence>
                <wl:sentence id="7e985ffb692bb6f617f25619ecca39a9"><![CDATA[Der ganze Wortlaut]]></wl:sentence>
            </wl:page> '''
    
        xml = XMLContent(xml_content)
        assert len(xml.sentences) == 1
        xml_out = xml.get_xml_document()
        assert 'CDATA' in xml_out

    def test_empty_content(self):
        xml = XMLContent(None)
        assert '' == xml.get_plain_text()
        assert [] == xml.get_sentences()

    def test_pos_tags(self):
        xml = XMLContent(self.xml_content)
        for sentence in xml.sentences:
            sentence.pos_tags = 'NN NN AA'

        rdf = xml.get_pos_tags()
        assert '<rdf:RDF xmlns' in rdf
        
    def test_attributes(self):
        ''' '''  
        xml = XMLContent(self.xml_content)
    
        assert 'Der ganze Wortlaut' in xml.title
        assert xml.lang == 'DE'
        assert xml.content_type == 'text/html'
        assert xml.nilsimsa == None
        assert xml.content_id == 228557824
        
if __name__ == '__main__':
    unittest.main()
        