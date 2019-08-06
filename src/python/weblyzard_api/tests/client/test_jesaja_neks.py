#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2016

.. codeauthor: max goebel <mcgoebel@gmail.com>
'''

import unittest

from gzip import GzipFile
from cPickle import load

from weblyzard_api.client.jesaja_ng import JesajaNg

from weblyzard_api.tests.test_helper import get_full_path


class TestJesajaNeks(unittest.TestCase):

    xml_content = '''
<wl:page xmlns:wl="http://www.weblyzard.com/wl/2013#" xmlns:ma="http://www.w3.org/ns/ma-ont#" xmlns:dc="http://purl.org/dc/elements/1.1/" original_request_url="http://derstandard.at/2000014426852/Soziale-Medien-fuer-die-Nachrichtenverbreitung?ref=rss" source_id="11467" dc:format="text/html" dc:title="Journalismus - Social Media für die Nachrichtenverbreitung" xml:lang="de" wl:id="1243661964" wl:jonas_type="http" wl:nilsimsa="7b30d8322a12a94e12618a60fef8cae144aaae914951a1f59d132a90ca35f247"> <wl:sentence wl:id="060ed6ac1243488b7bb613218a559443" wl:is_title="true"><![CDATA[Journalismus - Social Media für die Nachrichtenverbreitung]]></wl:sentence>
  <wl:sentence wl:dependency="10:adpmod 0:adpobj 1:adpmod 2:adpobj 10:auxpass 10:nsubjpass 10:adpmod 9:det 9:amod 6:adpobj -1:ROOT" wl:id="bbe56bd8da7d00c4c4631db3c21434b3" wl:pos="APPRART NN APPR NE VAFIN NN APPR ART ADJA NN VVPP" wl:significance="6474.394537668186" wl:token="0,4 5,25 26,28 29,36 37,43 44,54 55,58 59,62 63,72 73,86 87,98"><![CDATA[Beim Journalismusfestival in Perugia werden Reaktionen auf die geänderte Mediennutzung präsentiert]]></wl:sentence>
  <wl:sentence wl:dependency="6:det 5:advmod 5:adpmod 4:amod 2:adpobj 6:amod 10:nsubj 10:adpmod 9:amod 7:adpobj -1:ROOT 14:advmod 14:advmod 14:det 10:attr 18:p 18:aux 18:dobj 10:NMOD 18:cc 22:advmod 22:aux 18:conj 10:NMOD" wl:id="0eae768acc5f5cca1a27a4c097dc0158" wl:pos="ART ADV APPRART ADJA NN ADJA NN APPRART ADJA NN VAFIN ADJD ADV ART NN $, KOUI PRF VVIZU KON ADV PTKZU VVINF $." wl:sem_orient="0.7647191129018726" wl:significance="6302.26668899656" wl:token="0,3 4,11 12,15 16,23 24,27 28,42 43,63 64,66 67,80 81,88 89,92 93,104 105,109 110,113 114,125 125,126 127,129 130,134 135,148 149,152 153,164 165,167 168,174 174,175"><![CDATA[Das nunmehr zum neunten Mal stattfindenden Journalismusfestival im italienischen Perugia ist alljährlich auch ein Tummelplatz, um sich auszutauschen und voneinander zu lernen.]]></wl:sentence>
  <wl:sentence wl:dependency="1:amod 4:nsubj 1:adpmod 2:adpobj -1:ROOT 4:advmod 4:adpmod 8:amod 6:adpobj 8:cc 11:amod 8:conj 13:det 11:poss 21:p 21:adpmod 15:adpobj 21:adpmod 20:det 20:num 17:adpobj 4:rcmod 21:dobj 24:poss 22:poss 24:cc 27:poss 24:conj 21:xcomp 4:p" wl:id="2bd25044b69848d1d096c915409c4b71" wl:pos="ADJA NN KOKOM NE VVFIN ADV KOKOM ADJA NN KON ADJA NN ART NN $, APPR PDAT APPR PIAT CARD NN VVFIN NN PPOSAT NN KON PPOSAT NN VVIZU $." wl:significance="222.3186296147562" wl:token="0,5 6,17 18,21 22,30 31,37 38,45 46,49 50,58 59,74 75,79 80,95 96,109 110,113 114,125 125,126 127,130 131,137 138,141 142,150 151,158 159,171 172,181 182,195 196,201 202,205 206,209 210,214 215,223 224,236 236,237"><![CDATA[Große Unternehmen wie Facebook nutzen genauso wie kleinere Start-Up-Firmen oder journalistische Einzelkämpfer die Möglichkeit, bei diesem von mehreren hundert Journalisten besuchten Branchentreff ihren Weg und ihre Projekte vorzustellen.]]></wl:sentence>
  <wl:sentence wl:dependency="7:adpmod 0:adpmod 3:det 1:adpobj 3:cc 3:conj 3:appos 8:amod 16:nsubj 16:dep 9:p 12:det 16:nsubj 14:det 12:poss 14:appos -1:ROOT 19:det 19:amod 16:dobj 16:p 27:det 26:adpmod 24:det 22:adpobj 24:nmod 27:amod 16:conj 27:p 36:nsubj 31:advmod 36:advmod 36:advmod 36:dobj 33:cc 33:conj 27:rcmod 16:p" wl:id="c42d46eabbd8be93fb9ab9011672e57f" wl:pos="NN APPR ART NN KON NN NE VVFIN NN KON $. ART NN ART NN NE VAFIN ART ADJA NN $. ART APPR ART NN CARD ADJA NN $, PRELS ADV ADV ADJD NN KON NN VVINF $." wl:sem_orient="0.7580980435789034" wl:significance="559.0445660281754" wl:token="0,10 11,14 15,18 19,31 32,35 36,42 43,48 49,54 55,57 57,58 58,59 60,63 64,74 75,78 79,93 94,104 105,108 109,113 114,119 120,130 130,131 132,135 136,140 141,144 145,149 150,154 155,164 165,175 175,176 177,180 181,186 187,191 192,197 198,209 210,213 214,227 228,239 239,240"><![CDATA[Vorwiegend auf die Mobilnutzung und Social Media setzt AJ+. Der US-Ableger des Fernsehsenders Al-Jazerra hat eine klare Zielgruppe: die nach dem Jahr 2000 geborenen Millenials, die immer mehr mobil Nachrichten und Informationen konsumieren.]]></wl:sentence>
  <wl:sentence wl:dependency="16:adpmod 4:adpmod 3:det 1:adpobj 5:amod 0:adpobj 0:cc 0:conj 7:adpobj 8:p 8:conj 8:p 8:conj 8:cc 8:conj 0:cc -1:ROOT 19:det 19:amod 16:nsubj 16:advmod 16:prt 16:p" wl:id="ca25562a1422c88f51d70f631b5064a9" wl:pos="APPR APPR ART NN VVFIN NN KON APPR NE $, NN $, NN KON NN KON VVFIN ART ADJA NN PROAV PTKVZ $." wl:sem_orient="0.6085806194501846" wl:significance="222.3186296147562" wl:token="0,5 6,9 10,14 15,35 36,41 42,44 44,45 46,49 50,57 57,58 59,66 66,67 68,76 77,80 81,90 91,94 95,99 100,103 104,108 109,114 115,120 121,124 124,125"><![CDATA[Statt auf eine Nachrichtenplattform setzt AJ+ auf YouTube, Twitter, Facebook und Instagram und baut die neue Marke dafür auf.]]></wl:sentence>
  <wl:sentence wl:dependency="2:p 2:nsubj -1:ROOT 4:neg 2:dobj 2:NMOD 2:NMOD 2:NMOD 7:adpmod 10:amod 8:adpobj 7:p 2:NMOD 15:advmod 15:compmod 2:NMOD 2:NMOD 2:NMOD 17:adpmod 18:adpobj 2:NMOD 20:adpobj 20:cc 2:NMOD 2:NMOD 24:adpobj 25:adpmod 26:adpobj 2:NMOD" wl:id="49cbcc3a127adcb186ae09a5d01c5131" wl:pos="' PPER VAFIN PIAT NN $, KON NN APPR ADJA NN ' $, ADV NE NE $, FM FM NN APPR NN KON $, APPRART NN APPR NE $." wl:sem_orient="0.7216878364870322" wl:significance="6302.26668899656" wl:token="0,1 1,4 5,10 11,16 17,24 24,25 26,33 34,41 42,45 46,53 54,60 60,61 61,62 63,65 66,71 72,77 77,78 79,83 84,86 87,97 98,101 102,104 104,105 105,106 107,109 110,120 121,123 124,131 131,132"><![CDATA["Wir haben keine Website, sondern Content für soziale Medien", so Jigar Mehta, Head of Engagement bei AJ+, am Donnerstag in Perugia.]]></wl:sentence>
  <wl:sentence wl:id="47f7a2e7f09b2a1d564cabd6bc777240" wl:token="0,15"><![CDATA[Userbeteiligung]]></wl:sentence>
  <wl:sentence wl:dependency="-1:ROOT 0:NMOD 15:adpmod 5:det 5:amod 2:adpobj 7:amod 5:poss 5:cc 5:conj 15:auxpass 15:adpmod 14:det 14:amod 11:adpobj 0:NMOD 19:p 19:nsubj 19:advmod 0:NMOD 19:p 27:mark 27:nsubj 24:advmod 27:adpmod 24:adpobj 27:acomp 19:csubj 0:NMOD" wl:id="fd818a9d1ab59ae0a64623a034e46768" wl:pos="ADJA $, APPR ART ADJA NN ADJA NN KON NN VAFIN APPR ART ADJA NN VVPP $, NN ADV VVFIN $, KOUS PPER ADV APPR NN ADJD VAFIN $." wl:sem_orient="0.982946374365981" wl:significance="451.6501316857136" wl:token="0,5 5,6 7,10 11,14 15,20 21,31 32,45 46,52 53,56 57,65 66,72 73,76 77,80 81,87 88,95 96,106 106,107 108,113 114,116 117,127 127,128 129,133 134,137 138,142 143,147 148,151 152,164 165,169 169,170"><![CDATA[Kurze, auf die junge Zielgruppe ausgerichtete Videos und Grafiken werden für die mobile Nutzung abgestimmt, Filme so produziert, dass sie auch ohne Ton verständlich sind.]]></wl:sentence>
  <wl:sentence wl:dependency="1:advmod -1:ROOT 1:nsubj 1:dobj 1:advmod 1:adpmod 5:adpobj 1:adpmod 10:compmod 10:p 7:adpobj 1:adpmod 13:det 11:adpobj 1:p" wl:id="501201b3f8305ebd9f2d18b4945e972c" wl:pos="PROAV VVFIN PPER NE ADV APPR PIS APPR NN $[ ADV APPR PWAT NN $." wl:token="0,5 6,10 11,13 14,19 20,24 25,28 29,34 35,37 38,53 54,55 56,60 61,64 65,72 73,78 78,79"><![CDATA[Dabei geht es Mehta aber vor allem um Userbeteiligung - egal auf welchem Kanal.]]></wl:sentence>
  <wl:sentence wl:dependency="8:p 8:adpmod 3:det 7:nmod 7:adpmod 6:poss 4:adpobj 1:adpmod -1:ROOT 14:p 14:aux 14:dobj 14:nsubj 14:advmod 8:NMOD 19:p 19:advmod 18:det 19:nsubj 8:NMOD 19:p 23:p 23:advmod 19:appos 8:NMOD" wl:id="586dfbf8990aaaa49365a2a43bc917ca" wl:pos="' KOUI ART NN APPR PPOSAT NN APPR VVFIN $, VMFIN PPER PPER ADV VVFIN $, PWAV ART NN VAFIN ' $, ADV NE $." wl:sem_orient="0.4303314829119352" wl:token="0,1 1,8 9,12 13,23 24,27 28,34 35,40 41,43 44,50 50,51 52,58 59,62 63,66 67,71 72,78 78,79 80,82 83,86 87,91 92,96 96,97 97,98 99,101 102,107 107,108"><![CDATA["Anstatt die Diskussion auf unsere Seite zu leiten, wollen wir sie dort führen, wo die User sind", so Mehta.]]></wl:sentence>
  <wl:sentence wl:dependency="1:advmod 5:adpmod 4:det 4:amod 1:adpobj -1:ROOT 5:nsubj 5:advmod 5:p 10:det 15:dobj 15:adpmod 14:det 14:amod 11:adpobj 5:xcomp 5:p" wl:id="bda47835db3a68d0026ed19f6b613a73" wl:pos="ADV APPR ART ADJA NN VVFIN PIS PROAV $, ART NN APPR ART ADJA NN VVIZU $." wl:token="0,4 5,7 8,13 14,22 23,30 31,36 37,40 41,46 46,47 48,51 52,62 63,66 67,70 71,84 85,109 110,126 126,127"><![CDATA[Erst in einem weiteren Schritt denkt man daran, die Kommentare auf den verschiedenen Social-Media-Plattformen zusammenzuführen.]]></wl:sentence>
  <wl:sentence wl:dependency="1:advmod 5:adpmod 4:det 4:amod 1:adpobj -1:ROOT 5:nsubj 8:det 5:dobj 5:p 5:adpmod 10:adpobj 5:NMOD 15:det 15:amod 12:iobj 15:appos 16:p 16:conj 16:cc 16:conj 12:p" wl:id="ddafa2bfc7a2c2806f288621912b1f09" wl:pos="ADJD APPR ART ADJA NN VVFIN PPER ART NN $. APPR NN VVFIN ART ADJA NN NN $, NN KON NN $." wl:sem_orient="-0.7001400420140049" wl:token="0,10 11,13 14,17 18,26 27,34 35,39 40,42 43,47 48,51 51,52 53,58 59,70 71,76 77,80 81,88 89,93 94,103 103,104 105,117 118,122 123,129 129,130"><![CDATA[Zusätzlich zu den sozialen Kanälen gibt es eine App. Neben Nachrichten macht ein kleines Team Kurzdokus, Erklärvideos oder Satire.]]></wl:sentence>
  <wl:sentence wl:dependency="1:num -1:adpobj 1:NMOD 2:adpmod 5:compmod 3:adpobj 2:adpmod 9:det 9:amod 6:adpobj 2:adpmod 12:det 10:adpobj 19:p 19:mark 16:det 19:nsubj 19:adpmod 17:adpobj 12:rcmod 2:p" wl:id="b76b963c88cefd14838084ec9e0a7ce7" wl:pos="CARD NN VVFIN APPR NE NE APPR ART ADJA NN APPR ART NN $, PRELS ART NN APPRART NN VAFIN $." wl:token="0,2 3,8 9,17 18,20 21,24 25,34 35,39 40,45 46,52 53,57 58,60 61,64 65,71 71,72 73,76 77,80 81,89 90,92 93,110 111,114 114,115"><![CDATA[80 Leute arbeiten in San Francisco seit einem halben Jahr an dem Medium, das ein Start-Up im Mediengroßkonzern ist.]]></wl:sentence>
  <wl:sentence wl:dependency="1:compmod -1:ROOT 1:cc 1:conj" wl:id="5497014a3d21e667f18552f3efd21a25" wl:pos="NE NE KON NN" wl:significance="279.5222830140877" wl:token="0,6 7,12 13,16 17,23"><![CDATA[Social Media und Videos]]></wl:sentence>
  <wl:sentence wl:dependency="1:compmod 11:nsubj 11:p 11:nsubj 11:adpmod 4:adpobj 5:adpmod 6:adpobj 7:cc 7:conj 9:advmod 13:ccomp 13:p -1:ROOT 13:advmod 16:det 13:nsubj 13:p 19:num 31:dobj 22:det 22:amod 19:poss 31:aux 25:poss 31:dobj 27:advmod 31:advmod 31:adpmod 30:amod 28:adpobj 13:NMOD 13:NMOD" wl:id="2a90e7de06442ab948b5ee729467dac1" wl:pos="NE NE $, PRELS APPR NN APPR NN KON NN ADJD VAFIN $, VVFIN PROAV ART NN $. CARD NN ART ADJA NN VAFIN PPOSAT NN ADV ADV APPR ADJA NN VVINF $." wl:significance="222.3186296147562" wl:token="0,4 5,13 13,14 15,18 19,22 23,31 32,35 36,57 58,61 62,73 74,83 84,87 87,88 89,94 95,100 101,106 107,112 112,113 114,116 117,124 125,128 129,135 136,144 145,151 152,156 157,168 169,172 173,177 178,182 183,190 191,197 198,206 206,207"><![CDATA[Andy Mitchell, der bei Facebook für Medienpartnerschaften und Nachrichten zuständig ist, sieht darin einen Trend: 80 Prozent der jungen Menschen würden ihre Nachrichten nur noch über soziale Medien beziehen.]]></wl:sentence>
  <wl:sentence wl:dependency="-1:adpmod 2:det 0:adpobj 0:NMOD 0:NMOD 6:advmod 7:num 0:NMOD 9:det 7:poss 21:p 21:nsubj 21:dobj 21:adpmod 15:det 13:adpobj 21:adpmod 16:adpobj 19:amod 17:poss 21:nsubj 9:rcmod 0:NMOD" wl:id="e03c884b2a0f216e56ccd92c25ad3aca" wl:pos="APPR ART NE VAFIN PPER ADV CARD NN ART NN $, PRELS PRF APPR PDAT NN APPR NN ADJA NN NN ADJD $." wl:sem_orient="0.40422604172722165" wl:significance="2103.881673326629" wl:token="0,2 3,6 7,10 11,15 16,18 19,28 29,31 32,39 40,43 44,55 55,56 57,60 61,65 66,69 70,75 76,81 82,85 86,97 98,108 109,110 111,118 119,127 127,128"><![CDATA[In den USA sind es insgesamt 30 Prozent der Bevölkerung, die sich auf diese Weise mit Nachrichten versorgten – Tendenz steigend.]]></wl:sentence>
  <wl:sentence wl:dependency="1:num 2:num 3:nmod 4:advmod -1:ROOT 14:adpmod 5:adpmod 8:num 6:adpobj 8:adpmod 9:adpobj 5:adpmod 11:adpobj 14:p 4:NMOD 14:nsubj 14:adpmod 16:adpobj 14:adpmod 20:amod 18:adpobj 20:adpmod 21:adpobj 4:NMOD" wl:id="a9268a65ee627ce8284e140ae02899a0" wl:pos="CARD NN NN ADJD VVINF APPR APPR CARD NN APPR NN APPR NE $, VVFIN PPER APPRART NN APPRART ADJA NN APPR NE $." wl:significance="6524.585318611316" wl:token="0,3 4,14 15,23 24,32 33,40 41,44 45,47 48,50 51,54 55,58 59,62 63,65 66,74 74,75 76,86 87,89 90,92 93,103 104,106 107,117 118,129 130,132 133,140 140,141"><![CDATA[1,4 Milliarden Menschen weltweit schauen bis zu 14 Mal pro Tag in Facebook, referierte er am Donnerstag im prächtigen Rathaussaal in Perugia.]]></wl:sentence>
  <wl:sentence wl:dependency="2:det 2:amod 3:dobj -1:ROOT 3:NMOD 4:adpmod 5:adpobj 3:NMOD" wl:id="6d0a6eb9df8a06fd2b5a7a1b013da86e" wl:pos="ART ADJA NN VVFIN NE APPR NN $." wl:token="0,5 6,14 15,20 21,26 27,35 36,38 39,45 45,46"><![CDATA[Einen weiteren Trend sieht Mitchell in Videos.]]></wl:sentence>
  <wl:sentence wl:dependency="4:adpmod 0:adpobj 3:poss 1:poss -1:ROOT 6:det 4:nsubj 8:det 6:poss 4:NMOD 11:det 9:adpobj 11:adpmod 16:det 16:amod 16:num 12:adpobj 4:NMOD 4:NMOD" wl:id="7f728b1b23a729d7e95328a33a9f8e12" wl:pos="APPR NN PPOSAT NN VVFIN ART NN ART NN APPR ART NN APPR ART ADJA CARD NN PTKVZ $." wl:token="0,4 5,16 17,23 24,36 37,42 43,46 47,51 52,55 56,62 63,65 66,69 70,77 78,80 81,84 85,93 94,98 99,105 106,108 108,109"><![CDATA[Nach Schätzungen seines Unternehmens nimmt die Zahl der Videos um das 14fache in den nächsten drei Jahren zu.]]></wl:sentence>
  <wl:sentence wl:dependency="4:mark 4:advmod 3:det 4:dobj 15:advcl 4:cc 12:nsubj 6:advmod 12:advmod 10:neg 11:advmod 12:advmod 4:conj 12:aux 15:p 28:dobj 15:advmod 18:det 15:nsubj 18:appos 15:adpmod 15:prt 28:p 28:adpmod 23:adpobj 27:advmod 27:amod 28:dobj -1:ROOT 28:NMOD" wl:id="d6094357007e5157194da4baf6fe466e" wl:pos="KOUS ADV ART NN VVFIN KON PIS PROAV ADJD PTKNEG ADV ADJD VVINF VMFIN $, VVFIN ADV ART NN NE PROAV PTKVZ $, APPR NN ADV ADJA NN VVIZU $." wl:sem_orient="-0.6804138174397717" wl:token="0,4 5,9 10,13 14,26 27,33 34,37 38,41 42,47 48,54 55,60 61,63 64,67 68,75 76,80 80,81 82,86 87,91 92,95 96,112 113,116 117,121 122,126 126,127 128,130 131,137 138,142 143,152 153,166 167,177 177,178"><![CDATA[Weil auch die Mobilnutzung steigt und man dabei häufig nicht so gut zuhören kann, geht etwa der US-Medienkonzern Vox dazu über, in Videos auch grafische Informationen einzubauen.]]></wl:sentence>
  <wl:sentence wl:dependency="1:advmod -1:ROOT 1:advmod 1:advmod 1:adpmod 6:det 4:adpobj 6:adpmod 7:adpobj 10:compmod 8:appos 1:p" wl:id="312ea95b45c50be0c5dd4a215d5adaaf" wl:pos="ADV VVFIN ADV ADV APPR ART NN APPR NN NE NE $." wl:token="0,2 3,12 13,17 18,24 25,28 29,34 35,44 45,48 49,61 62,68 69,74 74,75"><![CDATA[So geschehen auch jüngst bei einem Interview mit US-Präsident Barack Obama.]]></wl:sentence>
  <wl:sentence wl:dependency="2:advmod 2:compmod 12:nsubj 5:p 5:compmod 2:appos 5:adpmod 10:compmod 10:compmod 10:compmod 6:adpobj 12:p -1:ROOT 12:adpmod 13:p 27:mark 17:amod 27:nsubj 27:adpmod 18:adpobj 27:advmod 27:adpmod 23:advmod 24:amod 21:adpobj 26:advmod 27:acomp 12:NMOD 12:NMOD" wl:id="6490409e82e3bf1becf998dc32e30b8a" wl:pos="ADV NE NE $, NE NN APPR NE NE FM FM $, VVFIN PROAV $, KOUS ADJA NN APPRART NN ADV APPR ADJD ADJA NN ADV ADJD VAINF $." wl:sem_orient="0.33333333333333337" wl:significance="206.752657380957" wl:token="0,4 5,9 10,19 19,20 21,27 28,41 42,45 46,52 53,61 62,66 67,78 78,79 80,87 88,94 94,95 96,100 101,108 109,115 116,119 120,137 138,150 151,154 155,164 165,177 178,189 190,195 196,205 206,212 212,213"><![CDATA[Auch Raju Narisetti, Senior Vizepräsident bei Rupert Murdochs News Corporation, verwies darauf, dass soziale Medien zur Weiterverbreitung insbesondere von aufwendig produzierten Geschichten immer wichtiger werden.]]></wl:sentence>
  <wl:sentence wl:dependency="1:det 2:nsubj -1:ROOT 4:neg 9:advmod 9:adpmod 8:det 8:amod 5:adpobj 2:conj 2:NMOD" wl:id="f921266d883ba15c2b1d606f8aa4ca19" wl:pos="ART NN VVFIN PTKNEG ADV APPR ART ADJA NN VVINF $." wl:token="0,3 4,12 13,20 21,26 27,43 44,47 48,51 52,59 60,68 69,78 78,79"><![CDATA[Die Zugriffe müssten nicht notwendigerweise auf der eigenen Homepage passieren.]]></wl:sentence>
  <wl:sentence wl:dependency="-1:adpobj 22:aux 22:advmod 22:aux 3:adpobj 4:adpmod 7:amod 5:adpobj 3:cc 3:conj 11:amod 22:nsubj 22:advmod 22:adpmod 15:amod 13:adpobj 13:p 18:advmod 13:conj 18:adpobj 13:p 22:aux 0:NMOD 0:NMOD" wl:id="c9ddd2eb8fc4eacdf0fe027f9b43002d" wl:pos="NE VVFIN ADJD APPR NN APPR ADJA NN KON VVFIN ADJA NN ADV APPRART ADJA NN $, ADV APPR NN $, PTKZU VVINF $." wl:sem_orient="1.0" wl:significance="222.3186296147562" wl:token="0,8 9,14 15,21 22,24 25,40 41,44 45,56 57,63 64,67 68,76 77,89 90,98 99,103 104,106 107,124 125,129 129,130 131,135 136,139 140,147 147,148 149,151 152,163 163,164"><![CDATA[Facebook wirbt massiv um Partnerschaften mit etablierten Medien und versucht individuelle Angebote auch im deutschsprachigen Raum, etwa mit Spiegel, zu produzieren.]]></wl:sentence>
  <wl:sentence wl:dependency="4:mark 4:advmod 4:advmod 4:advmod 7:advcl 4:p 7:advmod -1:ROOT 9:compmod 7:nsubj 11:p 7:dobj 11:adpmod 16:det 15:compmod 16:compmod 12:adpobj 11:p 7:cc 20:compmod 7:conj 7:NMOD 24:det 24:det 33:dobj 32:p 32:adpmod 26:adpobj 30:dobj 30:advmod 31:amod 32:dobj 33:xcomp 7:NMOD 7:NMOD 7:NMOD 37:poss 35:adpobj 35:mwe 7:NMOD" wl:id="fdb542ef34e7c2d91388ca739762b62f" wl:pos="KOUS ADV ADV ADV VAFIN $, PROAV VVFIN NE NE $, NN APPR ART NE NE NE $, KON NE NE $, PRELS ART NN $, APPR PRELS PRF ADV ADJA NN VVINF VVINF $, APPR PPOSAT NN PTKVZ $." wl:sem_orient="0.5184758473652127" wl:significance="318.4871872165339" wl:token="0,4 5,13 14,21 22,26 27,30 30,31 32,38 39,45 46,52 53,58 58,59 60,75 76,79 80,83 84,87 88,92 93,98 98,99 100,103 104,109 110,116 116,117 118,121 122,125 126,137 137,138 139,142 143,146 147,151 152,159 160,171 172,181 182,192 193,199 199,200 201,204 205,210 211,223 224,227 227,228"><![CDATA[Dass manchmal weniger mehr ist, darauf wiesen Gregor Aisch, Grafikredakteur bei der New York Times, und Mirko Lorenz, der den Datawrapper, mit dem sich einfach interaktive Diagramme herstellen lassen, bei ihrer Präsentation hin.]]></wl:sentence>
  <wl:sentence wl:dependency="1:poss 2:adpobj 3:adpmod -1:ROOT 3:dobj 7:det 7:amod 3:nsubj 7:adpmod 11:num 11:amod 8:adpobj 3:acomp 14:p 25:nsubj 14:p 14:p 14:conj 17:p 17:cc 17:conj 14:cc 14:conj 14:cc 14:conj 3:NMOD 25:adpmod 26:adpobj 25:prt 3:NMOD" wl:id="0a126f4c15fbf1eb5b945337af395512" wl:pos="PPOSAT NN APPO VVFIN PRF ART PIDAT NN APPR CARD ADJA NN VVFIN $. NN $[ $, NN $[ KON NN KON NN KON NN VVFIN APPRART NN PTKVZ $." wl:sem_orient="0.34752402342845795" wl:token="0,5 6,13 14,18 19,25 26,30 31,34 35,42 43,54 55,58 59,63 64,73 74,85 86,94 94,95 96,102 102,103 103,104 105,111 111,112 113,116 117,131 132,137 138,146 147,150 151,162 163,171 172,174 175,184 185,188 188,189"><![CDATA[Ihrer Ansicht nach lassen sich die meisten Geschichten mit fünf einfachen Grafiktypen erzählen: Balken-, Linien- und Tortengrafiken sowie Tabellen und Punktwolken reichten im Regelfall aus.]]></wl:sentence>
  <wl:sentence wl:dependency="-1:adpobj 14:adpmod 1:prt 1:p 6:advmod 6:advmod 1:partmod 6:p 6:conj 8:adpmod 9:adpobj 10:cc 10:conj 14:aux 0:NMOD 21:p 21:mark 21:nsubj 21:advmod 21:adpmod 19:adpobj 14:conj 21:aux 14:p" wl:id="f7a5f43c241734b798aeccc3d6b7c115" wl:pos="NE VVFIN PTKVZ $, PWAV ADV ADJD $, NN APPR NN KON NN PTKZU VVINF $, KOUS PDAT ADV APPRART NN VVINF VMFIN $." wl:sem_orient="0.7856742013183862" wl:significance="318.4871872165339" wl:token="0,6 7,12 13,15 15,16 17,21 22,27 28,35 35,36 37,48 49,54 55,76 77,80 81,87 88,90 91,99 99,100 101,105 106,111 112,116 117,120 121,131 132,141 142,149 149,150"><![CDATA[Lorenz regte an, wann immer möglich, Symbolfotos durch Datenvisualisierungen und Charts zu ersetzen, weil diese mehr zur Geschichte beitragen könnten.]]></wl:sentence>
  <wl:sentence wl:dependency="-1:ROOT 0:NMOD 3:p 0:NMOD 5:p 0:NMOD 5:p 9:compmod 9:p 5:appos 5:p" wl:id="1cbf243d9b44558bf5743cb01364ca06" wl:pos="( ITJ $, VVFIN $, VVFIN $, VVPP $, CARD )" wl:token="0,1 1,4 4,5 6,9 9,10 11,14 14,15 16,30 30,31 32,41 41,42"><![CDATA[(afs, fin, pum, derStandard.at, 16.4.2015)]]></wl:sentence>
  <wl:annotation wl:sentence="20" wl:entityType="PersonEntity" wl:end="74" wl:key="http://de.dbpedia.org/resource/Barack_Obama" wl:preferredName="Barack Obama" wl:start="62" wl:surfaceForm="Barack Obama"/>
  <wl:annotation wl:sentence="2" wl:entityType="OrganizationEntity" wl:end="30" wl:key="http://de.dbpedia.org/resource/Facebook_Inc." wl:preferredName="Facebook Inc." wl:start="22" wl:surfaceForm="Facebook"/>
  <wl:annotation wl:sentence="4" wl:entityType="OrganizationEntity" wl:end="76" wl:key="http://de.dbpedia.org/resource/Facebook_Inc." wl:preferredName="Facebook Inc." wl:start="68" wl:surfaceForm="Facebook"/>
  <wl:annotation wl:sentence="14" wl:entityType="OrganizationEntity" wl:end="31" wl:key="http://de.dbpedia.org/resource/Facebook_Inc." wl:preferredName="Facebook Inc." wl:start="23" wl:surfaceForm="Facebook"/>
  <wl:annotation wl:sentence="16" wl:entityType="OrganizationEntity" wl:end="74" wl:key="http://de.dbpedia.org/resource/Facebook_Inc." wl:preferredName="Facebook Inc." wl:start="66" wl:surfaceForm="Facebook"/>
  <wl:annotation wl:sentence="23" wl:entityType="OrganizationEntity" wl:end="8" wl:key="http://de.dbpedia.org/resource/Facebook_Inc." wl:preferredName="Facebook Inc." wl:surfaceForm="Facebook"/>
  <wl:annotation wl:sentence="12" wl:entityType="GeoEntity" wl:end="34" wl:key="http://sws.geonames.org/5391959/" wl:preferredName="San Francisco" wl:start="21" wl:surfaceForm="San Francisco"/>
  <wl:annotation wl:sentence="24" wl:entityType="GeoEntity" wl:end="92" wl:key="http://sws.geonames.org/5391959/" wl:preferredName="San Francisco" wl:start="84" wl:surfaceForm="New York"/>
  <wl:annotation wl:sentence="24" wl:entityType="GeoEntity" wl:end="92" wl:key="http://sws.geonames.org/5128638/" wl:preferredName="New York" wl:start="84" wl:surfaceForm="New York"/>
  <wl:annotation wl:sentence="12" wl:entityType="GeoEntity" wl:end="34" wl:key="http://sws.geonames.org/6252001/" wl:preferredName="USA" wl:start="21" wl:surfaceForm="San Francisco"/>
  <wl:annotation wl:sentence="24" wl:entityType="GeoEntity" wl:end="92" wl:key="http://sws.geonames.org/6252001/" wl:preferredName="USA" wl:start="84" wl:surfaceForm="New York"/>
