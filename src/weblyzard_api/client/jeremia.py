'''
Created on Jan 4, 2013

@author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''
from unittest import main, TestCase

from eWRT.ws.rest import RESTClient
from weblyzardServices.xml_content import XMLContent

JEREMIA_URL = "http://localhost:8080/jeremia/rest"

class Jeremia(RESTClient):
    '''
    Jeremia Web Service
    '''
    
    def __init__(self, url=JEREMIA_URL, usr=None, pwd=None):
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


class JeremiaTest(TestCase):

    DOCS = [ {'content_id': content_id,
              'content': 'Good day Mr. President! Hello "world" ' + str(content_id),
              'title': 'Hello "world" more ',
              'content_type': 'html/text',
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
            print sentences
            self.assertEqual( len(sentences), 2 )

    def test_illegal_xml_format_filtering(self):
        DOCS = [ {'content_id': "alpha",
                  'content': 'This is an illegal XML Sequence: J\x1amica',
                  'title': 'Hello "world" more ',
                  'content_type': 'html/text',
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
           'content': argv[1].strip(), 
           'content_id': 99933,
           'content_type': 'text/html',
           'header': {},
          } 
        ]
    print d
    j.submit_documents( "1239", d )
    doc = list( j.commit("1239") )[0]
    sentences = XMLContent(doc['xml_content']).sentences
    print doc
    for s in sentences:
        print s.sentence
        print s.pos
        print s.token

    exit()
    main()
