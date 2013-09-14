#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase, main

from eWRT.util.module_path import get_resource
from weblyzard_api.xml_content import XMLContent, Sentence


class TestXMLContent(TestCase):
    
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
        xml_content  = open( get_resource(__file__, ('data', 'test-quotes.xml')) ).read()
        xml = XMLContent( xml_content )
        for sentence in xml.sentences:
            assert "\"" in sentence.pos_tag_string
    
    def test_sentence_tokens(self):
        sent = Sentence('md5sum',
                        pos_tag_string='NN VVFIN ADV ADV ADJA NN $, KON ADV NN $.',
                        sentence='Horuck-Aktionen bringen da wenig ökonomischen Anreiz, aber vielleicht Wählerstimmen.', 
                        token_indices='0,15 16,23 24,26 27,32 33,45 46,52 52,53 54,58 59,69 70,83 83,84')
        
        result = list(sent.get_token())
        assert result == [u'Horuck-Aktionen', u'bringen', u'da', u'wenig', 
                          u'ökonomischen', u'Anreiz', u',', u'aber', u'vielleicht', 
                          u'Wählerstimmen', u'.']
        
if __name__ == '__main__':
    main()
