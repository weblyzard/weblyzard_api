#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Aug 29, 2016

.. codeauthor: max goebel <mcgoebel@gmail.com>
'''
import unittest

from weblyzard_api.client.annotator_client import Annotator,\
    WEBLYZARD_ANNOTATOR_URL

class AnnotatorTest(unittest.TestCase):
   
    TEXT_ANNOTATION_PROFILE_NAME = 'text'
    TEXT_ANNOTATION_MAPPING = {'<s>%s</s>': ['ana', 'daniela', 'markus'],
                  '<l>%s</l>': ['jasna']}
    XML_ANNOTATION_PROFILE_NAME = 'xml'
    XML_ANNOTATION_MAPPING = {'<wl:re name="%s">%s</s>': ['Büros', 'Umfrage'],
                  '<article>%s</article>': ['Der', 'der', 'Die', 'die', 'Das', 'das']} 
    
    def setUp(self):
        self.annotator = Annotator( WEBLYZARD_ANNOTATOR_URL )
        self.annotator.add_profile(self.TEXT_ANNOTATION_PROFILE_NAME, 
                                   self.TEXT_ANNOTATION_MAPPING)
        self.annotator.add_profile(self.XML_ANNOTATION_PROFILE_NAME, 
                                   self.XML_ANNOTATION_MAPPING)
        
    
    def test_annotation_profile(self):
        assert self.annotator.has_profile(self.TEXT_ANNOTATION_PROFILE_NAME)
        assert not self.annotator.has_profile('unknown')
    
    def test_xml_document_annotation(self):
        annotation_profile = self.XML_ANNOTATION_PROFILE_NAME
        TEST_XML_DOCUMENT_LIST = [{'content_id': '22', 'content':"""<?xml version="1.0" encoding="UTF-8"?>
        <wl:page xmlns:wl="http://www.weblyzard.com/wl/2005" content_id="321893.xml" title="test" lang="de" nilsimsa="5f207e11aed4a894b328aa726fa47cf239921d9551e133f5c1346898de74364f">
           <wl:sentences id="59dbbf534799b60cec4b00d7ad271f35"><![CDATA[Z�rich (Reuter) - Die Besch�ftigungslage bei Schweizer Archikten und Projektierungsb�ros hat sich im dritten Vierteljahr 1996 weiter verschlechtert.]]></wl:sentences>
           <wl:sentences id="3caac23298c31a6d52116abd9011fe90"><![CDATA[Die Auftragsbest�nde h�tten seit Jahresmitte um weitere f�nf Prozent abgenommen, teilte der Schweizerische Ingenieur-und Architekten-Verein (sia) am Donnerstag mit.]]></wl:sentences>
           <wl:sentences id="37024dd0a288599015fdef65ac39f38e"><![CDATA[Bei einer Umfrage bei Projektierungsb�ros meldeten 40 Prozent aller Befragten gegen�ber Ende Juni niedrigere Auftragsbest�nde.]]></wl:sentences>
           <wl:sentences id="429addb9c155915eeda8e029b0a5c764"><![CDATA[Weitere 47 Prozent s�hen eine Stagnation auf tiefem Niveau.]]></wl:sentences>
           <wl:sentences id="9a13e2efa4a03f77d3e1cebd0e5ac71b"><![CDATA[Nur 13 Prozent der B�ros h�tten h�here Auftragsbest�nde verzeichnet.]]></wl:sentences>
           <wl:sentences id="53d4b91a81a8690bb84624a8e883d271"><![CDATA[Der Arbeitsvorrat d�rfte 6,5 Monate reichen, hiess es weiter Die H�lfte der B�ros meldete tiefere Bausummen, 36 Prozent eine Stagnation.]]></wl:sentences>
           <wl:sentences id="d8e47657332291133d503f931fcfbbe4"><![CDATA[In den n�chsten sechs Monaten erwartet �ber ein Drittel der befragten Architekten und fast die H�lfte der Ingenieure eine weitere Verschlechterung der Lage.]]></wl:sentences>
           <wl:sentences id="f042babd9e7ea2134e829df42163084e"><![CDATA[Die meisten B�ros rechnen mit weiter fallenden Preisen.]]></wl:sentences>
        </wl:page>"""}, 
        {'content_id': '23', 'content': """Das Huhn sagt hallo zum Fuchs"""  }]
        d = Annotator( WEBLYZARD_ANNOTATOR_URL )
        print(d.annotate_xml( annotation_profile, 
                              TEST_XML_DOCUMENT_LIST,
                              'wl:sentences', 
                              True))
        
    
    def test_text_document_annotation(self):
        annotation_profile = self.TEXT_ANNOTATION_PROFILE_NAME
        TEST_DOCUMENT_LIST = [{'content_id': "1", 'content': 'ana knowns daniela and gerhard.'} ,
                              {'content_id': "2", 'content': 'i have met jasna at the pool.'} ]
        
        d = Annotator( WEBLYZARD_ANNOTATOR_URL )
        print(d.annotate_text(annotation_profile, TEST_DOCUMENT_LIST))


if __name__ == '__main__':
    unittest.main()
    