import unittest

from client.textqualityclient.client_text_quality import TextQualityClient


class TestTextQualityClient(unittest.TestCase):
    TEST_CASES = [
        ("@RT This is just a text. It was supposed to be funny",
         "it was supposed to be you in this case"),

        ("#love The wind is blowing. he is sopposed to cover us",
         "this is supposed to happen today"),

        ]

    TEXTQUALITYINSTANCE = TextQualityClient(
        'http://skb-viewer-lexical.prod.i.weblyzard.net:8443')

    def test_text_quality_sentence(self):
        for value in self.TEST_CASES:
            passive_words = self.TEXTQUALITYINSTANCE. \
                get_single_sentence_passive_words(value[1])
            assert len(passive_words) == 2

            is_passive = self.TEXTQUALITYINSTANCE. \
                is_single_sentence_passive(value[1])
            assert is_passive == True

    def test_text_quality_full_text(self):
        for value in self.TEST_CASES:
            passive_sent_cnt = self.TEXTQUALITYINSTANCE. \
                get_passive_sentences_count_from_text(value[0])
            assert passive_sent_cnt == 1

            sent_cnt = self.TEXTQUALITYINSTANCE. \
                get_sentences_count_from_text(value[0])
            assert sent_cnt == 2


if __name__ == '__main__':
    unittest.main()
