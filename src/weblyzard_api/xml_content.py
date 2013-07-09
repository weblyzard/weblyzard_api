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

import unittest
import logging
from lxml import etree

DOCUMENT_NAMESPACE  = {'wl': 'http://www.weblyzard.com/wl/2013#',
                       'dc': 'http://purl.org/dc/elements/1.1/',
                       'xml': 'http://www.w3.org/XML/1998/namespace',
                       }

SENTENCE_ATTRIBUTES = {
    'pos_tag_string': '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'pos'), 
    'token_indices' : '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'token'),
    'significance'  : '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'significance'),
    'sem_orient'    : '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'sem_orient'),
    'md5sum'        : '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'id'),
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
                                  'pos_tag_string': 'pos',
                                  'sem_orient'    : 'sem_orient',
                                  'significance'  : 'significance' }.items()

    def __init__(self, md5sum, pos_tag_string=None, token_indices=None, 
                 sem_orient=None, sentence=None, significance=None, is_title=False):
        '''
        @param pos_tag_string: a string containing the sentences pos
                               tags (e.g. 'NN VB NN')
        @param token_indices: a string containing the token indices
                              (e.g. '0:1 3:12')

        '''
        self.md5sum = md5sum
        self.pos_tag_string = pos_tag_string
        self.sem_orient = sem_orient
        self.sentence = sentence
        self.significance = significance
        self.token_indices = token_indices
        self.is_title = is_title
        
    def as_dict(self):
        '''
        @return: a dictionary representation of the given sentence object
              that can be used for REST services.
        '''
        return { dictattr: getattr(self, key) for key, dictattr in 
                     self.ATTRIBUTE_TO_DICT_MAPPING if getattr(self, key) }

    def get_pos_tags(self):
        '''
        @return: a list of the sentence's POS tags
        '''
        if not self.pos_tag_string:
            return []
        else:
            return self.pos_tag_string.split(" ")

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


    # convenient functions for directly accessing 
    # pos tags and tokens
    pos_tags = property(get_pos_tags)
    tokens   = property(get_token)


