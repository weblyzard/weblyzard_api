#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
.. codeauthor:: Max Goebel <goebel@weblyzard.com>
"""
from __future__ import print_function
from __future__ import unicode_literals

import os
import unittest

from weblyzard_api.client.jairo import JairoClient


class JairoTest(unittest.TestCase):
    SERVICE_URL = "localhost:63005/rest"

    PROFILES = {

    }

    def setUp(self):
        service_url = os.getenv("JAIRO_SERVICE_URL", self.SERVICE_URL)
        self.client = JairoClient(url=self.SERVICE_URL)
        self.set_profiles()

    def test_service(self):
        """ test status of the Jairo service. """
        print(self.client.status())
        assert "processedDocuments" in self.client.status()

    def set_profiles(self):
        """ test setting a profile on the Jairo service. """
        for profile_name, profile in list(self.PROFILES.items()):
            self.client.set_profile(
                profile_name=profile_name, profile=profile)

            assert profile_name in self.client.list_profiles()

    def test_entity_extension_bad_result_token(self):
        """ test entity extension of the Jairo service. """
        #         profile_name = "dbpedia_person_en"
        #         input_annotations = [
        #             {
        #                 "start": 0, "end": 3,
        #                 "key": "<http://dbpedia.org/resource/Sophie_Scholl>"
        #             },
        #             #             {
        #             #                 "start": 7, "end": 13,
        #             #                 "key": "<http://dbpedia.org/resource/Switzerland>"
        #             #             }
        #         ]
        #         profile_name = "geonames.seeAlso.wikidata"
        #         input_annotations = [{"key": u"2963597"}]
        #         result = self.client.enrich_annotations(profile_name=profile_name,
        #                                                 annotations=input_annotations)
        from pprint import pprint
        #         pprint(result)

        profile_name = "wikidata_label"
        input_annotations = [{"key": u"<http://www.wikidata.org/entity/Q40>"},
                             {"key": u"<http://www.wikidata.org/entity/Q214>"}]
        result = self.client.enrich_annotations(profile_name=profile_name,
                                                annotations=input_annotations)
        pprint(result)
        assert len(result)


if __name__ == "__main__":
    unittest.main()
