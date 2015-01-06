Annie-based Annotation Format
=============================

The webLyzard/WISDOM annotation format is based on the data structures used by the `GATE <http://www.gate.ac.uk/>`_ project. A detailed description of these data structures can be found in the `Gate Documentation on Language Resources: Corpora, Documents and Annotations <http://gate.ac.uk/sale/tao/splitch5.html>`_.

Classes
-------
* Annotation Set(type:String) - an Annotation Set contains "n" Annotations
* Annotation(start:int, end:int, type:String, feature=Map<String, String>)




Sentence-level annotations
--------------------------

Running example:
::

	Andreas Wieland, CEO, Hamilton Bonaduz AG said: «We are very excited ...
	012345678901234567890123456789012345678901234567890123456789012345678901
	0.........1.........2.........3.........4.........5.........6.........7.

*** Definition of the used JSON Fields ***
* sentence: the sentence's MD5 sum
* start: the annotation's start position within the sentence
* end: the annotation's end position within the sentence
* type: the annotation type
* features: a dictionary of annotation features

Geonames
........
::

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

People
......
::

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


Organizations
.............
::

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


Part-of-speech Tags
...................

Please refer to `used part-of-speech (POS) tags <weblyzard_api.data_format.pos-tags.html>`_ for a list of the POS-Tags used within webLyzard.
::

	Anna is a student.
	012345678901234567
	0.........1.......


::

	[
	  {sentence="fbb1a44c0d422e496d87c3c8d23b4480", start=0, end=3,  type="Token", features={ 'POS': 'NN' } }
	  {sentence="fbb1a44c0d422e496d87c3c8d23b4480", start=5, end=6,  type="Token", features={ 'POS': 'VRB' } }
	  {sentence="fbb1a44c0d422e496d87c3c8d23b4480", start=8, end=8,  type="Token", features={ 'POS': 'ART' } }
	  ...
	]
