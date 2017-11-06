'''
Created on 14.02.2014

@author: heinz-peterlang
'''
from weblyzard_api.client.openrdf import OpenRdfClient

class SPARQLQuery(object):
    
    def __init__(self, repository):
        
        pass
    

QUERIES = {
'configured_profiles': 
    '''
        PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?s ?profile_name 
        WHERE {
               ?s rdfs:label  ?profile_name .
        }
    '''           
}

if __name__ == '__main__':
    server_uri = ''
    repository_name = 'config.weblyzard.com'
    
    query = '''
    
    '''
    
    client = OpenRdfClient(server_uri)
    
    #results = client.run_query(repository_name, query)
    #
    #for result in results: 
    #    print result
    
    #client.update_profile(profile_name=None, profile_definition=None)
    
    
    '''
            DELETE DATA
            {
                <http://www.weblyzard.com/recognize/lexicon/en.off.cities.500000> ?p ?o
            }
            
    '''
    
    '''
    SELECT * WHERE 
            {
                <http://www.weblyzard.com/recognize/lexicon/en.off.cities.500000> ?p ?o
            }
    '''
    
    
    print(client.get_profiles())
