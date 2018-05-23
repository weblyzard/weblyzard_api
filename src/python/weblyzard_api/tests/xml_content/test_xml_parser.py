#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import os

from pickle import load

from weblyzard_api.xml_content.parsers import XMLParser
from weblyzard_api.xml_content.parsers.xml_2005 import XML2005
from weblyzard_api.xml_content.parsers.xml_2013 import XML2013


class TestXMLParser(unittest.TestCase):

    def test_illegal_document_headers_for_lxml(self):
        test_data_path = os.path.join(
            os.path.dirname(__file__),
            '../data',
            'xml_content_with_illegal_header_attributes.pkl')
        with open(test_data_path) as f:
            xml_content = load(f)
            xml_string = xml_content.get_xml_document()
            print(xml_string)
            assert xml_string

#     def test_incomplete_xml_parsing(self):
#         test_data_path = os.path.join(
#             os.path.dirname(__file__),
#             'data',
#             'failing_xml.xml')
#         with open(test_data_path) as f:
#             xml_string = f.read()
#             assert len(xml_string) > 100
#             attributes, sentences, title_annotations, body_annotations, features, \
#                 relations = XML2013.parse(xml_string)
#
#             xml_content = XMLContent(xml_string)
#             assert len(xml_content.sentences) > 0

    def test_scientific_notation_bug(self):
        '''
        make sure that a decoding bug for strings in scientific notation yielding infinity doesn't occur
        '''
        import hashlib

        m = hashlib.md5()
        m.update(
            "\"That triumph for more military spending was an anomaly in the budget blueprint, which would cut spending $5.5 trillion over the next decade.")
        md5sum = m.hexdigest()
        expected = '3120900866903065837e521458088467'
        self.assertEqual(md5sum, expected)
        self.assertEqual(XMLParser.decode_value(md5sum), expected)


class TestXML2005(unittest.TestCase):

    def test(self):
        xml = ''' <wl:page xmlns:wl="http://www.weblyzard.com/wl/2005" 
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
        </wl:sentence></wl:page>'''

        attributes, sentences, title_annotations, body_annotations, features,  \
            relations = XML2005.parse(xml)
        assert len(attributes) == 5
        assert len(sentences) == 1
        assert all(attr in attributes for attr in ('content_id', 'content_type',
                                                   'lang', 'nilsimsa'))
        for sent in sentences:
            assert 'id' not in sent
            assert 'md5sum' in sent


class TestXML2013(unittest.TestCase):

    def test(self):
        xml = '''<wl:page xmlns:wl="http://www.weblyzard.com/wl/2013#" 
             xmlns:dc="http://purl.org/dc/elements/1.1/" 
             wl:id="578351358" 
             dc:format="text/html" 
             xml:lang="de" 
             wl:nilsimsa="37345e380610614cc7696ac08ed098e05fa64211755da1d4f525ef4cd762726e">
        <wl:sentence 
            wl:pos="NN $( NN APPR ADJA NN VVPP" 
            wl:id="b42bb3f2cb7ed667ba311811823f37cf" 
            wl:token="0,20 21,22 23,38 39,42 43,49 50,56 57,64" 
            wl:sem_orient="0.0" 
            wl:significance="0.0"
            wl:is_title="true">
                <![CDATA[Freihandelsgespräche - Erleichterungen für kleine Firmen geplant]]>
        </wl:sentence>
        <wl:annotation
            wl:key="some.url.com"
            wl:surfaceForm="Österreich"
            wl:start="0"
            wl:end="10"
            wl:md5sum="b42bb3f2cb7ed667ba311811823f37cf">
        </wl:annotation></wl:page>'''

        attributes, sentences, _, _, _, _ = XML2013.parse(xml)

        assert len(attributes) == 4
        assert len(sentences) == 1
        assert all(attr in attributes for attr in ('content_id', 'content_type',
                                                   'lang', 'nilsimsa'))
        for sent in sentences:
            assert 'id' not in sent
            assert 'md5sum' in sent


if __name__ == '__main__':
    unittest.main()
