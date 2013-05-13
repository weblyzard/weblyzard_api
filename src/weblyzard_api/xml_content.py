#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Feb, 27 2013

@author: heinz-peterlang
         albert weichselbraun

Successor of the xml_content library.

Functions added:
 - support for sentence tokens and pos iterators

Remove functions:
 - compatibility fixes for namespaces, encodings etc.
 - support for the old POS tags mapping.
'''

import json
import unittest
import logging
from lxml import etree

RDF_NS = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}
WL_NS = {'wl': 'http://www.weblyzard.com/wl/2005'}

SENTENCE_ATTRIBUTES = {'pos_tag_list': 'pos', 
                       'token_list'  : 'token',
                       'significance': 'significance',
                       'sem_orient'  : 'sem_orient',
                       'md5sum'      : 'md5sum' }.items()

logger = logging.getLogger('wl_core.xml_content')

class Sentence(object):
    
    def __init__(self, md5sum, pos_tag_list=None, sem_orient=None, 
                 sentence=None, significance=None, token_list=None):
        self.md5sum = md5sum
        self.pos_tag_list = pos_tag_list.split(" ")
        self.sem_orient = sem_orient
        self.sentence = sentence
        self.significance = significance
        self.token_list = token_list
        
    def as_dict(self):
        '''
        @return: a dictionary representation of the given sentence object
              that can be used for REST services.
        '''
        return {'value'    : self.sentence, # used for the @XMLValue field
                'md5sum'       : self.md5sum,
                'token'    : self.token_list,
                'pos'      : self.pos_tag_list }

    def get_pos_tags(self):
        '''
        @return: a list of the sentence's POS tags
        '''
        if not self.pos_tag_list:
            return []
        else:
            return self.pos_tag_list.split(" ")

    def set_pos_tags(self, pos_tags):
        self.pos_tag_list = pos_tags

    def get_token(self):
        '''
        @return: an iterator providing the sentence's tokens 
        '''
        if not self.token_list:
            raise StopIteration

        tokens = self.token_list.split(" ")
        for token_pos in tokens:
            start, end = map(int, token_pos.split(","))
            yield self.sentence[start:end]

    def set_token(self, token):
        self.token_list = token

    pos_tags = property(get_pos_tags, set_pos_tags)
    token    = property(get_token, set_token)

class XMLContent(object):
    sentence_xpath = './/wl:sentence'
    id_attribute = 'md5sum'
    
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
        return {'content_id'  : self.content_id,
                'title'       : self.title,
                'sentence'    : [ s.as_dict() for s in self.sentences ],
                'content_type': self.content_type,
                'lang'        : self.lang,
                'nilsimsa'    : self.nilsimsa }

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
            # remove the encoding, because lxml doesn't like that in UTF-8 strings
            parser = etree.XMLParser(recover=True, strip_cdata=False)
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
        
        processed_sentences = set()
        sentences = []
        
        if self.root is None:
            return sentences
        
        for sent_element in self.root.iterfind(self.sentence_xpath, 
                                               namespaces=WL_NS):

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

    def get_content_id(self):
        wl_page = self.root.find(".")
        return wl_page.attrib['content_id']

    def get_nilsimsa(self):
        wl_page = self.root.find(".")
        return wl_page.get('nilsimsa', None)

    def get_title(self):
        wl_page = self.root.find(".")
        return wl_page.get('title', None)

    def get_lang(self):
        wl_page = self.root.find(".")
        return wl_page.get('lang', None)

    def get_content_type(self):
        wl_page = self.root.find(".")
        return wl_page.get('content_type', None)

   
    def get_xml_document(self):
        ''' returns the string representation of the xml content '''
        ns = '{%s}' % WL_NS['wl']
        root = etree.Element( 'page', nsmap=WL_NS)
        
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

    sentences    = property(get_sentences, update_sentences)    
    content_id   = property(get_content_id)
    nilsimsa     = property(get_nilsimsa)
    content_type = property(get_content_type)
    plain_text   = property(get_plain_text)
    title        = property(get_title)
    lang         = property(get_lang)
    
class TestXMLContent(unittest.TestCase):
    
    def setUp(self):
        self.xml_content = '''
        <?xml version="1.0" encoding="UTF-8"?>
          <page xmlns:wl="http://www.weblyzard.com/wl/2005" content_id="http://www.youtube.com/watch?v=nmywf7a9OlI" content_type="text/html" lang="en" nilsimsa="4b780db90e79090d000001b4eb8d01bd446b79ff51b26e252d5d2a45eb3be0cb" title="Global Dimming">
             <wl:sentence id="7f3251087b6552159846493558742f18" pos="( CD NNP NN ) IN NNS VBD IN DT CD , NNS VBP VBN IN EX VBZ VBN DT NN IN NN VBG DT NNP : PRP VBD PRP JJ NN ." token="0,1 1,2 2,6 7,18 18,19 20,25 26,38 39,44 45,47 48,51 52,57 57,58 59,69 70,74 75,85 86,90 91,96 97,100 101,105 106,107 108,115 116,118 119,127 128,136 137,140 141,146 146,147 148,152 153,159 160,162 163,169 170,177 177,178"><![CDATA[(*FULL DOCUMENTARY) Since measurements began in the 1950s, scientists have discovered that there has been a decline of sunlight reaching the Earth; they called it global dimming.]]></wl:sentence>\n   
             <wl:sentence id="93f56b9d196787d1cf662a06ab5f866b" pos="CC VBG TO DT NN VBN IN DT NN IN NNP , DT NN VBD RB VB IN DT CD CC RB IN DT CD NNS VBP VBN DT JJ VBG ." token="0,3 4,13 14,16 17,18 19,24 25,34 35,37 38,41 42,49 50,52 53,60 60,61 62,65 66,73 74,77 78,81 82,90 91,95 96,99 100,105 106,109 110,116 117,122 123,126 127,132 133,143 144,148 149,157 158,159 160,170 171,182 182,183"><![CDATA[But according to a paper published in the journal of Science, the dimming did not continue into the 1990s and indeed since the 1980s scientists have observed a widespread brightening.]]></wl:sentence>
        </page>
         '''
        # reference data sets
        self.sentence_pos_tags = {'7f3251087b6552159846493558742f18': 
                                   ' ( CD NNP NN ) IN NNS VBD IN DT CD , NNS VBP'
                                   ' VBN IN EX VBZ VBN DT NN IN NN VBG DT NNP :'
                                   ' PRP VBD PRP JJ NN .'.split(),
                                   '93f56b9d196787d1cf662a06ab5f866b':
                                   ' CC VBG TO DT NN VBN IN DT NN IN NNP , DT NN'
                                   ' VBD RB VB IN DT CD CC RB IN DT CD NNS VBP'
                                   ' VBN DT JJ VBG .'.split(), }
        self.sentence_tokens = {'7f3251087b6552159846493558742f18':
                                 ['(', '*', 'FULL', 'DOCUMENTARY', ')',
                                  'Since', 'measurements', 'began', 'in',
                                  'the', '1950s', ',', 'scientists', 'have',
                                  'discovered', 'that', 'there', 'has', 'been',
                                  'a', 'decline', 'of', 'sunlight', 'reaching',
                                  'the', 'Earth', ';', 'they', 'called', 'it',
                                  'global', 'dimming', '.'
                                 ],
                                 '93f56b9d196787d1cf662a06ab5f866b':
                                 ['But', 'according', 'to', 'a', 'paper',
                                  'published', 'in', 'the', 'journal', 'of',
                                  'Science', ',', 'the', 'dimming', 'did',
                                  'not', 'continue', 'into', 'the', '1990s',
                                  'and', 'indeed', 'since', 'the', '1980s',
                                  'scientists', 'have', 'observed', 'a',
                                  'widespread', 'brightening', '.'
                                 ] 
                                }

    def test_tokenization(self):
        ''' tests the tokenization '''
        xml = XMLContent( self.xml_content )
        for sentence in xml.sentences:
            for token, reference_token in zip(
                sentence.token, self.sentence_tokens[ sentence.md5sum ]):
                print token, reference_token
                self.assertEqual(token, reference_token)

    def test_token_to_pos_mapping(self):
        ''' verifiy that the number of pos tags corresponds
            to the number of available tokens '''
        xml = XMLContent( self.xml_content )
        for sentences in xml.sentences:
            self.assertEqual( len(sentences.pos_tags), 
                              len( list(sentences.token)) )

    def test_update_sentences(self):
        xml_content = self.xml_content
        sentences = (Sentence('7f3251087b6552159846493558742f18'),
                     Sentence('93f56b9d196787d1cf662a06ab5f866b'))
        
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
            <page xmlns:wl="http://www.weblyzard.com/wl/2005" content_id="http://www.youtube.com/watch?v=nmywf7a9OlI" content_type="text/html" lang="en" nilsimsa="4b780db90e79090d000001b4eb8d01bd446b79ff51b26e252d5d2a45eb3be0cb" title="Global Dimming">
                <wl:sentence id="7e985ffb692bb6f617f25619ecca39a9" token="0,3 5,10" pos="DET NN NN"><![CDATA[Der ganze Wortlaut]]></wl:sentence>
                <wl:sentence id="7e985ffb692bb6f617f25619ecca39a9" token="0,3 5,10" pos="DET NN NN"><![CDATA[Der ganze Wortlaut]]></wl:sentence>
            <page> '''
    
        xml = XMLContent(xml_content)
        assert len(xml.sentences) == 1
        xml_out = xml.get_xml_document()
        assert 'CDATA' in xml_out

    def test_empty_content(self):
        xml = XMLContent(None)
        assert '' == xml.get_plain_text()
        assert [] == xml.get_sentences()

        
if __name__ == '__main__':
    unittest.main()
        
