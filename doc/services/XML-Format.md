{:toc}

webLyzard XML and Annotation Format
=============================

Example webLyzard XML file:

```xml
<wl:page xmlns="http://www.weblyzard.com/wl/2013#" 
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 wl:id="332982121" 
 dc:format="text/html"
 dc:coverage="http://de.dbpedia.org/page/Helmut_Sch%C3%BCller 
              http://de.dbpedia.org/page/Gerda_Schaffelhofer 
              http://de.dbpedia.org/page/Styria_Media_Group"
 dc:creator="http://www.nachrichten.at/KA"
 dc:related="http://www.kurier.at/article/Die-Kirche.html http://www.diepresse.com/kirche/Katholische_Aktion_Österreich"
 xml:lang="de" 
 wl:nilsimsa="77799a10d691a16416300ae1fad0bbe24c3f0991c17533649db7cbe1e23d5241">
 
<!-- The title -->
   <wl:sentence wl:id="61e8b085944f173e36637e8daf7d77c0" 
     wl:token = "0:3 4:12 13:19 20:22 23:26 27:46 ...."
     wl:pos = "ADJA NN $. NN VVFIN NN XY" 
     wl:dependency = "1 2 -1 4 5 2 2"
     wl:is_title = "True"
     wl:sem_orient="0.764719112902" 
     wl:significance="None">
     <![CDATA[Katholische Aktion: Präsidentin rügt Pfarrer-Initiative | Nachrichten.at.]]>

<!-- The content (wl:is_title = "False" or not set) -->
   <wl:sentence wl:id="61e8b085944f173e36637e8daf7d77c0" 
     wl:pos ="APPR ADJA NN APPR ART NN APPR NE NE VVFIN APPRART NN ART ADJA NN ART ADJA NN NE ( NE ) $, NE NE $."
     wl:dependency="1 -1 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 1 1 1 1 1"
     wl:token = "0,3 4,12 13,19 20,22 23,26 27,45 46,48 49,55 56,64 65,76 77,79 80,88 89,92 93,97 98,109 110,113 114,126 127,133 134,144 145,146 146,148 148,149 149,150 151,156 157,170 170,171"
     wl:sem_orient="0.764719112902" 
     wl:significance="None">
        <![CDATA[Mit scharfer Kritik an der Pfarrer-Initiative um Helmut Schüller überraschte am Dienstag die neue Präsidentin der Katholischen Aktion Österreich (KA), Gerda Schaffelhofer.]]>
   </wl:sentence>
   <wl:sentence wl:id="a3cba1f907f41160e690ad072dd2fc08" wl:pos="NN ADJD APPR ART NN PPOSAT NN APPR ART NN NN PRF ART NN ART ADJA ADJA NN APPR ART ADJA NN NN ART NN APPR PPER NN APPR ART NN PIS VMFIN PTKNEG APPR NN ADJA NN VVFIN NN VVFIN NN ART NN APPRART NN NN NN" wl:sem_orient="-0.901669634667" wl:significance="None"><![CDATA[Werbung Knapp nach der Bestätigung ihrer Wahl durch die Bischöfe „wehrt“ sich die Präsidentin der offiziellen katholischen Laienvertretung in einem offenen Brief „gegen die Vereinnahmung von uns Laien durch die Pfarrer-Initiative“. Man wolle nicht von „irgendwelchen kirchlichen Kreisen“ instrumentalisiert werden, schreibt Schaffelhofer, die Managerin im kirchennahen Styria-Konzern ist.]]></wl:sentence>
   <wl:sentence wl:id="3f49d4fe7e9fc31b74a8748e21002e23" wl:pos="NN NN KOUS ART NN PPOSAT NN APPR ART NN VVFIN KON PPER APPR NN NN" wl:sem_orient="0.0" wl:significance="None"><![CDATA[Hintergrund ist, dass die Pfarrer-Initiative ihr Augenmerk auf die Laien richtet und sie als „Kirchenbürger“ bezeichnet.]]></wl:sentence>
</wl:page>
```

#### Dependency trees:

* `wl:dependency` describes the sentences' dependency structure. The number refers to the current token's parent in the dependency tree.
* Special values:
  * `-1`: root node
  * `-2`: no parent could be determined
* Example: 
  * Text: "Ana loves Tom.", wl:dependency: "1 -1 1" 
  * Tree: "Anna -> loves <- Tom"

#### Changelog

- use http://www.weblyzard.com/wl/2013# as default namespace
- include the dublin core namespace
    - use dc:title rather than title
    - use dc:format rather than `content_type`
    - Support the following constructs:
        -   use dc:creator to refer to authors
        -   use dc:coverage to refer to companies, organizations and locations covered in the article
        -   multiple entries are separated by spaces
    - Field names for document objects
       - content_id -> wl:id
       - content_type -> dc:format