</wl:page>
'''

    JESAJA_URL = 'http://localhost:63002/rest/'
    PROFILE_NAME = 'default'
    STOPLIST_PROFILE_NAME = 'stoplist'
    CORPUS_NAME = 'test_corpus_neks'
    MATVIEW_NAME = 'unittest'
    SAMPLE_DATA_FILE = get_full_path('xml_documents.pickle.gz')
    SAMPLE_DATA_FILE = get_full_path('xml_documents_dach_at_media.pickle.gz')
    PROFILE = {
        'valid_pos_tags': ['NN', 'NNP', 'NNS'],  # ['NN', 'P', 'ADJ'],
        'required_pos_tags': [],
        'min_phrase_significance': 2.0,
        'num_keywords': 5,
        'keyword_algorithm': 'com.weblyzard.backend.jesaja.algorithm.keywords.YatesKeywordSignificanceAlgorithm',
        'min_token_count': 1,
        'min_ngram_length': 1,
        'max_ngram_length': 3,
        'skip_underrepresented_keywords': False,
        'ground_annotations': True,
        'stoplists': [],
    }

    def setUp(self):
        '''
        Setup Jesaja Keyword Server
        '''
        self.jesaja = JesajaNg(url=self.JESAJA_URL)
        self.service_is_online = self.jesaja.is_online()

        if self.service_is_online:

            STOPLIST_PROFILE = self.PROFILE.copy()
            STOPLIST_PROFILE['stoplists'] = ['testList', 'anotherList']

            with GzipFile(self.SAMPLE_DATA_FILE) as f:
                sample_corpus = load(f)
                print('Loaded corpus with %d entries' % (len(sample_corpus)))

#             for doc in sample_corpus:
#                 print(doc)
            self.jesaja.set_stoplist('testList',
                                     ('the', 'from', 'there', 'here'))
            self.jesaja.set_stoplist('anotherList',
                                     ('you', 'he', 'she', 'it', 'them'))
            self.jesaja.set_keyword_profile(self.PROFILE_NAME, self.PROFILE)
            self.jesaja.set_keyword_profile(
                self.STOPLIST_PROFILE_NAME, STOPLIST_PROFILE)
            self.jesaja.set_matview_profile(
                self.MATVIEW_NAME, self.PROFILE_NAME)

            xml_documents = [self.xml_content]

            # create the reference corpus
            if not self.jesaja.has_corpus(matview_id=self.MATVIEW_NAME):
                while self.jesaja.rotate_shard(matview_id=self.MATVIEW_NAME) == 0:
                    #                     csv_corpus = {'keystone':25, 'energy': 123, 'ana': 12, 'tom': 22, 'petra': 3, 'clima':5, 'Shihab': 12, 'Kirche':10}
                    #                     self.jesaja.add_csv(matview_id=self.MATVIEW_NAME, keyword_count_map=csv_corpus )
                    self.jesaja.add_documents(
                        matview_id=self.MATVIEW_NAME, xml_documents=xml_documents)
        else:
            print('WARNING: Webservice is offline --> not executing all tests!!')

    def test_nek_annotation(self):
        ''' test nek annotations '''
        xml_content = '''<wl:page xmlns:wl="http://www.weblyzard.com/wl/2013#" xmlns:ma="http://www.w3.org/ns/ma-ont#" xmlns:dc="http://purl.org/dc/elements/1.1/" original_request_url="http://derstandard.at/2000014426852/Soziale-Medien-fuer-die-Nachrichtenverbreitung?ref=rss" source_id="11467" dc:format="text/html" dc:title="Journalismus - Social Media für die Nachrichtenverbreitung" xml:lang="de" wl:id="1243661964" wl:jonas_type="http" wl:nilsimsa="7b30d8322a12a94e12618a60fef8cae144aaae914951a1f59d132a90ca35f247">
                            <wl:sentence> Did you hear about Obama? This is a really good story.</wl:sentence>
                            <wl:sentence wl:dependency="1:advmod -1:ROOT 1:advmod 1:advmod 1:adpmod 6:det 4:adpobj 6:adpmod 7:adpobj 10:compmod 8:appos 1:p" wl:id="312ea95b45c50be0c5dd4a215d5adaaf" wl:pos="ADV VVFIN ADV ADV APPR ART NN APPR NN NE NE $." wl:token="0,2 3,12 13,17 18,24 25,28 29,34 35,44 45,48 49,61 62,68 69,74 74,75"><![CDATA[So geschehen auch jüngst bei einem Interview mit US-Präsident Barack Obama.]]></wl:sentence>
                            <wl:annotation wl:sentence="1" wl:entity_type="PersonEntity" wl:end="74" wl:key="http://de.dbpedia.org/resource/Barack_Obama" wl:md5sum="312ea95b45c50be0c5dd4a215d5adaaf" wl:preferredName="Barack Obama" wl:start="62" wl:surfaceForm="Barack Obama"/>
                         </wl:page>'''
        if self.service_is_online:
            result = self.jesaja.get_keyword_annotations(self.MATVIEW_NAME,
                                                         [xml_content])
            assert len(result)
#            from pprint import pprint
#            pprint(result)
            assert '1243661964' in result
            assert len(result['1243661964']) == 1
            assert result['1243661964'][0]['key'] == 'http://de.dbpedia.org/resource/Barack_Obama'


if __name__ == '__main__':
    unittest.main()
