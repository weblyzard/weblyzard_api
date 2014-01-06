#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Feb, 27 2013

@author: heinz-peterlang

'''
import unittest

from weblyzard_api.xml_content.xml_content_2005 import XMLContent as XMLContentOld
from weblyzard_api.xml_content import XMLContent, Sentence, DOCUMENT_NAMESPACE

class TranslateXML(object):
    
    # mapping: xml sentence --> xml_content.Sentence 
    SENTENCE_TRANSLATION_TABLE = { 
        'pos': 'pos_tag_string',
        'id': 'md5sum',
        'md5sum': 'md5sum',
        'token': 'token_indices',
        'sem_orient': 'sem_orient',
        'significance': 'significance',
        'pos_tags': 'pos_tag_string',
        'is_title': 'is_title',
        'sentence': 'sentence'}

    ATTRIBUTE_TRANSLATION_TABLE = {
        'content_id': '{%s}id' % DOCUMENT_NAMESPACE['wl'],
        'lang': '{%s}lang' % DOCUMENT_NAMESPACE['xml'],
        'nilsimsa': '{%s}nilsimsa' % DOCUMENT_NAMESPACE['wl'],
        'title': '{%s}title' % DOCUMENT_NAMESPACE['dc'],
        'type': '{%s}format' % DOCUMENT_NAMESPACE['dc']}
    
    @classmethod
    def translate(cls, xml_content, skip_none_values=False):
        '''
        translates wl:xml 2005 to wl:xml 2013
        :param xml_content: XML as text
        :type xml_content: str or unicode
        :param skip_none_values: should the function remove None values
        :type skip_none_values: bool
        :rtype: str
        '''
        xml_obj_old = XMLContentOld(xml_content)
        
        new_attributes = cls.translate_object(xml_obj_old.attributes, 
                                              cls.ATTRIBUTE_TRANSLATION_TABLE,
                                              skip_none_values=skip_none_values)
        
        assert len(new_attributes) == len(xml_obj_old.attributes)

        new_sentences = []

        for sentence in xml_obj_old.sentences:
            new_sentence = cls.translate_object(sentence.__dict__, 
                                                cls.SENTENCE_TRANSLATION_TABLE,
                                                skip_none_values=True)        
            new_sentences.append(Sentence(**new_sentence))
    
        xml = XMLContent.get_xml_from_dict(new_attributes, new_sentences)
        return  xml.get_xml_document()

    @classmethod
    def translate_object(cls, old_object, translation_table, 
                         skip_none_values=False):
        new_object = {}
        
        for attribute, value in old_object.iteritems():
            
            if skip_none_values and not value:
                continue
            
            if attribute in translation_table:
                attribute = translation_table[attribute] 
            
            new_object[attribute] = value
            
        return new_object


class TestTranslateXML(unittest.TestCase):
    
    def check_document(self, xml_content_old):

        xml_obj_old = XMLContentOld(xml_content_old)
        plain_text_old = xml_obj_old.plain_text
        
        xml_content_new = TranslateXML.translate(xml_content_old)
        xml_obj_new = XMLContent(xml_content_new)
        
        assert xml_obj_new
        
        plain_text_new = xml_obj_new.plain_text
        
        assert len(xml_content_new)
        assert len(xml_obj_new.sentences) == len(xml_obj_old.sentences)
        assert plain_text_old == plain_text_new

        for sentence in xml_obj_new.sentences: 
            sentence_attributes = sentence.get_xml_attributes().keys()
            assert all('wl/2013' in attr for attr in sentence_attributes)
    
        return xml_obj_new
    
    def test_translate(self):
        ''' '''
        from weblyzard_api.xml_content.tests import get_test_data
        
        test_files = ('xml_content_old.xml', 'xml_content_old2.xml')
        
        for test_file in test_files: 
            print 'testing file %s' % test_file
            xml_content_old = get_test_data(test_file)
            xml_obj = self.check_document(xml_content_old)
            print xml_obj.attributes
            
if __name__ == '__main__':
    unittest.main()