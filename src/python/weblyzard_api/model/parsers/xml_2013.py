#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 07.04.2014

@author: heinz-peterlang
'''
from __future__ import unicode_literals
from weblyzard_api.model.parsers import XMLParser
from weblyzard_api.client.rdf import Namespace


class XML2013(XMLParser):

    VERSION = 2013

    SUPPORTED_NAMESPACE = 'http://www.weblyzard.com/wl/2013#'

    DOCUMENT_NAMESPACES = {ns.name.lower(): ns.value for ns in Namespace}

    ATTR_MAPPING = {
        'lang': ('lang', 'xml'),  # legacy
        'language': ('language', 'dc'),
        'content_type': ('format', 'dc'),
        'publication_date': ('issued', 'dc'),
        'published': ('issued', 'dc'),
        'published_date': ('issued', 'dc'),
        'last_modified': ('modified', 'dc'),
        'url': ('identifier', 'dc'),
        'uri': ('identifier', 'dc'),
        'license': ('license', 'dc'),
        'creator': ('creator', 'dc'),
        'author': ('creator', 'dc'),
        'publisher': ('publisher', 'dc'),
        'keywords': ('subject', 'dc'),
        'articleSection': ('articleSection', 'schema'),
        'tags': ('subject', 'dc'),  # twitter
        'title': ('title', 'dc'),
        'content': ('description', 'dc'),
        'description': ('description', 'dc'),

        # internal
        'nilsimsa': ('nilsimsa', 'wl'),
        'content_id': ('id', 'wl'),
        'jonas_type': ('jonas_type', 'wl'),
        'url_label': ('url_label', 'wl'),
        'reach': ('reach', 'wl'),
        'link_text': ('link_text', 'wl'),
        'tweet_id': ('tweet_id', 'wl'),

        'fbType': ('post_type', 'wl'),  # FB
        'thumbnail': ('thumbnail', 'wl'),
        'picture': ('thumbnail', 'wl'),  # FB, YT
        'org_picture': ('thumbnail', 'wl'),  # FB
        'group_picture': ('thumbnail', 'wl'),  # FB
        'location': ('location', 'wl'),  # YT, vimeo/daily
        'duration': ('duration', 'wl'),
        'is_sensitive': ('is_sensitive', 'wl'),  # YT

        # For events, broadcasts, etc.
        'temporal_start': ('temporalStart', 'wl'),
        'temporal_end': ('temporalEnd', 'wl'),

        # DOCUMENT RELATIONS (CID<->CID only) #################################
        # reference to other document (outgoing link)
        'references': ('references', 'dc'),
        'relation': ('relation', 'dc'),

        # reference to similar document (re-tweet)
        'source': ('source', 'dc'),
        # reference to top-level parent (thread ancestor)
        'has_container': ('has_container', 'sioc'),
        # reference to direct parent (nested thread parent)
        'reply_of': ('reply_of', 'sioc'),

        # DOCUMENT METRICS ####################################################
        'user_mentions': ('user_mentions', 'wl'),
        'rating': ('rating', 'wl'),
        'rating_average': ('rating', 'wl'),  # YT
        'viewcount': ('num_views', 'wl'),  # vimeo/daily
        'statistics_viewcount': ('num_views', 'wl'),  # youtube
        'comment_count': ('num_replies', 'wl'),
        'reshares': ('num_reshares', 'wl'),  # g+
        'nr_of_retweets': ('num_reshares', 'wl'),  # twitter

        # USER MAPPINGS #######################################################
        'user_verified': ('user_verified', 'wl'),  # TW
        'user_geo_enabled': ('user_geo_enabled', 'wl'),  # TW
        'user_favourites_count': ('user_favourites_count', 'wl'),  # TW
        'user_post_count': ('user_post_count', 'wl'),
        'user_following': ('user_following', 'wl'),
        'user_view_count': ('user_view_count', 'wl'),  # YT
        'num_tweets': ('user_post_count', 'wl'),  # TW
        'user_created': ('user_created', 'wl'),  # TW
        'user_id': ('user_id', 'wl'),  # FB, G+
        'user_url': ('user_id', 'wl'),  # YT, twitter
        'user_name': ('user_name', 'wl'),
        'user_type': ('user_type', 'wl'),
        'current_status': ('user_status', 'wl'),  # twitter
        'screen_name': ('user_screen_name', 'wl'),
        'user_location': ('user_location', 'wl'),  # twitter
        'user_time_zone': ('user_timezone', 'wl'),  # twitter
        'user_thumbnail': ('user_thumbnail', 'wl'),
        'user_img_url': ('user_thumbnail', 'wl'),  # twitter

        # USER METRICS #######################################################
        'likes_count': ('user_rating', 'wl'),  # FB
        'org_likes_count': ('user_rating', 'wl'),  # FB
        'group_likes_count': ('user_rating', 'wl'),  # FB
        'followers': ('user_rating', 'wl'),  # twitter
        'plusoners': ('user_rating', 'wl'),  # G+

        # MULTIMEDIA ##########################################################
        'media_url': ('locator', 'ma'),
        'media_type': ('format', 'ma'),
        'media_recordingLocation': ('createdIn', 'ma'),
        'media_recordingDate': ('creationDate', 'ma'),
        'media_license': ('hasPolicy', 'ma'),

        # BROADCAST ###########################################################
        'media_genre': ('genre', 'ma'),
        'media_brand': ('brand', 'po'),
        'media_season': ('season', 'po'),
        'media_episode': ('episode', 'po'),
        'broadcaster': ('broadcaster', 'po'),

        # to be migrated to features, eventually
        'mediacriticism': ('mediacriticism', 'wl'),  # SMC
        'categories_by_url': ('categories_by_url', 'wl'),
    }

    SENTENCE_MAPPING = {'token': ('token', 'wl'),
                        'sem_orient': ('sem_orient', 'wl'),
                        'significance': ('significance', 'wl'),
                        'md5sum': ('id', 'wl'),
                        'pos': ('pos', 'wl'),
                        'is_title': ('is_title', 'wl'),
                        'dependency': ('dependency', 'wl')}

    ANNOTATION_MAPPING = {'key': ('key', 'wl'),
                          'surfaceForm': ('surfaceForm', 'wl'),
                          'start': ('start', 'wl'),
                          'end': ('end', 'wl'),
                          'annotationType': ('annotationType', 'wl'),
                          'preferredName': ('preferredName', 'wl'),
                          'sem_orient': ('sem_orient', 'wl'),
                          'md5sum': ('md5sum', 'wl'),
                          'sentence': ('sentence', 'wl'),
                          'confidence': ('confidence', 'wl')
                          }

    FEATURE_MAPPING = {'key': ('key', 'wl')}

    RELATION_MAPPING = {'key': ('key', 'wl'),
                        'type': ('type', 'wl'),
                        'domain': ('domain', 'wl'),
                        'internal': ('internal', 'wl'),
                        'format': ('format', 'dc')}

    @classmethod
    def pre_xml_dump(cls, titles, attributes, sentences):
        return attributes, titles + sentences
