#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import json

from pprint import pprint

from weblyzard_api.xml_content import Sentence, LabeledDependency, XMLContent
from weblyzard_api.tests.test_helper import get_test_data


class TestXMLContent(unittest.TestCase):

    xml_content1 = '''
            <wl:page xmlns:wl="http://www.weblyzard.com/" content_id="228557824" content_type="text/html" lang="DE" title="Der ganze Wortlaut: Offener Brief an Niko Pelinka  | Heute.at   ">
                <wl:sentence id="7e985ffb692bb6f617f25619ecca39a9"><![CDATA[Ich hasse scheiß encodings .... ]]></wl:sentence>
                <wl:sentence id="7e985ffb692bb6f617f25619ecca3910"><![CDATA[Pöses ärbeiten am Wochenende ... scheiß encodings ]]></wl:sentence>
            </wl:page> '''

    xml_content2 = '''
        <?xml version="1.0" encoding="UTF-8"?>
        <wl:page xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://www.weblyzard.com/wl/2013#" wl:id="99933" dc:format="text/html" xml:lang="en" wl:nilsimsa="c3f00c9bae798a55a013209ceba9012f4d2349f7c1b2486529674a05ef7be8fb" dc:related="http://www.heise.de http://www.kurier.at">
           <wl:sentence wl:id="27cd03a5aaac20ae0dba60038f17fdad" wl:is_title="True" wl:pos="JJ NN ." wl:token="0,6 7,14 14,15" wl:sem_orient="0.0" wl:significance="1.5"><![CDATA[Global Dimming.]]></wl:sentence>
           <wl:sentence wl:id="7f3251087b6552159846493558742f18" wl:pos="( CD NNP NN ) IN NNS VBD IN DT CD , NNS VBP VBN IN EX VBZ VBN DT NN IN NN VBG DT NNP : PRP VBD PRP JJ NN ." wl:token="0,1 1,2 2,6 7,18 18,19 20,25 26,38 39,44 45,47 48,51 52,57 57,58 59,69 70,74 75,85 86,90 91,96 97,100 101,105 106,107 108,115 116,118 119,127 128,136 137,140 141,146 146,147 148,152 153,159 160,162 163,169 170,177 177,178" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[(*FULL DOCUMENTARY) Since measurements began in the 1950s, scientists have discovered that there has been a decline of sunlight reaching the Earth; they called it global dimming.]]></wl:sentence>
           <wl:sentence wl:id="93f56b9d196787d1cf662a06ab5f866b" wl:pos="CC VBG TO DT NN VBN IN DT NN IN NNP , DT NN VBD RB VB IN DT CD CC RB IN DT CD NNS VBP VBN DT JJ VBG ." wl:token="0,3 4,13 14,16 17,18 19,24 25,34 35,37 38,41 42,49 50,52 53,60 60,61 62,65 66,73 74,77 78,81 82,90 91,95 96,99 100,105 106,109 110,116 117,122 123,126 127,132 133,143 144,148 149,157 158,159 160,170 171,182 182,183" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[But according to a paper published in the journal of Science, the dimming did not continue into the 1990s and indeed since the 1980s scientists have observed a widespread brightening.]]></wl:sentence>
         </wl:page>
    '''

    xml_content3 = '''
        <?xml version="1.0" encoding="UTF-8"?>
        <wl:page xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://www.weblyzard.com/wl/2013#" wl:id="99933" dc:format="text/html" xml:lang="en" wl:nilsimsa="c3f00c9bae798a55a013209ceba9012f4d2349f7c1b2486529674a05ef7be8fb" dc:related="http://www.heise.de http://www.kurier.at">
           <wl:sentence wl:id="27cd03a5aaac20ae0dba60038f17fdad" wl:is_title="True" wl:pos="JJ NN ." wl:token="0,6 7,14 14,15" wl:sem_orient="0.0" wl:significance="1.5"><![CDATA[Global Dimming.]]></wl:sentence>
           <wl:sentence wl:id="7f3251087b6552159846493558742f18" wl:pos="( CD NNP NN ) IN NNS VBD IN DT CD , NNS VBP VBN IN EX VBZ VBN DT NN IN NN VBG DT NNP : PRP VBD PRP JJ NN ." wl:token="0,1 1,2 2,6 7,18 18,19 20,25 26,38 39,44 45,47 48,51 52,57 57,58 59,69 70,74 75,85 86,90 91,96 97,100 101,105 106,107 108,115 116,118 119,127 128,136 137,140 141,146 146,147 148,152 153,159 160,162 163,169 170,177 177,178" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[(*FULL DOCUMENTARY) Since measurements began in the 1950s, scientists have discovered that there has been a decline of sunlight reaching the Earth; they called it global dimming.]]></wl:sentence>
           <wl:sentence wl:id="93f56b9d196787d1cf662a06ab5f866b" wl:pos="CC VBG TO DT NN VBN IN DT NN IN NNP , DT NN VBD RB VB IN DT CD CC RB IN DT CD NNS VBP VBN DT JJ VBG ." wl:token="0,3 4,13 14,16 17,18 19,24 25,34 35,37 38,41 42,49 50,52 53,60 60,61 62,65 66,73 74,77 78,81 82,90 91,95 96,99 100,105 106,109 110,116 117,122 123,126 127,132 133,143 144,148 149,157 158,159 160,170 171,182 182,183" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[But according to a paper published in the journal of Science, the dimming did not continue into the 1990s and indeed since the 1980s scientists have observed a widespread brightening.]]></wl:sentence>
           <wl:relation key="parent_doc">http://www.twitter.com/parent</wl:relation>
           <wl:relation key="retweeted_from">http://www.twitter.com/original_tweet1</wl:relation>
           <wl:relation key="retweeted_from">http://www.twitter.com/original_tweet2</wl:relation>
           <wl:relation key="retweeted_from">http://www.twitter.com/original_tweet3</wl:relation>
           <wl:relation key="reply_to">http://www.twitter.com/in_reply_to_tweet</wl:relation>
           <wl:feature key="advert">0</wl:feature>
         </wl:page>
    '''
    # reference data sets
    sentence_pos_tags = {'27cd03a5aaac20ae0dba60038f17fdad':
                         'JJ NN',
                         '7f3251087b6552159846493558742f18':
                         ' ( CD NNP NN ) IN NNS VBD IN DT CD , NNS VBP'
                         ' VBN IN EX VBZ VBN DT NN IN NN VBG DT NNP :'
                         ' PRP VBD PRP JJ NN .'.split(),
                         '93f56b9d196787d1cf662a06ab5f866b':
                         ' CC VBG TO DT NN VBN IN DT NN IN NNP , DT NN'
                         ' VBD RB VB IN DT CD CC RB IN DT CD NNS VBP'
                         ' VBN DT JJ VBG .'.split()}
    sentence_tokens = {
        '27cd03a5aaac20ae0dba60038f17fdad': ['Global', 'Dimming'],
        '7f3251087b6552159846493558742f18': ['(', '*', 'FULL', 'DOCUMENTARY',
                                             ')', 'Since', 'measurements',
                                             'began', 'in', 'the', '1950s', ',',
                                             'scientists', 'have', 'discovered',
                                             'that', 'there', 'has', 'been',
                                             'a', 'decline', 'of', 'sunlight',
                                             'reaching', 'the', 'Earth', ';',
                                             'they', 'called', 'it', 'global',
                                             'dimming', '.'],
        '93f56b9d196787d1cf662a06ab5f866b': ['But', 'according', 'to', 'a',
                                             'paper', 'published', 'in', 'the',
                                             'journal', 'of', 'Science', ',',
                                             'the', 'dimming', 'did', 'not',
                                             'continue', 'into', 'the', '1990s',
                                             'and', 'indeed', 'since', 'the',
                                             '1980s', 'scientists', 'have',
                                             'observed', 'a', 'widespread',
                                             'brightening', '.']
    }

    def test_update_sentences(self):
        xml_content = self.xml_content1
        sentences = [Sentence('7e985ffb692bb6f617f25619ecca39a9'),
                     Sentence('7e985ffb692bb6f617f25619ecca3910')]

        for s in sentences:
            s.pos_tags = 'nn nn'
            s.significance = 3
            s.sem_orient = 1

        xml = XMLContent(xml_content)

        print(xml.get_xml_document())

        for sentence in xml.sentences:
            print(sentence.md5sum, sentence.value, sentence.significance)

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

        xml = XMLContent(xml_content, remove_duplicates=False)
        assert len(xml.sentences) == 2, 'got %s sentences' % len(xml.sentences)
        xml_out = xml.get_xml_document()
        assert 'CDATA' in xml_out

    def test_empty_content(self):
        xml = XMLContent(None)
        assert '' == xml.get_plain_text()
        assert [] == xml.get_sentences()

    def test_attributes(self):
        ''' '''
        xml = XMLContent(self.xml_content1)

        assert 'Der ganze Wortlaut' in xml.title
        assert xml.lang == 'DE'
        assert xml.content_type == 'text/html'
        assert xml.nilsimsa == None
        assert xml.content_id == 228557824

    def test_features(self):
        ''' '''
        xml = XMLContent(self.xml_content3)
        assert xml.features and xml.features['advert'] == 0
        pass

    def test_relations(self):
        ''' '''
        xml = XMLContent(self.xml_content3)
        assert xml.relations and 'http://www.twitter.com/original_tweet1' in xml.relations['retweeted_from']
        pass

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

        print(new_xml_obj.get_xml_document())
        print(new_xml_obj.get_xml_document(xml_version=2005))

        xml_converted = xml_test_obj.get_xml_document(xml_version=2005)

        old_xml_obj2 = XMLContent(xml_content=xml_converted)

        assert old_xml_obj2.xml_version == 2005
        assert len(old_xml_obj2.sentences) == 5
        assert len(old_xml_obj2.titles) == 1

    def test_as_dict(self):
        ''' tests exporting the document as dict '''

        xml_content = '''<wl:page xmlns:wl="http://www.weblyzard.com/wl/2005" content_id="495692737" lang="en" nilsimsa="5bb001c8a610a105b1120bb9c4889d33c62b19e1493245cc2f252a83e270646b" title="Keystone report leaves environmental, energy, safety debates far from settled" source_id="12830" jonas_type="http" description="WASHINGTON &amp;mdash; The State Department minimized the climate change impact of building the Keystone XL pipeline in its final environmental review issued on Friday, a key finding as President Barack Obama decides whether to approve the controversial project. Olivier Douliery | Abaca Press/MCT Activists engage in civil disobedience Wednesday, February 13, 2013 at the White House in Washington, D.C., in hopes of pressuring President Barack Obama to reject the Keystone XL oil sands pipeline. http://media.mcclatchydc.com/smedia/2014/01/31/17/06/SoIRM.La.91.jpg &quot; style=&quot;border-left:2px solid #dddddd; padding-left:5px;max-width:100%;&quot;&gt; More News Read more Politics However, the review leaves the..." feed_url="http://rss.wn.com/english/keyword/" original_request_url="http://article.wn.com/view/2014/02/01/Keystone_report_leaves_environmental_energy_safety_debates_f_1/" content_type="text/html">
   <wl:sentence pos_tags="None" sem_orient="0.0" significance="12951.7567942" md5sum="0c8cb136073a20a932f2d6748204ce9b" pos="NNP CD ( NN ) : DT NNP NNP POS JJ JJ NN IN DT NN NN IN DT JJ NN NNS TO DT NNP NNP NNP VBZ VBN PRP VBP IN DT JJ CC JJ NN IN NNP NNP VBZ DT NN IN DT NN ." token="0,4 5,7 8,9 9,18 18,19 20,22 23,26 27,32 33,43 43,45 46,51 52,65 66,76 77,79 80,83 84,92 93,101 102,106 107,110 111,119 120,123 124,129 130,132 133,136 137,141 142,146 147,152 153,155 156,158 159,161 162,166 167,169 170,173 174,187 188,191 192,201 202,208 209,211 212,221 222,227 228,239 240,243 244,256 257,259 260,263 264,272 272,273"><![CDATA[Dec. 23 (Bloomberg) -- The State Department's final environmental assessment of the Keystone pipeline from the Canadian tar sands to the U.S. Gulf Coast is c. We look at the environmental and political impact if President Obama greenlights the construction of the pipeline.]]></wl:sentence>
   <wl:sentence pos_tags="None" sem_orient="0.0" significance="0.0" md5sum="cdc2b1edeec27081819ca4f50e067240" pos="NNP NNP VBZ VBN IN NNS : NNS ." token="0,6 7,15 16,18 19,25 26,28 29,35 35,36 37,42 42,43"><![CDATA[Shihab Rattansi is joined by guests: clima.]]></wl:sentence>
   </wl:page>'''

        expected_result = {'id': 495692737, 'lang': 'en',
                           'sentence': [{'id': '0c8cb136073a20a932f2d6748204ce9b',
                                         'token': '0,4 5,7 8,9 9,18 18,19 20,22 23,26 27,32 33,43 43,45 46,51 52,65 66,76 77,79 80,83 84,92 93,101 102,106 107,110 111,119 120,123 124,129 130,132 133,136 137,141 142,146 147,152 153,155 156,158 159,161 162,166 167,169 170,173 174,187 188,191 192,201 202,208 209,211 212,221 222,227 228,239 240,243 244,256 257,259 260,263 264,272 272,273',
                                         'value': '''Dec. 23 (Bloomberg) -- The State Department's final environmental assessment of the Keystone pipeline from the Canadian tar sands to the U.S. Gulf Coast is c. We look at the environmental and political impact if President Obama greenlights the construction of the pipeline.''',
                                         'pos': 'NNP CD ( NN ) : DT NNP NNP POS JJ JJ NN IN DT NN NN IN DT JJ NN NNS TO DT NNP NNP NNP VBZ VBN PRP VBP IN DT JJ CC JJ NN IN NNP NNP VBZ DT NN IN DT NN .'},
                                        {'id': 'cdc2b1edeec27081819ca4f50e067240',
                                         'token': '0,6 7,15 16,18 19,25 26,28 29,35 35,36 37,42 42,43',
                                         'value': 'Shihab Rattansi is joined by guests: clima.',
                                         'pos': 'NNP NNP VBZ VBN IN NNS : NNS .'}]}

        xml_obj = XMLContent(xml_content)

        attr_mapping = {'content_id': 'id',
                        'lang': 'lang',
                        'sentences': 'sentence',
                        'sentences_map': {'pos': 'pos',
                                          'token': 'token',
                                          'md5sum': 'id',
                                          'value': 'value'}}

        result = xml_obj.as_dict(mapping=attr_mapping)

        print('result: ')
        pprint(result)

        print('expected result')
        pprint(expected_result)
        assert result == expected_result

        # add the titles
        result2 = xml_obj.as_dict(mapping=attr_mapping,
                                  add_titles_to_sentences=True)
        assert len(result2['sentence']) == 3

        # ignore non-sentences (without pos tags)
        result3 = xml_obj.as_dict(mapping=attr_mapping,
                                  ignore_non_sentence=True,
                                  add_titles_to_sentences=True)
        assert len(result3['sentence']) == 2

    def test_2013_to_2005(self):
        xml = '''<wl:page xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://www.weblyzard.com/wl/2013#" wl:id="1234" dc:format="text/html" xml:lang="de" wl:nilsimsa="c131b2b10e82b95c36635540b7bbdf0704a7f8db022025e03a80b0c0205b5ea9">
   <wl:sentence wl:id="27c236ff13ce52930c4b3cbc47c63e0d" wl:pos="ADJA ADV ADJD $," wl:token="0,10 11,13 14,28 28,29" wl:is_title="true" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[@neuholder So eidesstattlich,]]></wl:sentence>
   <wl:sentence wl:id="0b1bd9b348e90e02738da7d20db09196" wl:pos="ADJA ADV ADJD $, PWAV ART NN ART ADJA NN" wl:token="0,10 11,13 14,28 28,29 30,33 34,37 38,47 48,51 52,58 59,65" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[@neuholder So eidesstattlich, wie die Erklärung der Wiener Grünen]]></wl:sentence>
   <wl:sentence wl:id="c02b4e7c55c7cc7a09770e1879a2c029" wl:pos="APPRART NN ART NN $." wl:token="0,3 4,20 21,24 25,35 35,36" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[zur Demokratisierung des Wahlrechts?]]></wl:sentence>
   <wl:sentence wl:id="83823c9e7a165700828acb374c15d68f" wl:pos="XY ADJD XY XY" wl:token="0,1 1,4 4,5 6,17" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[*lol* @Peter_Pilz]]></wl:sentence>
</wl:page>'''

        xml_obj = XMLContent(xml)
        assert len(xml_obj.sentences) == 3, 'got %s sentences' % len(
            xml_obj.sentences)
        assert len(xml_obj.titles) == 1, 'got %s titles' % len(xml_obj.titles)

        xml2005 = xml_obj.get_xml_document(xml_version=2005)
        xml2013 = xml_obj.get_xml_document(xml_version=2013)

        assert 'id="0b1bd9b348e90e02738da7d20db09196"' not in xml2005
        assert 'md5sum="0b1bd9b348e90e02738da7d20db09196"' in xml2005

        assert 'wl:id="0b1bd9b348e90e02738da7d20db09196"' in xml2013
        assert 'md5sum="0b1bd9b348e90e02738da7d20db09196"' not in xml2013

    def test_tokenization(self):
        ''' tests the tokenization '''
        xml = XMLContent(self.xml_content2)
        for sentence in xml.sentences:
            for token, reference_token in zip(sentence.tokens,
                                              self.sentence_tokens[sentence.md5sum]):
                print(token, reference_token)
                self.assertEqual(token, reference_token)

    def test_token_to_pos_mapping(self):
        ''' verifiy that the number of pos tags corresponds
            to the number of available tokens '''
        xml = XMLContent(self.xml_content2)
        for sentences in xml.sentences:
            print(self.xml_content2)
            self.assertEqual(len(sentences.pos_tags_list),
                             len(list(sentences.tokens)))

    def test_dictionary_export(self):
        xml = XMLContent(self.xml_content2)
        assert len(xml.as_dict()) > 0

    def test_sentence_tokens(self):
        sent = Sentence('md5sum',
                        pos='NN VVFIN ADV ADV ADJA NN $, KON ADV NN $.',
                        value=u'Horuck-Aktionen bringen da wenig ökonomischen Anreiz, aber vielleicht Wählerstimmen.',
                        token='0,15 16,23 24,26 27,32 33,45 46,52 52,53 54,58 59,69 70,83 83,84')

        result = list(sent.tokens)
        print(result)
        assert result == [u'Horuck-Aktionen', u'bringen', u'da', u'wenig',
                          u'ökonomischen', u'Anreiz', u',', u'aber', u'vielleicht',
                          u'Wählerstimmen', u'.']

    def test_missing_sentence_content(self):
        xml_content = get_test_data('test-quotes.xml')
        xml = XMLContent(xml_content)
        for sentence in xml.sentences:
            assert "\"" in sentence.pos_tag_string

    def test_pos_with_dependency(self):
        '''
        Test that if an XML's wl:pos tags contain dependency, the pos and
        dependency are handled correctly.
        '''
        xml_content_string = '''<wl:page xmlns:wl="http://www.weblyzard.com/wl/2013#" xmlns:dc="http://purl.org/dc/elements/1.1/" dc:format="html/text" xml:lang="en" wl:id="192292" wl:nilsimsa="15d10438875d418899a17909c2ca05591252b24450b259006242105024d43de4">
          <wl:sentence wl:dependency="2:ADV 2:SBJ 16:DEP 2:VC 3:OBJ 3:P 16:DEP 8:AMOD 16:DEP 8:P 8:COORD 10:P 10:CONJ 14:NMOD 12:COORD 14:P -1:ROOT" wl:id="6e4c1420b2edaa374ff9d2300b8df31d" wl:pos="RB PRP MD VB IN ' CC JJR JJ ' CC ' NN JJR CD ' ." wl:token="0,9 10,12 13,18 19,23 24,28 29,30 30,31 31,32 32,33 33,34 35,38 39,40 40,41 41,42 42,44 44,45 45,46"><![CDATA[Therefore we could show that "x>y" and "y<z.".]]></wl:sentence>
          </wl:page>'''
        xml_content = XMLContent(xml_content_string)
        sentence = xml_content.sentences[0]
        assert sentence.pos_tags_list == [
            'RB', 'PRP', 'MD', 'VB', 'IN', "'", 'CC', 'JJR', 'JJ', "'", 'CC', "'", 'NN', 'JJR', 'CD', "'", '.']
        assert sentence.pos_tag_string == "RB PRP MD VB IN ' CC JJR JJ ' CC ' NN JJR CD ' ."
        assert sentence.dependency_list == [
            LabeledDependency(parent='2', pos='RB', label='ADV'),
            LabeledDependency(parent='2', pos='PRP', label='SBJ'),
            LabeledDependency(parent='16', pos='MD', label='DEP'),
            LabeledDependency(parent='2', pos='VB', label='VC'),
            LabeledDependency(parent='3', pos='IN', label='OBJ'),
            LabeledDependency(parent='3', pos="'", label='P'),
            LabeledDependency(parent='16', pos='CC', label='DEP'),
            LabeledDependency(parent='8', pos='JJR', label='AMOD'),
            LabeledDependency(parent='16', pos='JJ', label='DEP'),
            LabeledDependency(parent='8', pos="'", label='P'),
            LabeledDependency(parent='8', pos='CC', label='COORD'),
            LabeledDependency(parent='10', pos="'", label='P'),
            LabeledDependency(parent='10', pos='NN', label='CONJ'),
            LabeledDependency(parent='14', pos='JJR', label='NMOD'),
            LabeledDependency(parent='12', pos='CD', label='COORD'),
            LabeledDependency(parent='14', pos="'", label='P'),
            LabeledDependency(parent='-1', pos='.', label='ROOT')]
        tmp_dependency = sentence.dependency_list
        sentence.dependency_list = tmp_dependency
        assert sentence.dependency_list == tmp_dependency


