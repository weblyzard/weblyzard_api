#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 16.04.2014
.. seealso::

    `API Documentation <https://gitlab.semanticlab.net/matthiasb/weblyzard-youtube-tab/wikis/api-documentation>`_

    :mod::`wl_data_scripts.projects.videolyzard.import_data`
@author: heinz-peterlang
'''
import unittest

from datetime import datetime, timedelta
from weblyzard_api.client.videolyzard import VideolyzardClient


class TestVideolyzard(unittest.TestCase):

    def test_submit_video(self):
        videos = [{'portal_name': 'portal_climate_new',
                   'original_url': 'https://www.youtube.com/watch?v=gB37g7al-F4',
                   'title': 'test1',
                   'text': 'test1 description'},

                  {'portal_name': 'portal_climate_new',
                   'original_url': 'https://www.youtube.com/watch?v=FQjZVdaTZOs',
                   'title': 'test2',
                   'text': 'test2 description'}, ]

        client = VideolyzardClient(
            username='weblyzard', password='VID30lyz4rd')
        response = client.post_dict_videos_to_queue(videos)

        self.assertEquals(response.status_code, 200)
        self.assertTrue('success' in response.content)

    def test_retrieve_videos(self):

        client = VideolyzardClient(
            username='weblyzard', password='VID30lyz4rd')
        since = datetime.now() - timedelta(days=90)
        videos_query = client.get_video_data('portal_climate_new',
                                             status='completed',
                                             since=since)

        num_checked_videos = 0
        for video in videos_query:

            self.assertTrue('output' in video)
            self.assertTrue('state' in video)
            self.assertTrue('portal_url' in video)
            self.assertTrue('video_url' in video)

            self.assertEquals(video['state'], 'completed')

            num_checked_videos = num_checked_videos + 1

            # without this additional break up condition
            # the test would run for ages!
            if num_checked_videos > 10:
                break


if __name__ == '__main__':
    unittest.main()
