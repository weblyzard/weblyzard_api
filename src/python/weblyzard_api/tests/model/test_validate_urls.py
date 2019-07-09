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

        assert JSON10ParserDocument._validate_urls(valid_url)
        assert not JSON10ParserDocument._validate_urls(non_valid_url)


if __name__ == '__main__':
    unittest.main()


