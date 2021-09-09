import unittest
import pytest

from weblyzard_api.client.textqualityclient.client_text_quality import TextQualityClient


class TestTextQualityClient(object):
    """
    Each test tuple has:

    - first item: full text, two sentences or more
    - Second item: number of passive sentences
    - Third item: nb of sentences in the text

    - Fourth item: single sentence
    - Fifth item: nb of passive words in the single sentences
    - Sixth item: bool, true if single sentence is passive
    """

    TEST_CASES_FULL_TEXT = [
         ('@RT This is just a text. It was supposed to be funny', 1, 2),
         ('Susan will bake two dozen cupcakes for the bake sale. The wedding planner '
          'is making all the reservations. The science class viewed the comet.',
          0,
          3),
         ('The homeowners remodeled the house to help it sell. The metal beams were '
          'corroded by the saltwater. I will clean the house every Saturday.',
          1,
          3),
         ('apple is releasing a new software update. The savannah is roamed by '
          'beautiful giraffes.',
          1,
          2),
         ('The entire house was painted by Tom.. It was supposed to look nice', 2, 2),
         ('I ran the obstacle course in record time. The crew paved the entire stretch '
          'of highway.',
          0,
          2)
    ]
    TEST_CASES_SINGLE_SENTENCE = [
        ('At dinner, six shrimp were eaten by Harry', 2, True),
        ('Harry ate six shrimp at dinner.', 0, False),
        ('it was supposed to be you in this case', 2, True),
        ('Thousands of tourists visit the Grand Canyon every year.', 0, False)
    ]

    TEXTQUALITYINSTANCE = TextQualityClient(
        'http://skb-viewer-lexical.prod.i.weblyzard.net:8443')

    @pytest.mark.parametrize('text,word_count,_is_passive', TEST_CASES_SINGLE_SENTENCE)
    def test_text_quality_sentence(self, text, word_count, _is_passive):
            passive_words = self.TEXTQUALITYINSTANCE. \
                get_single_sentence_passive_words(text)
            assert len(passive_words) == word_count

            is_passive = self.TEXTQUALITYINSTANCE. \
                is_single_sentence_passive(text)
            assert is_passive == _is_passive

    @pytest.mark.parametrize('text,passive_sentences,all_sentences', TEST_CASES_FULL_TEXT)
    def test_text_quality_full_text(self, text, passive_sentences, all_sentences):
            passive_sent_cnt = self.TEXTQUALITYINSTANCE. \
                get_passive_sentences_count_from_text(text)
            assert passive_sent_cnt == passive_sentences

            sent_cnt = self.TEXTQUALITYINSTANCE. \
                get_sentences_count_from_text(text)
            assert sent_cnt == all_sentences


if __name__ == '__main__':
    unittest.main()