class TestSentence(unittest.TestCase):
    '''
    Test for the Sentence class, especially anything for converting
    it to JSON for the API.
    '''
    test_sentence = Sentence(
        md5sum=u'6e4c1420b2edaa374ff9d2300b8df31d',
        pos=u"RB PRP MD VB IN ' CC JJR JJ ' CC ' NN JJR CD ' .",
        sem_orient=0.0,
        significance=None,
        token=u'0,9 10,12 13,18 19,23 24,28 29,30 30,31 31,32 32,33 33,34 35,38 39,40 40,41 41,42 42,44 44,45 45,46',
        value=u'Therefore we could show that "x>y" and "y<z.".',
        is_title=False,
        dependency=u'2:ADV 2:SBJ 16:DEP 2:VC 3:OBJ 3:P 16:DEP 8:AMOD 16:DEP 8:P 8:COORD 10:P 10:CONJ 14:NMOD 12:COORD 14:P -1:ROOT')
    test_sentence_dict = {
        'value': 'Therefore we could show that "x>y" and "y<z.".',
        'id': '6e4c1420b2edaa374ff9d2300b8df31d',
        'is_title': False,
        'pos_list': "RB PRP MD VB IN ' CC JJR JJ ' CC ' NN JJR CD ' .",
        'tok_list': '0,9 10,12 13,18 19,23 24,28 29,30 30,31 31,32 32,33 33,34 35,38 39,40 40,41 41,42 42,44 44,45 45,46',
        'dep_tree': '2:ADV 2:SBJ 16:DEP 2:VC 3:OBJ 3:P 16:DEP 8:AMOD 16:DEP 8:P 8:COORD 10:P 10:CONJ 14:NMOD 12:COORD 14:P -1:ROOT',
        'polarity': 0.0,
    }

    def test_sentence_to_json(self):
        '''
        Tests that Sentence objects can successfully be serialized to
        JSON.
        '''
        assert self.test_sentence.to_json(version=1.0) == \
            json.dumps(self.test_sentence_dict)


if __name__ == '__main__':
    unittest.main()
