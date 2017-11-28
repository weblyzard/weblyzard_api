#!/usr/bin/python
# -*- coding: utf-8 -*-
'''

'''
import unittest

class JoannaTest(unittest.TestCase):
    
    def setUp(self):
        self.joanna = JoannaTest(url="http://localhost:9000/joanna")
        self.docs = 10
        self.rand_strings = self.joanna.rand_strings(self.docs)
        self.source_id = 21555
        self.test_db = 'test_weblyzard'

    def test_random_strings(self):
        self.assertEqual(len(self.rand_strings), 10)
        
    def test_online(self):
        self.assertEqual(self.joanna.status(), '"ONLINE"')
    
    def test_batch_request(self):
        self.rand_strings = self.joanna.rand_strings(self.docs)
        batch_results = self.joanna.similar_documents(
                        self.source_id, self.test_db, 
                        self.rand_strings, 20)
        for _, similar in batch_results.iteritems():
            self.assertEqual(similar, 'false')
        batch_results = self.joanna.similar_documents(
                        self.source_id, self.test_db, 
                        self.rand_strings, 20)
        for _, similar in batch_results.iteritems():
            self.assertEqual(similar, 'true')
         
    def test_single_request(self):
        self.rand_strings = self.joanna.rand_strings(self.docs)
        single_result = self.joanna.similar_document(
                        self.source_id, self.rand_strings[0], 
                        self.test_db)
        self.assertEqual(single_result, 'false')
        single_result = self.joanna.similar_document(
                        self.source_id, self.rand_strings[0], 
                        self.test_db)
        self.assertEqual(single_result, 'true')
      
    def test_loaded(self):
        loaded_result = self.joanna.reload_source_nilsimsa(
                        self.source_id, self.test_db, 20)
        self.assertEqual(loaded_result, 'LOADED')
     
    def test_existing_document(self):
        ''' Test an existing doc from the database. Note: 
        this is expected to fail when the document becomes very old
        '''
        existing_doc = [
            '1100101100100110001001110011001000000010001000001010100',
            '001001110100010000001001110110010101100111101000011000',
            '1001001011100100001000011110110111000011011101000011',
            '0010101101100100100110010001100011010000100000110111110',
            '0101001011100010010100101111010001001011']
        existing_doc = ''.join(existing_doc)
        single_result = self.joanna.similar_document(
                        self.source_id, existing_doc, self.test_db)
        self.assertEqual(single_result, 'true')
        batch_result = self.joanna.similar_documents(
                        self.source_id, self.test_db, [existing_doc])
        for _, similar in batch_result.iteritems():
            self.assertEqual(similar, 'true')

    def test_batch_rand(self):
        docs = self.rand_strings
        batch_results = self.joanna.similar_documents(
                        self.source_id, self.test_db, 
                        docs, 20)
        print("Batch results {}".format(batch_results))
        self.rand_strings = self.joanna.rand_strings(self.docs)

        docs = self.joanna.rand_strings(30)
        batch_results = self.joanna.similar_documents(
                        self.source_id, self.test_db, docs, 20)
        print("Batch results {}".format(batch_results))

if __name__ == '__main__':    
    unittest.main()