class XMLContent(object):
    SENTENCE_XPATH = './/wl:sentence'
    
    def __init__(self, xml_content):
        ''' '''
        if xml_content and xml_content.find(DOCUMENT_NAMESPACE['wl']) == -1:
            raise ValueError("Unsupported XML format.")
        self.root, self.attributes = self._set_root(xml_content)
        self.sentence_objects = []
        self.sentence_objects = self.get_sentences()

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

    def get_plain_text(self):
        ''' returns the plain text of the XML content '''
        if not len(self.sentences):
            return ''
        return '\n'.join([sent.sentence for sent in self.sentences])

    def get_attribute(self, namespace, attr):
        wl_page = self.root.find(".")
        return wl_page.attrib['{%s}%s' % (DOCUMENT_NAMESPACE[namespace], attr)]
        
 
    def get_content_id(self):
        return self.get_attribute('wl', 'id')

    def get_nilsimsa(self):
        return self.get_attribute('wl', 'nilsimsa')

    def get_title(self):
        return [ s for s in self.sentences if s.is_title ] 

    def get_lang(self):
        wl_page = self.root.find(".")
        return wl_page.get('xml:lang', None)

    def get_content_type(self):
        return self.get_attribute('dc', 'format')

    @staticmethod
    def get_text(text):
        ''' encodes the text ''' 
        if isinstance(text, str):
            text = text.decode('utf-8')
        return text
 
   
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
        <wl:page xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://www.weblyzard.com/wl/2013#" wl:id="99933" dc:format="text/html" xml:lang="en" wl:nilsimsa="c3f00c9bae798a55a013209ceba9012f4d2349f7c1b2486529674a05ef7be8fb" dc:related="http://www.heise.de http://www.kurier.at">
           <wl:sentence wl:id="27cd03a5aaac20ae0dba60038f17fdad" wl:is_title="True" wl:pos="JJ NN ." wl:token="0,6 7,14 14,15" wl:sem_orient="0.0" wl:significance="1.5"><![CDATA[Global Dimming.]]></wl:sentence>
           <wl:sentence wl:id="7f3251087b6552159846493558742f18" wl:pos="( CD NNP NN ) IN NNS VBD IN DT CD , NNS VBP VBN IN EX VBZ VBN DT NN IN NN VBG DT NNP : PRP VBD PRP JJ NN ." wl:token="0,1 1,2 2,6 7,18 18,19 20,25 26,38 39,44 45,47 48,51 52,57 57,58 59,69 70,74 75,85 86,90 91,96 97,100 101,105 106,107 108,115 116,118 119,127 128,136 137,140 141,146 146,147 148,152 153,159 160,162 163,169 170,177 177,178" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[(*FULL DOCUMENTARY) Since measurements began in the 1950s, scientists have discovered that there has been a decline of sunlight reaching the Earth; they called it global dimming.]]></wl:sentence>
           <wl:sentence wl:id="93f56b9d196787d1cf662a06ab5f866b" wl:pos="CC VBG TO DT NN VBN IN DT NN IN NNP , DT NN VBD RB VB IN DT CD CC RB IN DT CD NNS VBP VBN DT JJ VBG ." wl:token="0,3 4,13 14,16 17,18 19,24 25,34 35,37 38,41 42,49 50,52 53,60 60,61 62,65 66,73 74,77 78,81 82,90 91,95 96,99 100,105 106,109 110,116 117,122 123,126 127,132 133,143 144,148 149,157 158,159 160,170 171,182 182,183" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[But according to a paper published in the journal of Science, the dimming did not continue into the 1990s and indeed since the 1980s scientists have observed a widespread brightening.]]></wl:sentence>
         </wl:page>
         '''
        # reference data sets
        self.sentence_pos_tags = {'27cd03a5aaac20ae0dba60038f17fdad':
                                  'JJ NN',
                                  '7f3251087b6552159846493558742f18': 
                                  ' ( CD NNP NN ) IN NNS VBD IN DT CD , NNS VBP'
                                  ' VBN IN EX VBZ VBN DT NN IN NN VBG DT NNP :'
                                  ' PRP VBD PRP JJ NN .'.split(),
                                  '93f56b9d196787d1cf662a06ab5f866b':
                                  ' CC VBG TO DT NN VBN IN DT NN IN NNP , DT NN'
                                  ' VBD RB VB IN DT CD CC RB IN DT CD NNS VBP'
                                  ' VBN DT JJ VBG .'.split() }
        self.sentence_tokens = {'27cd03a5aaac20ae0dba60038f17fdad':
                                 ['Global', 'Dimming'],
                                '7f3251087b6552159846493558742f18':
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
                sentence.tokens, self.sentence_tokens[ sentence.md5sum ]):
                print token, reference_token
                self.assertEqual(token, reference_token)

    def test_token_to_pos_mapping(self):
        ''' verifiy that the number of pos tags corresponds
            to the number of available tokens '''
        xml = XMLContent( self.xml_content )
        for sentences in xml.sentences:
            self.assertEqual( len(sentences.pos_tags), 
                              len( list(sentences.tokens)) )

    def test_update_sentences(self):
       
        xml = XMLContent(self.xml_content)
        for s in xml.sentences: 
            s.pos_tag_string = 'nn nn'
            s.significance = 3
            s.sem_orient = 1
 
        for sentence in xml.sentences:
            assert sentence.significance == 3
            assert sentence.sem_orient == 1
            
        xml_out = xml.get_xml_document()
        assert 'CDATA' in xml_out

    def test_double_sentences(self):
        xml_content = ''' 
         <wl:page xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://www.weblyzard.com/wl/2013#" wl:id="http://www.youtube.com/watch?v=nmywf7a9OlI" dc:format="text/html" xml:lang="en" wl:nilsimsa="4b780db90e79090d000001b4eb8d01bd446b79ff51b26e252d5d2a45eb3be0cb" >
            <wl:sentence wl:id="27cd03a5aaac20ae0dba60038f17fdad" wl:is_title="True" wl:pos="JJ NN ." wl:token="0,6 7,14 14,15" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[Global Dimming.]]></wl:sentence>
            <wl:sentence wl:id="7e985ffb692bb6f617f25619ecca39a9" wl:token="0,3 5,10" wl:pos="DET NN NN"><![CDATA[Der ganze Wortlaut]]></wl:sentence>
            <wl:sentence wl:id="7e985ffb692bb6f617f25619ecca39a9" wl:token="0,3 5,10" wl:pos="DET NN NN"><![CDATA[Der ganze Wortlaut]]></wl:sentence>
         <wl:page> '''
    
        xml = XMLContent(xml_content)
        assert len(xml.sentences) == 2
        xml_out = xml.get_xml_document()
        assert 'CDATA' in xml_out

    def test_empty_content(self):
        xml = XMLContent(None)
        assert '' == xml.get_plain_text()
        assert [] == xml.get_sentences()

    def test_dictionary_export(self):
        xml = XMLContent( self.xml_content )
        assert len(xml.as_dict()) > 0

    def test_missing_sentence_content(self):
        from os.path import join, dirname
        xml_content  = open( join(dirname(__file__), 'test/test-quotes.xml') ).read()
        xml = XMLContent( xml_content )
        for sentence in xml.sentences:
            assert "\"" in sentence.pos_tag_string
        
if __name__ == '__main__':
    unittest.main()
