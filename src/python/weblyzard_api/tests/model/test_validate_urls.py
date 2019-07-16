import unittest

from wl_core_ng.models.document import JSON10ParserDocument


class TestValidURLs(unittest.TestCase):

    def test(self):
        valid_url = {
            "content": "Puzzles and crosswords won't necessarily prevent Alzheimer's https://t.co/J8uojkURj4 via @NetDoctor",
            "content_type": "text/plain",
            "repository_id": "communidata.weblyzard.com/api",
            "uri": "https://twitter.com/status/324623423432432325632",
            "title": "Tweet by Max Goebel"
        }

        non_valid_url = {

            "content": "Puzzles and crosswords won't necessarily prevent Alzheimer's https://t.co/J8uojkURj4 via @NetDoctor",
            "content_type": "text/plain",
            "repository_id": "communidata.weblyzard.com/api",
            "uri": "/status/324623423432432325632",
            "title": "Tweet by Max Goebel"
        }
        valid_relations = {

            "content": "Puzzles and crosswords won't necessarily prevent Alzheimer's https://t.co/J8uojkURj4 via @NetDoctor",
            "content_type": "text/plain",
            "repository_id": "communidata.weblyzard.com/api",
            "uri": "https://twitter.com/status/324623423432432325632",
            "title": "Tweet by Max Goebel",
            'relations': {'dc:references': ['http://google.com/path_to_file',
                                            'https://gmail.com/path_to_mail'],
                          'sioc:reply_of': 'https://gmail.com/random_thing'}
        }

        non_valid_relations_path_error = {

            "content": "Puzzles and crosswords won't necessarily prevent Alzheimer's https://t.co/J8uojkURj4 via @NetDoctor",
            "content_type": "text/plain",
            "repository_id": "communidata.weblyzard.com/api",
            "uri": "https://twitter.com/status/324623423432432325632",
            "title": "Tweet by Max Goebel",
            'relations': {
                'dc:references': ['http://google.com',
                                  'https://gmail.com/path_to_mail'],  # first url doesn't have path, not accepted
                'sioc:reply_of': 'https://randomdomain.org/random_thing'
            }
        }
        non_valid_relations_array_error = {

            "content": "Puzzles and crosswords won't necessarily prevent Alzheimer's https://t.co/J8uojkURj4 via @NetDoctor",
            "content_type": "text/plain",
            "repository_id": "communidata.weblyzard.com/api",
            "uri": "https://twitter.com/status/324623423432432325632",
            "title": "Tweet by Max Goebel",
            'relations': {
                'dc:references': ['http://google.com/something',
                                  'https://gmail.com/path_to_mail'],
                'sioc:reply_of': 'https://random_domain.org/random_thing',
                'key': {'urls': ['http://google.com/path_to_file',
                                 'https://gmail.com/path_to_mail']}  # it should be array
            }
        }
        non_valid_relations = {

            "content": "Puzzles and crosswords won't necessarily prevent Alzheimer's https://t.co/J8uojkURj4 via @NetDoctor",
            "content_type": "text/plain",
            "repository_id": "communidata.weblyzard.com/api",
            "uri": "https://twitter.com/status/324623423432432325632",
            "title": "Tweet by Max Goebel",
            'relations': {
                'dc:references': ['http://google.com/something',
                                  'https://gmail.com/path_to_mail'],
                'sioc:reply_of': 'https:///random_thing'  # doesn't have domain
            }
        }

        assert JSON10ParserDocument._validate_urls(valid_relations)[0]

        assert not JSON10ParserDocument._validate_urls(non_valid_relations)[0]
        assert not JSON10ParserDocument._validate_urls(non_valid_relations_array_error)[0]
        assert not JSON10ParserDocument._validate_urls(non_valid_relations_path_error)[0]

        assert JSON10ParserDocument._validate_urls(valid_url)[0]

        assert not JSON10ParserDocument._validate_urls(non_valid_url)[0]


if __name__ == '__main__':
    unittest.main()
