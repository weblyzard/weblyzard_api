'''
Created on Jan 4, 2013

@author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''
from unittest import main, TestCase

from eWRT.ws.rest import RESTClient, MultiRESTClient
from weblyzard_api.xml_content import XMLContent
from os import getenv
import time

JEREMIA_API_URL  = getenv("WEBLYZARD_API_URL") or "http://localhost:8080"
JEREMIA_API_USER = getenv("WEBLYZARD_API_USER")
JEREMIA_API_PASS = getenv("WEBLYZARD_API_PASS")

class Jeremia(RESTClient):
    '''
    Jeremia Web Service
    '''
    
    def __init__(self, url=JEREMIA_API_URL, usr=JEREMIA_API_USER, pwd=JEREMIA_API_PASS):
        url += '/jeremia/rest'
        RESTClient.__init__(self, url, usr, pwd)

    def commit(self, batch_id):
        """ @param batch_id: the batch_id to retrieve 
            @return: a generator yielding all the documents of that
                     particular patch 
        """
        while True:
            docs = self.execute('commit', batch_id)
            if not docs:
                return
            for doc in docs:
                yield doc

    def submit_documents( self, batch_id, documents ):
        """ 
        @param batch_id: batch_id to use for the given submission
        @param documents: a list of dictionaries containing the document 
        """
        if not documents:
            raise ValueError("Cannot process an empty document list")
        return self.execute('submit_documents', batch_id, documents)
        
    def status(self):
        return self.execute('status')
    
    def get_xml_doc(self, text, content_id = "1"):
        """
        Processes text and returns a XMLContent object.
        @param text: the text to process
        @param content_id: optional content id
        """
        batch = [{'id': content_id, 'body': text, 'format': 'html/text'}]
        num = str(int(time.time()))
        self.submit_documents(num, batch)
        results = list(self.commit(num))
        result = results[0]
        return XMLContent(result['xml_content'])


class JeremiaClient2(MultiRESTClient):
    
    def __init__(self, service_urls):
        MultiRESTClient.__init__(self, service_urls)
    
    def commit(self, batch_id):
        ''' returns a generator ''' 
        while True:
            result = self.request('commit/%s' % batch_id)
            if not result:
                break
            else:
                for doc in result:
                    yield doc
    
    def submit_documents(self, batch_id, documents):
        return self.request('submit_documents/%s' % batch_id, documents)

    def submit_documents_blacklist(self, batch_id, documents, source_id):
        url = 'submit_documents_blacklist/%s/%s' % (batch_id, source_id)
        return self.request(url, documents)
    
    def update_blacklist(self, source_id, blacklist):
        ''' updates an existing blacklist cache '''
        url = 'cache/updateBlacklist/%s' % source_id
        return self.request(url, blacklist)
        
    def clear_blacklist(self, source_id):
        ''' empties existing blacklist cache ''' 
        return self.request('cache/clearBlacklist/%s' % source_id)
        
    def get_blacklist(self, source_id):
        return self.request('cache/getBlacklist/%s' % source_id)

    def submit(self, batch_id, documents, source_id=None, use_blacklist=False):
         
        if use_blacklist: 
            if not source_id:
                raise Exception('Blacklist requires a source_id')
        
            url = 'submit_documents_blacklist/%s/%s' % (batch_id, source_id)
        else: 
            url = 'submit_documents/%s' % batch_id
            
        self.request(url, documents)
        
        return self.commit(batch_id) 

class JeremiaTest(TestCase):

    DOCS = [ {'id': content_id,
              'body': 'Good day Mr. President! Hello "world" ' + str(content_id),
              'title': 'Hello "world" more ',
              'format': 'html/text',
              'header': {}}  for content_id in xrange(1000,1020)]

    def test_batch_processing(self):
        j = Jeremia()
        print "Submitting documents..."
        j.submit_documents( "1234", self.DOCS[:10] )
        j.submit_documents( "1234", self.DOCS[10:] )
        
        # retrieve initial patch 
        print "Retrieving results..."
        docs = list(j.commit( "1234" ) )
        self.assertEqual( len(docs), 20 )
        
        # no more results are available
        self.assertEqual( len(list(j.commit("1234"))), 0 )


    def test_sentence_splitting(self):
        j = Jeremia()
        j.submit_documents( "1222", self.DOCS[:1] )

        for doc in j.commit("1222"):
            # extract sentences
            sentences = [ s.sentence 
                          for s in XMLContent(doc['xml_content']).sentences ]
            print doc['xml_content']
            assert 'wl:is_title' in doc['xml_content']
            print sentences
            self.assertEqual( len(sentences), 3 )

    def test_illegal_xml_format_filtering(self):
        DOCS = [ {'id': "alpha",
                  'body': 'This is an illegal XML Sequence: J\x1amica',
                  'title': 'Hello "world" more ',
                  'format': 'html/text',
                  'header': {}}  ]

        j = Jeremia()
        j.submit_documents( "12234", DOCS )
        for doc in list(j.commit("12234")):
            xml = XMLContent(doc['xml_content'])
            print doc['xml_content']
            assert xml.sentences[0].sentence != None
       

    def test_illegal_input_args(self):
        j = Jeremia()

        with self.assertRaises(ValueError):
            j.submit_documents("1223", [] )
        
if __name__ == '__main__':
    j = Jeremia()
    from sys import argv
    d = [ {'title': '',
           'body': argv[1].strip(), 
           'id': 99933,
           'format': 'text/html',
           'header': {'dc:related': 'http://www.heise.de http://www.kurier.at'},
          } 
        ]
    print d
    j.submit_documents( "1239", d )
    doc = list( j.commit("1239") )[0]
    print doc['xml_content']
    sentences = XMLContent(doc['xml_content']).sentences
    for s in sentences:
        print s.sentence
        print s.pos_tags
        print list(s.tokens)

    exit()
    main()
