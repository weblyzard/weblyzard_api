### Overview

The result of a call to recognize with multiple profiles (e.g. geoname, organizations, ...) returns a dictionary with keys being the respective entity names (GeoEntity, OrganizationEntity, PersonEntity).

Recognize supports three different output formats:
* Standard, returns one annotated result per found instance. Also returns all respective bindings specified in the profile.
* Annie, returns one annotated result per found instance. Returns all candidate groundings found in the GATE Annie format.
* Compact, returns one annotated result per found entity. Multiple matches of the same entity are returned as a single annotation with the individual spans saved as entities. The compact format is optimized for the Weblyzard use case.

**Notice: Only the Annie and the Compact formats support sentence level annotation.**

### Annie 
```
dict: {
    u'GeoEntity': [
        {
            u'confidence': 0.0,
            u'end': 0,
            u'features': {
                u'profile': u'en.geo.500000',
                u'entities': [
                    {
                        u'url': u'http://sws.geonames.org/5551752/',
                        u'confidence': 0.0,
                        u'preferredName': u'Arizona'}
                ]
            },
            u'grounded': False,
            u'sentence': 0,
            u'scoreName': u'GEO FOCUS x OCCURENCE',
            u'entityType': u'GeoEntity',
            u'start': 0,
            u'score': 2.57,
            u'profileName': u'en.geo.500000',
            u'preferredName': u'Arizona'
        },
        {
            ...
        }
    ]
}
```

### Compact 
```
{
    u'GeoEntity': [
        {
             u'confidence': 9.0,
             u'entities': [
                 {
                       u'end': 7,
                       u'sentence': 15,
                       u'start': 0,
                       u'surfaceForm': u'Detroit'
                 },
                {
                       u'end': 10,
                       u'sentence': 16,
                       u'start': 3,
                       u'surfaceForm': u'Detroit'
                 },
             ],
             u'entityType': u'GeoEntity',
             u'key': u'http://sws.geonames.org/4990729/',
             u'preferredName': u'Detroit',
             u'profileName': u'en.geo.500000',
             u'properties': {
                  u'adminLevel': u'http://www.geonames.org/ontology#P.PPLA2',
                  u'latitude': u'42.33143',
                  u'longitude': u'-83.04575',
                  u'parent': u'http://sws.geonames.org/5014227/',
                  u'parentCountry': u'http://sws.geonames.org/6252001/',
                  u'population': u'713777'
             },
             u'score': 18.88
       },
       {
            ...
       }
    ],
 u'OrganizationEntity': [
        {
                          u'confidence': 1277.1080389750275,
                          u'entities': [{u'end': 101,
                                         u'sentence': 12,
                                         u'start': 87,
                                         u'surfaceForm': u'Public Service'}],
                          u'entityType': u'OrganizationEntity',
                          u'key': u'http://dbpedia.org/resource/Public_Service_Enterprise_Group',
                          u'preferredName': u'Public Service Enterprise',
                          u'profileName': u'en.organization.ng',
                          u'properties': {},
                          u'score': 1277.11}]
}
```