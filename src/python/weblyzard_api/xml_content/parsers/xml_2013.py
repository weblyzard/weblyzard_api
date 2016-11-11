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
#                            'sioc': 'http://rdfs.org/sioc/ns#',
#                            'skos': 'http://www.w3.org/2004/02/skos/core#',
#                            'foaf': 'http://xmlns.com/foaf/0.1/',
                           'ma': 'http://www.w3.org/ns/ma-ont#'}
    VERSION = 2013
    ATTR_MAPPING = {'{%s}nilsimsa' % DOCUMENT_NAMESPACES['wl']: 'nilsimsa',
                    '{%s}id' % DOCUMENT_NAMESPACES['wl']: 'content_id',
                    '{%s}jonas_type' % DOCUMENT_NAMESPACES['wl']: 'jonas_type',
                    '{%s}lang' % DOCUMENT_NAMESPACES['xml']: 'lang', #kept for legacy
                    '{%s}format' % DOCUMENT_NAMESPACES['dc']: 'content_type',
                    '{%s}language' % DOCUMENT_NAMESPACES['dc']: 'language',
                    '{%s}language' % DOCUMENT_NAMESPACES['dc']: 'lang',
                    '{%s}source' % DOCUMENT_NAMESPACES['dc']: 'source',
                    '{%s}identifier' % DOCUMENT_NAMESPACES['dc']: 'url',
                    '{%s}license' % DOCUMENT_NAMESPACES['dc']: 'license',
                    '{%s}creator' % DOCUMENT_NAMESPACES['dc']: 'creator',
                    '{%s}publisher' % DOCUMENT_NAMESPACES['dc']: 'publisher',
                    '{%s}subject' % DOCUMENT_NAMESPACES['dc']: 'keywords',
                    '{%s}title' % DOCUMENT_NAMESPACES['dc']: 'title',
                    '{%s}thumbnail' % DOCUMENT_NAMESPACES['wl']: 'thumbnail',
                    '{%s}thumbnail' % DOCUMENT_NAMESPACES['wl']: 'picture', #FB, YT
                    '{%s}thumbnail' % DOCUMENT_NAMESPACES['wl']: 'org_picture', #FB
                    '{%s}thumbnail' % DOCUMENT_NAMESPACES['wl']: 'group_picture', #FB
                    '{%s}post_type' % DOCUMENT_NAMESPACES['wl']: 'fbType', #FB
                    '{%s}location' % DOCUMENT_NAMESPACES['wl']: 'location',
                    '{%s}duration' % DOCUMENT_NAMESPACES['wl']: 'duration', #YT, vimeo/daily
                    '{%s}mediacriticism' % DOCUMENT_NAMESPACES['wl']: 'mediacriticism', #to be migrated to features, eventually
                    '{%s}article_content_id' % DOCUMENT_NAMESPACES['wl']: 'article_content_id', #to be migrated to relations eventually
                    
                    #INVID
                    '{%s}locator' % DOCUMENT_NAMESPACES['ma']: 'media_url',
                    '{%s}format' % DOCUMENT_NAMESPACES['ma']: 'media_type',
                    '{%s}createdIn' % DOCUMENT_NAMESPACES['ma']: 'media_recordingLocation',
                    '{%s}creationDate' % DOCUMENT_NAMESPACES['ma']: 'media_recordingDate',
                    '{%s}hasPolicy' % DOCUMENT_NAMESPACES['ma']: 'media_license',
                    
                    #SM_METRICS
                    '{%s}user_mentions' % DOCUMENT_NAMESPACES['wl']: 'user_mentions',
                    '{%s}rating' % DOCUMENT_NAMESPACES['wl']: 'rating',
                    '{%s}rating' % DOCUMENT_NAMESPACES['wl']: 'rating_average', #YT
                    '{%s}num_views' % DOCUMENT_NAMESPACES['wl']: 'viewcount', #vimeo/daily
                    '{%s}num_views' % DOCUMENT_NAMESPACES['wl']: 'statistics_viewcount', #youtube
                    '{%s}num_replies' % DOCUMENT_NAMESPACES['wl']: 'comment_count',
                    '{%s}num_reshares' % DOCUMENT_NAMESPACES['wl']: 'reshares', #g+ 
                    '{%s}num_reshares' % DOCUMENT_NAMESPACES['wl']: 'nr_of_retweets', #twitter                    
                    
                    #USER MAPPTINGS
                    '{%s}user_id' % DOCUMENT_NAMESPACES['wl']: 'user_id', #FB, G+
                    '{%s}user_id' % DOCUMENT_NAMESPACES['wl']: 'user_url', #YT, twitter
                    '{%s}user_name' % DOCUMENT_NAMESPACES['wl']: 'user_name',
                    '{%s}user_type' % DOCUMENT_NAMESPACES['wl']: 'user_type',
                    '{%s}user_status' % DOCUMENT_NAMESPACES['wl']: 'current_status', #twitter
                    '{%s}user_screen_name' % DOCUMENT_NAMESPACES['wl']: 'screen_name',
                    '{%s}user_location' % DOCUMENT_NAMESPACES['wl']: 'user_location', #twitter
                    '{%s}user_timezone' % DOCUMENT_NAMESPACES['wl']: 'user_time_zone', #twitter
                    '{%s}user_thumbnail' % DOCUMENT_NAMESPACES['wl']: 'user_thumbnail',
                    '{%s}user_thumbnail' % DOCUMENT_NAMESPACES['wl']: 'user_img_url', #twitter
                    
                    #USER METRICS
                    '{%s}user_rating' % DOCUMENT_NAMESPACES['wl']: 'likes_count', #FB
                    '{%s}user_rating' % DOCUMENT_NAMESPACES['wl']: 'org_likes_count', #FB
                    '{%s}user_rating' % DOCUMENT_NAMESPACES['wl']: 'group_likes_count', #FB
                    '{%s}user_rating' % DOCUMENT_NAMESPACES['wl']: 'following', #twitter
                    '{%s}user_rating' % DOCUMENT_NAMESPACES['wl']: 'plusoners', #G+
#                     '{%s}user_outdegree' % DOCUMENT_NAMESPACES['wl']: 'following', #twitter
#                     '{%s}user_indegree' % DOCUMENT_NAMESPACES['wl']: 'followers', #twitter

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