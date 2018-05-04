#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 07.04.2014

@author: heinz-peterlang
'''
from weblyzard_api.xml_content.parsers import XMLParser


class XML2013(XMLParser):

    SUPPORTED_NAMESPACE = 'http://www.weblyzard.com/wl/2013#'
    DOCUMENT_NAMESPACES = {'wl': SUPPORTED_NAMESPACE,
                           'dc': 'http://purl.org/dc/elements/1.1/',
                           'xml': 'http://www.w3.org/XML/1998/namespace',
                           'sioc': 'http://rdfs.org/sioc/ns#',
                           #                            'skos': 'http://www.w3.org/2004/02/skos/core#',
                           #                            'foaf': 'http://xmlns.com/foaf/0.1/',
                           'ma': 'http://www.w3.org/ns/ma-ont#'}
    VERSION = 2013
    ATTR_MAPPING = {

        # CORE ATTRIBUTES #####################################################
        # kept for legacy
        'lang': '{%s}lang' % DOCUMENT_NAMESPACES['xml'],

        'language': '{%s}language' % DOCUMENT_NAMESPACES['dc'],
        'content_type': '{%s}format' % DOCUMENT_NAMESPACES['dc'],
        'publication_date': '{%s}issued' % DOCUMENT_NAMESPACES['dc'],
        'published_date': '{%s}issued' % DOCUMENT_NAMESPACES['dc'],
        'last_modified': '{%s}modified' % DOCUMENT_NAMESPACES['dc'],
        'url': '{%s}identifier' % DOCUMENT_NAMESPACES['dc'],
        'uri': '{%s}identifier' % DOCUMENT_NAMESPACES['dc'],
        'license': '{%s}license' % DOCUMENT_NAMESPACES['dc'],
        'creator': '{%s}creator' % DOCUMENT_NAMESPACES['dc'],
        'author': '{%s}creator' % DOCUMENT_NAMESPACES['dc'],
        'publisher': '{%s}publisher' % DOCUMENT_NAMESPACES['dc'],
        'keywords': '{%s}subject' % DOCUMENT_NAMESPACES['dc'],
        'title': '{%s}title' % DOCUMENT_NAMESPACES['dc'],

        'nilsimsa': '{%s}nilsimsa' % DOCUMENT_NAMESPACES['wl'],
        'content_id': '{%s}id' % DOCUMENT_NAMESPACES['wl'],
        'jonas_type': '{%s}jonas_type' % DOCUMENT_NAMESPACES['wl'],
        'thumbnail': '{%s}thumbnail' % DOCUMENT_NAMESPACES['wl'],
        'description': '{%s}description' % DOCUMENT_NAMESPACES['wl'],
        'is_sensitive': '{%s}is_sensitive' % DOCUMENT_NAMESPACES['wl'],

        # FB, YT
        'picture': '{%s}thumbnail' % DOCUMENT_NAMESPACES['wl'],
        # FB
        'org_picture': '{%s}thumbnail' % DOCUMENT_NAMESPACES['wl'],
        # FB
        'group_picture': '{%s}thumbnail' % DOCUMENT_NAMESPACES['wl'],
        # FB
        'fbType': '{%s}post_type' % DOCUMENT_NAMESPACES['wl'],
        'location': '{%s}location' % DOCUMENT_NAMESPACES['wl'],
        # YT, vimeo/daily
        'duration': '{%s}duration' % DOCUMENT_NAMESPACES['wl'],
        # to be migrated to features, eventually
        'mediacriticism': '{%s}mediacriticism' % DOCUMENT_NAMESPACES['wl'],

        # DOCUMENT RELATIONS (CID<->CID only) #################################
        # reference to ohter document (outgoing link)
        'references': '{%s}references' % DOCUMENT_NAMESPACES['dc'],
        # reference to similar document (re-tweet)
        'source': '{%s}source' % DOCUMENT_NAMESPACES['dc'],
        # reference to top-level parent (thread ancestor)
        'has_container': '{%s}has_container' % DOCUMENT_NAMESPACES['sioc'],
        # reference to direct parent (nested thread parent)
        'reply_of': '{%s}reply_of' % DOCUMENT_NAMESPACES['sioc'],

        # MULTIMEDIA
        'media_url': '{%s}locator' % DOCUMENT_NAMESPACES['ma'],
        'media_type': '{%s}format' % DOCUMENT_NAMESPACES['ma'],
        'media_recordingLocation': '{%s}createdIn' % DOCUMENT_NAMESPACES['ma'],
        'media_recordingDate': '{%s}creationDate' % DOCUMENT_NAMESPACES['ma'],
        'media_license': '{%s}hasPolicy' % DOCUMENT_NAMESPACES['ma'],

        # SM_METRICS
        'user_mentions': '{%s}user_mentions' % DOCUMENT_NAMESPACES['wl'],
        'rating': '{%s}rating' % DOCUMENT_NAMESPACES['wl'],
        # YT
        'rating_average': '{%s}rating' % DOCUMENT_NAMESPACES['wl'],
        # vimeo/daily
        'viewcount': '{%s}num_views' % DOCUMENT_NAMESPACES['wl'],
        # youtube
        'statistics_viewcount': '{%s}num_views' % DOCUMENT_NAMESPACES['wl'],
        'comment_count': '{%s}num_replies' % DOCUMENT_NAMESPACES['wl'],
        # g+
        'reshares': '{%s}num_reshares' % DOCUMENT_NAMESPACES['wl'],
        # twitter
        'nr_of_retweets': '{%s}num_reshares' % DOCUMENT_NAMESPACES['wl'],

        # USER MAPPINGS #######################################################
        # FB, G+
        'user_id': '{%s}user_id' % DOCUMENT_NAMESPACES['wl'],
        # YT, twitter
        'user_url': '{%s}user_id' % DOCUMENT_NAMESPACES['wl'],
        'user_name': '{%s}user_name' % DOCUMENT_NAMESPACES['wl'],
        'user_type': '{%s}user_type' % DOCUMENT_NAMESPACES['wl'],
        # twitter
        'current_status': '{%s}user_status' % DOCUMENT_NAMESPACES['wl'],
        'screen_name': '{%s}user_screen_name' % DOCUMENT_NAMESPACES['wl'],
        # twitter
        'user_location': '{%s}user_location' % DOCUMENT_NAMESPACES['wl'],
        # twitter
        'user_time_zone': '{%s}user_timezone' % DOCUMENT_NAMESPACES['wl'],
        'user_thumbnail': '{%s}user_thumbnail' % DOCUMENT_NAMESPACES['wl'],
        # twitter
        'user_img_url': '{%s}user_thumbnail' % DOCUMENT_NAMESPACES['wl'],

        # USER METRICS #######################################################
        # FB
        'likes_count': '{%s}user_rating' % DOCUMENT_NAMESPACES['wl'],
        # FB
        'org_likes_count': '{%s}user_rating' % DOCUMENT_NAMESPACES['wl'],
        # FB
        'group_likes_count': '{%s}user_rating' % DOCUMENT_NAMESPACES['wl'],
        # twitter
        'followers': '{%s}user_rating' % DOCUMENT_NAMESPACES['wl'],
        # G+
        'plusoners': '{%s}user_rating' % DOCUMENT_NAMESPACES['wl'],

    }
    SENTENCE_MAPPING = {'{%s}token' % DOCUMENT_NAMESPACES['wl']: 'token',
                        '{%s}sem_orient' % DOCUMENT_NAMESPACES['wl']: 'sem_orient',
                        '{%s}significance' % DOCUMENT_NAMESPACES['wl']: 'significance',
                        '{%s}id' % DOCUMENT_NAMESPACES['wl']: 'md5sum',
                        '{%s}pos' % DOCUMENT_NAMESPACES['wl']: 'pos',
                        '{%s}is_title' % DOCUMENT_NAMESPACES['wl']: 'is_title',
                        '{%s}dependency' % DOCUMENT_NAMESPACES['wl']: 'dependency'}
    ANNOTATION_MAPPING = {'{%s}key' % DOCUMENT_NAMESPACES['wl']: 'key',
                          '{%s}surfaceForm' % DOCUMENT_NAMESPACES['wl']: 'surfaceForm',
                          '{%s}start' % DOCUMENT_NAMESPACES['wl']: 'start',
                          '{%s}end' % DOCUMENT_NAMESPACES['wl']: 'end',
                          '{%s}annotationType' % DOCUMENT_NAMESPACES['wl']: 'annotation_type',
                          '{%s}preferredName' % DOCUMENT_NAMESPACES['wl']: 'preferredName',
                          '{%s}sem_orient' % DOCUMENT_NAMESPACES['wl']: 'sem_orient',
                          '{%s}md5sum' % DOCUMENT_NAMESPACES['wl']: 'md5sum'}
    FEATURE_MAPPING = {'{%s}key' % DOCUMENT_NAMESPACES['wl']: 'key',
                       '{%s}context' % DOCUMENT_NAMESPACES['wl']: 'context'}
    RELATION_MAPPING = {'{%s}key' % DOCUMENT_NAMESPACES['wl']: 'key'}

    @classmethod
    def pre_xml_dump(cls, titles, attributes, sentences):
        return attributes, titles + sentences
