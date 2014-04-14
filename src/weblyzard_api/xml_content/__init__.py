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

import unittest
import hashlib

from weblyzard_api.xml_content.parsers.xml_2005 import XML2005
from weblyzard_api.xml_content.parsers.xml_2013 import XML2013
from weblyzard_api.xml_content.parsers.xml_deprecated import XMLDeprecated

SENTENCE_ATTRIBUTES = ('pos_tags', 'sem_orient', 'significance', 'md5sum',
                       'pos', 'token')

class Sentence(object):
    '''
    The sentence class used for accessing single sentences.

    Note: the class provides convenient properties for accessing pos tags 
          and tokens:
            .sentence: sentence text
            .tokens  : provides a list of tokens (e.g. ['A', 'new', 'day'])
            .pos_tags: provides a list of pos tags (e.g. ['DET', 'CC', 'NN'])
    '''
    
    def __init__(self, md5sum=None, pos=None, sem_orient=None, significance=None, 
                 token=None, value=None, is_title=False, dependencies=None):
        
        if not md5sum and value: 
            m = hashlib.md5()
            m.update(value)
            md5sum = m.hexdigest()
        
        self.md5sum = md5sum
        self.pos = pos
        self.sem_orient = sem_orient
        self.significance = significance
        self.token = token
        self.value = value
        self.is_title = is_title
        self.dependencies = dependencies

    def as_dict(self):
        return dict((k, v) for k, v in self.__dict__.iteritems() if not k.startswith('_'))
        
