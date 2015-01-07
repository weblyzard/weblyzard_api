Recognyze Annotation Service
============================

Welcome
-------

This is the public access point to the demo of the `Recognyze Annotation Service <https://www.weblyzard.com/recognyze/>`_. Given a text input, the Recognyze service returns a set of `Named Entities <http://en.wikipedia.org/wiki/Named-entity_recognition>`_ together with their start and end positions within the input text. Under the hood, Recognyze makes use of open data portals such as `DBpedia <http://dbpedia.org/About>`_ and `Geonames <http://www.geonames.org/>`_ for its queries, returning predefined subsets (property-wise) of respective entities.

**Service usage is limited to 100 requests per day (max. 1MB data transfer per request)**

Search Profiles
---------------

When querying Recognyze, you must provide a search profile to search within. A search profile describes a domain from the real world, and currently there exist the following set of domains:

{en,de}.organization.ng
	Organizations in english and german, taken from DBpedia. Returns type OrganizationEntity
	
{en,de}.people.ng
	Person Names in english and german, taken from DBpedia. Returns type PersonEntity
	
{en,de,fr}.geo.50000.ng
	Geolocations (cities, countries) with a population larger than 50000, taken from GeoNames. Returns type GeoEntity
	
Passing multiple profiles at once is also supported by the API.

REST API
--------

The REST interface can easily be accessed via our open source `weblyzard API <https://github.com/weblyzard/weblyzard_api>`_ as shown below.
::

	from weblyzard_api.client.recognize import Recognize
	from pprint import pprint
	 
	url = 'http://triple-store.ai.wu.ac.at/recognize/rest/recognize'
	profile_names=['en.organization.ng', 'en.people.ng', 'en.geo.500000.ng']
	text = 'Microsoft is an American multinational corporation headquartered in Redmond, Washington, that develops, manufactures, licenses, supports and sells computer software, consumer electronics and personal computers and services. It was was founded by Bill Gates and Paul Allen on April 4, 1975.'
	client = Recognize(url)
	result = client.search_text(profile_names,
					text,
					output_format='compact',
								max_entities=40,
								buckets=40,
								limit=40)  
	pprint(result)

Results
-------

Recognyze returns a JSON list object of all found entities. For each found entity, the service returns the entity type, the associated search profile (see above), the entity's occurences within the given text (start, end, sentence, surface form), the confidence of the found entity to be correct, the public key where the entity links to (e.g. http://sws.geonames.org/4990729), as well as extra properties where available.
::

	[{u'confidence': 6385.540194875138,
	u'entities': [{u'end': 22,
					u'sentence': 0,
					u'start': 1,
					u'surfaceForm': u'Microsoft Corporation'}],
	u'entityType': u'OrganizationEntity',
	u'key': u'http://dbpedia.org/resource/Microsoft_Corporation',
	u'preferredName': u'Microsoft Corporation',
	u'profileName': u'en.organization.ng',
	u'properties': {},
	u'score': 6385.54},
	{u'confidence': 4.0,
	u'entities': [{u'end': 100,
					u'sentence': 0,
					u'start': 90,
					u'surfaceForm': u'Washington'}],
	u'entityType': u'GeoEntity',
	u'key': u'http://sws.geonames.org/4140963/',
	u'preferredName': u'Washington D.C.',
	u'profileName': u'en.geo.500000.ng',
	u'properties': {u'adminLevel': u'http://www.geonames.org/ontology#P.PPLC',
					u'latitude': u'38.89511',
					u'longitude': u'-77.03637',
					u'parent': u'http://sws.geonames.org/4138106/',
					u'parentCountry': u'http://sws.geonames.org/6252001/',
					u'population': u'601723'},
	u'score': 3.15},
	{u'confidence': 1808.274919947148,
	u'entities': [{u'end': 269,
					u'sentence': 0,
					u'start': 259,
					u'surfaceForm': u'Bill Gates'}],
	u'entityType': u'PersonEntity',
	u'key': u'http://dbpedia.org/resource/Bill_Gates',
	u'preferredName': u'Bill Gates',
	u'profileName': u'en.people.ng',
	u'properties': {u'birthDate': u'1955-10-28',
					u'givenName': u'Bill',
					u's': u'http://dbpedia.org/resource/Bill_Gates',
					u'surname': u'Gates',
					u'thumbnail': u'http://upload.wikimedia.org/wikipedia/commons/4/4a/BillGates2012.jpg'},
	u'score': 1808.27},
	{u'confidence': 1808.274919947148,
	u'entities': [{u'end': 284,
					u'sentence': 0,
					u'start': 274,
					u'surfaceForm': u'Paul Allen'}],
	u'entityType': u'PersonEntity',
	u'key': u'http://dbpedia.org/resource/Paul_Allen',
	u'preferredName': u'Paul Allen',
	u'profileName': u'en.people.ng',
	u'properties': {u'birthDate': u'1953-01-21',
					u'givenName': u'Paul',
					u's': u'http://dbpedia.org/resource/Paul_Allen',
					u'surname': u'Allen',
					u'thumbnail': u'http://upload.wikimedia.org/wikipedia/commons/5/51/Paull_Allen_fix_1.JPG'},
	u'score': 1808.27}]