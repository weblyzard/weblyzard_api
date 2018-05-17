#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 07.04.2014

@author: heinz-peterlang
'''
from weblyzard_api.xml_content.parsers import XMLParser


class XML2013(XMLParser):

    VERSION = 2013

    SUPPORTED_NAMESPACE = 'http://www.weblyzard.com/wl/2013#'

    DOCUMENT_NAMESPACES = {'wl': SUPPORTED_NAMESPACE,
                           'dc': 'http://purl.org/dc/elements/1.1/',
                           'xml': 'http://www.w3.org/XML/1998/namespace',
                           'xsd': 'http://www.w3.org/2001/XMLSchema',
                           'sioc': 'http://rdfs.org/sioc/ns#',
                           'skos': 'http://www.w3.org/2004/02/skos/core#',
                           'foaf': 'http://xmlns.com/foaf/0.1/',
                           'ma': 'http://www.w3.org/ns/ma-ont#',
                           'po': 'http://purl.org/ontology/po/',
                           'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                           'rdfs': 'http://www.w3.org/2000/01/rdf-schema#'}

    ATTR_MAPPING = {
        'lang': ('lang', 'xml'),  # legacy
        'language': ('language', 'dc'),
        'content_type': ('format', 'dc'),
        'publication_date': ('issued', 'dc'),
        'published_date': ('issued', 'dc'),
        'last_modified': ('modified', 'dc'),
        'url': ('identifier', 'dc'),
        'uri': ('identifier', 'dc'),
        'license': ('license', 'dc'),
        'creator': ('creator', 'dc'),
        'author': ('creator', 'dc'),
        'publisher': ('publisher', 'dc'),
        'keywords': ('subject', 'dc'),
        'title': ('title', 'dc'),

        # internal
        'nilsimsa': ('nilsimsa', 'wl'),
        'content_id': ('id', 'wl'),
        'jonas_type': ('jonas_type', 'wl'),

        'fbType': ('post_type', 'wl'),  # FB
        'thumbnail': ('thumbnail', 'wl'),
        'picture': ('thumbnail', 'wl'),  # FB, YT
        'org_picture': ('thumbnail', 'wl'),  # FB
        'group_picture': ('thumbnail', 'wl'),  # FB
        'description': ('description', 'wl'),
        'location': ('location', 'wl'),  # YT, vimeo/daily
        'duration': ('duration', 'wl'),
        'is_sensitive': ('is_sensitive', 'wl'),  # YT

        # For events, broadcasts, etc.
        'temporal_start': ('temporalStart', 'wl'),
        'temporal_end': ('temporalEnd', 'wl'),

        # DOCUMENT RELATIONS (CID<->CID only) #################################
        # reference to other document (outgoing link)
        'references': ('references', 'dc'),
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
                          'md5sum': ('md5sum', 'wl')
                          }

    FEATURE_MAPPING = {'key': ('key', 'wl'),
                       'content': ('key', 'wl')}

    RELATION_MAPPING = {'key': ('key', 'wl')}

    @classmethod
    def pre_xml_dump(cls, titles, attributes, sentences):
        return attributes, titles + sentences
