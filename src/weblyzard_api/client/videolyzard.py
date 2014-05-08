#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 16.04.2014

@author: heinz-peterlang
'''

'''
required tasks - see the API documentation
* add new youtube urls to videoLyzard's analyzing queue
    * support for adding a single video and multiple videos 
* get analyzed videos (annotations, new xml) since timestamp x
    * support for iterating the pages, see variable pager in response
    * https://ccc.modul.ac.at/videolyzard/get-data?type=json&page=1&portal=portal_climate_new&since=1391172002&filter=completed

username: weblyzard 
password: VID30lyz4rd

non-targets: 
* update the database -> just return the result
* get the youtube urls -> just use anything from youtube

.. seealso:: 

    `API Documentation <https://gitlab.semanticlab.net/matthiasb/weblyzard-youtube-tab/wikis/api-documentation>`_

    :mod::`wl_data_scripts.projects.videolyzard.import_data`
'''
import csv
import unittest
import json
import requests
import time
from datetime import datetime, timedelta


class VideolyzardClient(object):

    UPLOAD_URL = 'https://ccc.modul.ac.at/videolyzard/add-json?username=%(username)s&password=%(password)s'
    VIDEO_DATA_URL = 'https://ccc.modul.ac.at/videolyzard/get-data?username=%(username)s&password=%(password)s&type=json'

    POSSIBLE_FILTER_CONFIGS = ('processing', 'failed', 'completed')
    FILTER_PROCESSING = 'processing'
    FILTER_FAILED = 'failed'
    FILTER_COMPLETED = 'completed'

    @classmethod
    def convert_datetime_to_timestamp(cls, datetime_obj):
        '''
        Generate a total timestamp used by the Videolyzard API.

        :param datetime_obj: A datetime object from the standard library
        :returns: an integer timestamp e.g. 1396310400
        '''
        converted_time = time.mktime(datetime_obj.timetuple()) + datetime_obj.microsecond / 1E6
        return int(converted_time)


    @classmethod
    def convert_videos_csv_to_dict(cls, file_obj):
        '''
        Convert a video CSV file to a dict.
        :param file_obj: A file object.
        :returns: A dictionary with the fields portal_name, original_url, title and text.
        '''
        reader = csv.reader(file_obj)
        titles = reader.next()

        portal_idx = titles.index('portal_name') if 'portal_name' in titles else None
        url_idx = titles.index('original_url') if 'original_url' in titles else None
        title_idx = titles.index('title') if 'title' in titles else None
        text_idx = titles.index('text') if 'text' in titles else None

        assert portal_idx is not None, 'Could not find title "portal_name" in CSV file!'
        assert url_idx is not None, 'Could not find title "portal_name" in CSV file!'

        videos = []

        for video_line in reader:

            video = {'portal_name': video_line[portal_idx],
                     'original_url': video_line[url_idx],
                     'title':video_line[title_idx] if title_idx else '',
                     'text': video_line[text_idx] if text_idx else '',}

            videos.append(video)

        return videos

    def __init__(self, username, password):
        '''
        The Videolyzard client requires a password and a username.
        '''
        assert username, 'No username was provided!'
        assert password, 'No password was provided!'

        self.username = username
        self.password = password


    def post_dict_videos_to_queue(self, videos):
        '''
        Post a list of video dictionaries to the Videolyzard queue.

        :param list videos: A list of video dictionaries.
                            Each dictionary should contain the fields

                            * 'portal_name'
                            * 'original_url'
                            * 'description'
                            * 'text': the title of the video

        :returns: A response object
        '''
        assert isinstance(videos, list)
        assert all('portal_name' in video for video in videos)
        assert all('original_url' in video for video in videos)

        response = self._send_to_queue(videos)
        return response


    def post_csv_to_queue(self, csv_file_object):
        '''
        Accepts a CSV file object and posts the lines to
        the Videolyzard queue.

        The following column headers are accepted:

            * portal_name
            * original_url
            * description
            * text: the title of the video

        '''
        videos = self.convert_videos_csv_to_dict(csv_file_object)
        return self.post_dict_videos_to_queue(videos)


    def _prepare_url_with_user_credentials(self, url):
        user = {'username':self.username, 'password':self.password,}
        return url % user


    def _send_to_queue(self, videos):

        headers = {'Content-type':'application/x-www-form-urlencoded',}
        url = self._prepare_url_with_user_credentials(self.UPLOAD_URL)

        payload = {'json':json.dumps(videos)}
        response = requests.post(url, data=payload, headers=headers)
        return response


    def get_video_data(self, portal, since=None, page=1, filter=None):
        '''
        Query video data from the Videolyzard API.

        :param portal: Reduces results to WebLyzard portal (e.g. portal_climate_new);
                       shows all if not specified
        :param filter: Filters results by their state (processing, failed, completed); shows all if not specified
        :param since: Shows results only from the specified timestamp (e.g. 1396310400); shows all if not specified
        :param page: Current selected page (e.g. 5); shows page 1 if not specified
        '''
        assert isinstance(page, int), page

        portal_str = '&portal=%s' % portal
        parameters = [portal_str,]

        # prepare the request URL
        if since:
            converted_timeobj = self.convert_datetime_to_timestamp(since)
            since_str = '&since=%s' % converted_timeobj
            parameters.append(since_str)

        if filter:
            error_msg = '%s is not a valid filter configuration!' % filter
            assert filter in self.POSSIBLE_FILTER_CONFIGS, error_msg
            filter_str = '&filter=%s' % filter
            parameters.append(filter_str)

        url = self._prepare_url_with_user_credentials(self.VIDEO_DATA_URL)
        url = url + ''.join(parameters)

        further_videos_exist = 200

        # query video data from API.
        while further_videos_exist:

            request_url = url + '&page=%s' % page
            response = requests.get(request_url)

            no_more_video_data = response.status_code != 200
            if no_more_video_data:
                break

            try:
                response_dict = json.loads(response._content)
                videos = response_dict['videos']

                for video in videos:
                    yield video

            except ValueError:
                pass

            page = page + 1
            further_videos_exist = response.status_code == 200

        return



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

        client = VideolyzardClient(username='weblyzard', password='VID30lyz4rd')
        response = client.post_dict_videos_to_queue(videos)

        self.assertEquals(response.status_code, 200)
        self.assertTrue('success' in response.content)


    def test_import_from_csv(self):

        csv_file_obj = open('videolyzard.csv')
        client = VideolyzardClient(username='weblyzard', password='VID30lyz4rd')
        response = client.post_csv_to_queue(csv_file_obj)

        self.assertTrue('success' in response.content)
        self.assertEquals(response.status_code, 200)


    def test_retrieve_videos(self):

        client = VideolyzardClient(username='weblyzard', password='VID30lyz4rd')
        since = datetime.now() - timedelta(days=90)
        videos_query = client.get_video_data('portal_climate_new', filter='completed', since=since)

        num_checked_videos = 0
        for video in videos_query:

            self.assertTrue('output' in video)
            self.assertTrue('state' in video)
            self.assertTrue('portal_url' in video)
            self.assertTrue('video_url' in video)

            num_checked_videos = num_checked_videos + 1

            if num_checked_videos > 10:
                break


if __name__ == '__main__':
    unittest.main()
