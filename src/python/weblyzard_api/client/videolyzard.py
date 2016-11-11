#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 16.04.2014
.. seealso::

    `API Documentation <https://gitlab.semanticlab.net/matthiasb/weblyzard-youtube-tab/wikis/api-documentation>`_

    :mod::`wl_data_scripts.projects.videolyzard.import_data`
@author: heinz-peterlang
'''

import csv
import json
import requests
import time
import urllib

class VideolyzardClient(object):
    '''
    A Python client for the Weblyzard API.

    .. seealso::

    `API Documentation <https://gitlab.semanticlab.net/matthiasb/weblyzard-youtube-tab/wikis/api-documentation>`_

    :mod::`wl_data_scripts.projects.videolyzard.import_data`
    '''
    SERVER_URL = 'http://ccc.modul.ac.at/videolyzard'
    UPLOAD_URL = '%(server_url)s/add-json?username=%(username)s&password=%(password)s'
    VIDEO_DATA_URL = '%(server_url)s/get-data?username=%(username)s&password=%(password)s&type=json&'

    POSSIBLE_FILTER_CONFIGS = ('processing', 'failed', 'completed')
    FILTER_PROCESSING = 'processing'
    FILTER_FAILED = 'failed'
    FILTER_COMPLETED = 'completed'

    def __init__(self, username, password, server_url=None):
        '''
        The Videolyzard client requires a password and a username.
        '''
        assert username, 'No username was provided!'
        assert password, 'No password was provided!'

        self.username = username
        self.password = password
        self.server_url = server_url if server_url else self.SERVER_URL

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
        return url % {'server_url' : self.server_url,
                      'username' : self.username,
                      'password' : self.password}


    def _send_to_queue(self, videos):

        headers = {'Content-type':'application/x-www-form-urlencoded',}
        url = self._prepare_url_with_user_credentials(self.UPLOAD_URL)

        payload = {'json':json.dumps(videos)}
        response = requests.post(url, data=payload, headers=headers)
        return response


    def get_video_data(self, portal, since=None, page=1, status=None):
        '''
        Query video data from the Videolyzard API.

        .. note :: The returned video_urls are modified!
                   '&videolyzard=annotated' is appended in order to
                   indicated that the video_url was processed. For example:
                   www.youtube.com/watch?v=m10pGZx1s0s => www.youtube.com/watch?v=m10pGZx1s0s&videolyzard=annotated

        :param portal: Reduces results to WebLyzard portal (e.g. portal_climate_new);
                       shows all if not specified
        :param status: Filters results by their state (processing, failed, completed); shows all if not specified
        :param since: Shows results only from the specified timestamp (e.g. 1396310400); shows all if not specified
        :param page: Current selected page (e.g. 5); shows page 1 if not specified
        '''
        assert isinstance(page, int), page
        parameters = {'portal' : portal}

        # prepare the request URL
        if since:
            converted_timeobj = self.convert_datetime_to_timestamp(since)
            parameters['since'] = converted_timeobj

        if status:
            error_msg = '%s is not a valid status configuration!' % status
            assert status in self.POSSIBLE_FILTER_CONFIGS, error_msg
            parameters['filter'] = status

        url = self._prepare_url_with_user_credentials(self.VIDEO_DATA_URL)
        parameters_str = urllib.urlencode(parameters)
        url = url + parameters_str
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

                    output_url = video.get('output')
                    no_transcript_was_found = not output_url

                    if no_transcript_was_found:
                        continue

                    output_response = requests.get(output_url)
                    output = output_response.json()

                    video['xml'] = output.get('xml')
                    video['annotations'] = output.get('annotations')

                    yield video

            except ValueError:
                pass

            page = page + 1
            further_videos_exist = response.status_code == 200

        return