class XMLContent(object):
    
    SUPPORTED_XML_VERSIONS = {XML2005.VERSION: XML2005, 
                              XML2013.VERSION: XML2013, 
                              XMLDeprecated.VERSION: XMLDeprecated}
    
    def __init__(self, xml_content):
        self.xml_version = None
        self.attributes = {}
        self.sentence_objects = []
        self.titles = []

        result = self.parse_xml_content(xml_content)
        
        if result: 
            self.xml_version, self.attributes, self.sentence_objects, self.titles = result

    @classmethod
    def parse_xml_content(cls, xml_content):
        xml_version = cls.get_xml_version(xml_content)
        
        if not xml_version or not xml_content:
            return None
        
        sentence_objects = []
        parser = cls.SUPPORTED_XML_VERSIONS[xml_version]
        
        attributes, sentences = parser.parse(xml_content)
        
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
                
        return xml_version, attributes, sentence_objects, titles
    
    @classmethod
    def get_xml_version(cls, xml_content):
        if not xml_content: 
            return None
        
        for version, xml_parser in cls.SUPPORTED_XML_VERSIONS.iteritems():
            if xml_parser.is_supported(xml_content):
                return version
            
    def get_xml_document(self, header_fields='all', 
                         sentence_attributes=SENTENCE_ATTRIBUTES, 
                         xml_version=XML2013.VERSION):
        
        if not xml_version: 
            xml_version = self.xml_version

        return self.SUPPORTED_XML_VERSIONS[xml_version].dump_xml(titles=self.titles,
                                                                 attributes=self.attributes, 
                                                                 sentences=self.sentences)

    def get_plain_text(self):
        ''' returns the plain text of the XML content '''
        if not len(self.sentences):
            return ''
        return '\n'.join([s.value for s in self.sentences if not s.is_title])
    
    @classmethod
    def get_text(cls, text):
        ''' encodes the text ''' 
        if isinstance(text, str):
            text = text.decode('utf-8')
        return text

    def add_attribute(self, key, value):
        if not self.attributes: 
            self.attributes = {}
        self.attributes[key] = value

    def update_attributes(self, new_attributes):
        ''' updates the existing attributes with new ones '''
        
        # not using dict.update to allow advanced processing
        
        if not new_attributes or not isinstance(new_attributes, dict):
            return
        
        for k, v in new_attributes.iteritems():
            self.attributes[str(k)] = v

    def as_dict(self):
        d = self.attributes
        d.udpate({'sentences': [sent.as_dict for sent in self.sentences]})
        return d

    def _get_attribute(self, attr_name):
        ''' @return: the attribute for the given name '''
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
        ''' updates the values of the existing sentences. if the list of 
        sentence object is empty, sentence_objects will be set to the new
        sentences. WARNING: this function will not add new sentences
        :param sentences: list of Sentence objects 
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
        sentences = [Sentence('7e985ffb692bb6f617f25619ecca39a9'),
                     Sentence('7e985ffb692bb6f617f25619ecca3910')]
         
        for s in sentences: 
            s.pos_tags = 'nn nn'
            s.significance = 3
            s.sem_orient = 1
         
        xml = XMLContent(xml_content)
 
        print xml.get_xml_document()
     
        for sentence in xml.sentences:
            print sentence.md5sum, sentence.value, sentence.significance
             
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
        assert len(xml.sentences) == 1, 'got %s sentences' % len(xml.sentences)
        xml_out = xml.get_xml_document()
        assert 'CDATA' in xml_out

    def test_empty_content(self):
        xml = XMLContent(None)
        assert '' == xml.get_plain_text()
        assert [] == xml.get_sentences()
 
#     def test_pos_tags(self):
#         xml = XMLContent(self.xml_content)
#         for sentence in xml.sentences:
#             sentence.pos_tags = 'NN NN AA'
# 
#         rdf = xml.get_pos_tags()
#         assert '<rdf:RDF xmlns' in rdf
         
    def test_attributes(self):
        ''' '''  
        xml = XMLContent(self.xml_content)
     
        assert 'Der ganze Wortlaut' in xml.title
        assert xml.lang == 'DE'
        assert xml.content_type == 'text/html'
        assert xml.nilsimsa == None
        assert xml.content_id == 228557824
 
 
    def test_supported_version(self):
 
        new_xml = '''
    <wl:page xmlns:wl="http://www.weblyzard.com/wl/2013#" 
             xmlns:dc="http://purl.org/dc/elements/1.1/" 
             wl:id="578351358" 
             dc:format="text/html" 
             xml:lang="de" 
             wl:nilsimsa="37345e380610614cc7696ac08ed098e05fa64211755da1d4f525ef4cd762726e">
        <wl:sentence 
            wl:pos="NN $( NN APPR ADJA NN VVPP" wl:id="b42bb3f2cb7ed667ba311811823f37cf" 
            wl:token="0,20 21,22 23,38 39,42 43,49 50,56 57,64" 
            wl:sem_orient="0.0" 
            wl:significance="0.0" 
            wl:is_title="true">
                <![CDATA[Freihandelsgespr??che - Erleichterungen f??r kleine Firmen geplant]]>
        </wl:sentence>
        <wl:sentence 
            wl:pos="NE $( NE ( NE ) $( ADJA KON ADJA NN VMFIN APPR NN APPRART NN APPR ART NE VVFIN $." 
            wl:id="05e9a90a82d67702cc19af457222c5b6" 
            wl:token="0,7 7,8 8,18 19,20 20,27 27,28 29,30 31,37 38,41 42,50 51,62 63,69 70,73 74,89 90,94 95,101 102,105 106,109 110,113 114,120 120,121" 
            wl:sem_orient="0.0" wl:significance="0.0">
                <![CDATA[Br??ssel/Washington (APA/dpa) - Kleine und mittlere Unternehmen k??nnen auf Erleichterungen beim Handel mit den USA hoffen.]]>
        </wl:sentence>
        <wl:sentence 
            wl:pos="APPR ART NN APPRART NN NN $( KON NN ( NE ) VVINF ART NN KON ART NE APPR ART ADJA NN $, PRELS PRF ADJA NN ( NE ) VVINF VMFIN $." 
            wl:id="9469bb40cbcbb8fba2e31567e135d43d" 
            wl:token="0,3 4,7 8,21 22,25 26,43 44,51 51,52 53,56 57,77 78,79 79,83 83,84 85,96 97,100 101,103 104,107 108,111 112,115 116,120 121,124 125,132 133,140 140,141 142,145 146,150 151,168 169,180 181,182 182,185 185,186 187,193 194,198 198,199" 
            wl:sem_orient="0.0" 
            wl:significance="0.0">
                <![CDATA[Bei den Verhandlungen zum Transatlantischen Handels- und Investitionsabkommen (TTIP) diskutieren die EU und die USA ??ber ein eigenes Kapitel, das sich mittelst??ndischen Unternehmen (KMU) widmen soll.]]>
        </wl:sentence>
        <wl:sentence 
            wl:pos="PDS VVFIN PIDAT NN APPR ART APPRART NN ADJA ADJA NN $." 
            wl:id="a3e062af32c8b12f4c42ffd57063f531" 
            wl:token="0,3 4,13 14,19 20,26 27,29 30,35 36,38 39,46 47,63 64,75 76,84 84,85" 
            wl:sem_orient="0.0" 
            wl:significance="0.0">
                <![CDATA[Das schreiben beide Seiten in einem am Freitag ver??ffentlichten gemeinsamen Dokument.]]>
        </wl:sentence>
        <wl:sentence 
            wl:pos="ART NN VAFIN ART ADJA ADJA NN $." 
            wl:id="90d951f171fa74fbda2177341906cb77" 
            wl:token="0,3 4,8 9,12 13,16 17,27 28,41 42,53 53,54" 
            wl:sem_orient="0.0" 
            wl:significance="0.0">
                <![CDATA[Das Ziel sei ein leichterer gegenseitiger Marktzugang.]]>
        </wl:sentence>
        <wl:sentence 
            wl:pos="NN NE NE VVFIN APPRART NN ART ADJA NN APPR NE $. &amp;quot; APPRART NN VVFIN PPER ADJD ADJD PTKVZ $. &amp;quot; ART ADJA NN VMFIN ADV APPR ART NN APPR NE VVFIN $, ART ADJD NN VVFIN APPR NN ADV PTKNEG PTKVZ $." 
            wl:id="a4beee1292a24bfa73c7675a03f2d115" 
            wl:token="0,21 22,25 26,34 35,40 41,44 45,54 55,58 59,66 67,84 85,87 88,95 95,96 97,98 98,100 101,107 108,114 115,118 119,127 128,131 132,137 137,138 138,139 140,143 144,152 153,162 163,169 170,174 175,178 179,182 183,189 190,192 193,203 204,215 215,216 217,220 221,228 229,235 236,241 242,246 247,257 258,262 263,268 269,273 273,274" 
            wl:sem_orient="0.0" 
            wl:significance="0.0">
                <![CDATA[US-Verhandlungsf??hrer Dan Mullaney sagte zum Abschluss der vierten Verhandlungsrunde in Br??ssel: ???Im Moment kommen wir wirklich gut voran.??? Die n??chsten Gespr??che sollen noch vor dem Sommer in Washington stattfinden, ein genauer Termin steht nach EU-Angaben noch nicht fest.]]>
        </wl:sentence>
    </wl:page>'''
        old_xml = '''
    <wl:page xmlns:wl="http://www.weblyzard.com/wl/2005" 
             lang="de" 
             title="Freihandelsgespr??che - Erleichterungen f??r kleine Firmen geplant" 
             content_type="text/html" 
             content_id="578351358" 
             nilsimsa="73345e38061061454f686ac08fd498e05fa6421175d5a1d5f525ef48d77a322e">
        <wl:sentence 
            pos_tags="None" 
            sem_orient="0.721687836487" 
            significance="839.529561215" 
            md5sum="b6ec48367959b201fb07f421d0743e50" 
            pos="NE $( NE ( NE ) $( ADJA KON ADJA NN VMFIN APPR NN APPRART NN APPR ART NE VVFIN $." 
            token="0,7 7,8 8,18 19,20 20,27 27,28 29,30 31,37 38,41 42,50 51,62 63,69 70,73 74,89 90,94 95,101 102,105 106,109 110,113 114,120 120,121">
                <![CDATA[Br??ssel/Washington (APA/dpa) - Kleine und mittlere Unternehmen k??nnen auf Erleichterungen beim Handel mit den USA hoffen.]]>    
        </wl:sentence>
        <wl:sentence 
            pos_tags="None" 
            sem_orient="0.68041381744" 
            significance="298.191028195" 
            md5sum="c1940778e578e6748046fe6f5eb06a9b" 
            pos="APPR ART NN APPRART NN NN $( KON NN ( NE ) VVINF ART NN KON ART NE APPR ART ADJA NN $, PRELS PRF ADJA NN ( NE ) VVINF VMFIN $." 
            token="0,3 4,7 8,21 22,25 26,43 44,51 51,52 53,56 57,77 78,79 79,83 83,84 85,96 97,100 101,103 104,107 108,111 112,115 116,120 121,124 125,132 133,140 140,141 142,145 146,150 151,168 169,180 181,182 182,185 185,186 187,193 194,198 198,199">
                <![CDATA[Bei den Verhandlungen zum Transatlantischen Handels- und Investitionsabkommen (TTIP) diskutieren die EU und die USA ??ber ein eigenes Kapitel, das sich mittelst??ndischen Unternehmen (KMU) widmen soll.]]>
        </wl:sentence>
        <wl:sentence 
            pos_tags="None" 
            sem_orient="1.0" 
            significance="197.953352851" 
            md5sum="e865ac842126627352d778df347a16db" 
            pos="PDS VVFIN PIDAT NN APPR ART APPRART NN ADJA ADJA NN $." 
            token="0,3 4,13 14,19 20,26 27,29 30,35 36,38 39,46 47,63 64,75 76,84 84,85">
                <![CDATA[Das schreiben beide Seiten in einem am Freitag ver??ffentlichten gemeinsamen Dokument.]]>
        </wl:sentence>
        <wl:sentence 
            pos_tags="None" 
            sem_orient="1.0" 
            significance="0.0" 
            md5sum="90d951f171fa74fbda2177341906cb77" 
            pos="ART NN VAFIN ART ADJA ADJA NN $." 
            token="0,3 4,8 9,12 13,16 17,27 28,41 42,53 53,54">
                <![CDATA[Das Ziel sei ein leichterer gegenseitiger Marktzugang.]]>
        </wl:sentence>
        <wl:sentence 
            pos_tags="None" 
            sem_orient="0.785674201318" 
            significance="1370.67991114" 
            md5sum="27045cb5143ba9726e767d6df80afafd" 
            pos="NN NE NE VVFIN APPRART NN ART ADJA NN APPR NE $. XY APPRART NN VVFIN PPER ADJD ADJD PTKVZ $. XY ART ADJA NN VMFIN ADV APPR ART NN APPR NE VVFIN $, ART ADJD NN VVFIN APPR NN ADV PTKNEG PTKVZ $." 
            token="0,21 22,25 26,34 35,40 41,44 45,54 55,58 59,66 67,84 85,87 88,95 95,96 97,98 98,100 101,107 108,114 115,118 119,127 128,131 132,137 137,138 138,139 140,143 144,152 153,162 163,169 170,174 175,178 179,182 183,189 190,192 193,203 204,215 215,216 217,220 221,228 229,235 236,241 242,246 247,257 258,262 263,268 269,273 273,274">
                <![CDATA[US-Verhandlungsf??hrer Dan Mullaney sagte zum Abschluss der vierten Verhandlungsrunde in Br??ssel: ???Im Moment kommen wir wirklich gut voran.??? Die n??chsten Gespr??che sollen noch vor dem Sommer in Washington stattfinden, ein genauer Termin steht nach EU-Angaben noch nicht fest.]]>
        </wl:sentence>
    </wl:page>'''
         
        old_xml_obj = XMLContent(xml_content=old_xml)
        old_xml_str = old_xml_obj.get_xml_document(xml_version=2005) 
        assert old_xml_obj.xml_version == 2005
        assert 'content_id="578351358"' in old_xml_str
        assert len(old_xml_obj.titles) == 1
         
        new_xml_obj = XMLContent(xml_content=new_xml)
        new_xml_str = new_xml_obj.get_xml_document()
        assert new_xml_obj.xml_version == 2013
        assert len(new_xml_obj.titles) == 1
         
        assert 'wl:id="578351358"' in new_xml_str
         
        assert len(old_xml_obj.sentences) == len(new_xml_obj.sentences)

        xml_test_obj = XMLContent(xml_content=new_xml_obj.get_xml_document())
        assert xml_test_obj.xml_version == 2013
         
        print new_xml_obj.get_xml_document()
        print new_xml_obj.get_xml_document(xml_version=2005)
         
        xml_converted = xml_test_obj.get_xml_document(xml_version=2005)
         
        old_xml_obj2 =  XMLContent(xml_content=xml_converted)
         
        assert old_xml_obj2.xml_version == 2005
        assert len(old_xml_obj2.sentences) == 5
        assert len(old_xml_obj2.titles) == 1
        
if __name__ == '__main__':
    unittest.main()
    