- 22 August 2014: add `wl:dependency` for dependency tries.
- Python related changes
    - Document object ```{'content_id': 12, 'content_type': 'text/html' ... } -> {'id': 12, 'format': 'text/html', ...}```
    - Justification
      - wl:id is required, i.e. the use of a proper namespace; the use of xml:id is not possible, because the XML Schema specification requires its values to be from type NCName (which does not allows values to start with a number!).
       - dc:format is a standardized identifier for the content type



## Annie-based Annotation Format

The webLyzard/WISDOM annotation format is based on the data structures used by the [GATE](http://www.gate.ac.uk/) project. A detailed description of these data structures can be found in the [Gate Documentation on Language Resources: Corpora, Documents and Annotations](http://gate.ac.uk/sale/tao/splitch5.html).

### Classes
* Annotation Set(type:String) - an Annotation Set contains "n" Annotations
* Annotation(start:int, end:int, type:String, feature=Map<String, String>)




### Sentence-level annotations

Running example:

```
Andreas Wieland, CEO, Hamilton Bonaduz AG said: «We are very excited ...
012345678901234567890123456789012345678901234567890123456789012345678901
0.........1.........2.........3.........4.........5.........6.........7.
```

*** Definition of the used JSON Fields ***
* sentence: the sentence's MD5 sum
* start: the annotation's start position within the sentence
* end: the annotation's end position within the sentence
* type: the annotation type
* features: a dictionary of annotation features

#### Geonames



```json
[{
    "start":31,
    "end":38,
    "sentence": "777081b7ebe4a99b598ac2384483b4ab",
    "type":"ch.htwchur.wisdom.entityLyzard.GeoEntity",
    "features":{
        "entities":[{
            "confidence":7.0,
            "url":"http://sws.geonames.org/2661453/",
            "preferredName":"Bonaduz"
        },{
            "confidence":6.0,
            "url":"http://sws.geonames.org/7285286/",
            "preferredName":"Bonaduz"
        }],
        "profile":"Cities.CH.de"
    }
}]
```

#### People
```json
[{
    "start":0,
    "end":15,
    "sentence": "777081b7ebe4a99b598ac2384483b4ab",
    "type":"ch.htwchur.wisdom.entityLyzard.PersonEntity",
    "features":{
        "entities":[{
            "confidence":1646.4685797722482,
            "url":"http://www.semanticlab.net/proj/wisdom/ofwi/person/Andreas_Wieland_(014204)",
            "preferredName":"Andreas Wieland"
        },{
            "confidence":2214.9741075564775,
            "url":"http://www.semanticlab.net/proj/wisdom/ofwi/person/Andreas_Wieland_(059264)",
            "preferredName":"Andreas Wieland"
        },{
            "confidence":1646.4685797722482,
            "url":"http://www.semanticlab.net/proj/wisdom/ofwi/person/Andreas_Wieland_(047517)",
            "preferredName":"Andreas Wieland"
        },{
            "confidence":1646.4685797722482,
            "url":"http://www.semanticlab.net/proj/wisdom/ofwi/person/Andreas_Wieland_(050939)",
            "preferredName":"Andreas Wieland"
        },{
            "confidence":2165.3683447585117,
            "url":"http://www.semanticlab.net/proj/wisdom/ofwi/person/Andreas_Wieland_(049748)",
            "preferredName":"Andreas Wieland"
        }],
        "profile":"ofwi.people"
    }
}]
```


#### Organizations
```json
[{
    "start":22,
    "end":41,
    "sentence": "777081b7ebe4a99b598ac2384483b4ab",
    "type":"ch.htwchur.wisdom.entityLyzard.OrganizationEntity",
    "features":{
        "entities":[{
            "confidence":438.9253911579335,
            "url":"http://www.semanticlab.net/proj/wisdom/ofwi/teledata/company/7246",
            "preferredName":"Hamilton Bonaduz AG"
        }],
        "profile":"ofwi.organizations"
    }
}]
```

#### Part-of-speech Tags

Please refer to [used part-of-speech (POS) tags](POS-Tags.md) for a list of the POS-Tags used within webLyzard.


```
Anna is a student.
012345678901234567
0.........1.......
```

```json
[
  {sentence="fbb1a44c0d422e496d87c3c8d23b4480", start=0, end=3,  type="Token", features={ 'POS': 'NN' } }
  {sentence="fbb1a44c0d422e496d87c3c8d23b4480", start=5, end=6,  type="Token", features={ 'POS': 'VRB' } }
  {sentence="fbb1a44c0d422e496d87c3c8d23b4480", start=8, end=8,  type="Token", features={ 'POS': 'ART' } }
  ...
 ]
```



### Document level annotations

Please add your examples here.
