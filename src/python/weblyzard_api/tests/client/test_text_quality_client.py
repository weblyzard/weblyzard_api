import unittest

from weblyzard_api.client.textqualityclient.client_text_quality import TextQualityClient


class TestTextQualityClient(unittest.TestCase):
    """
    Each test tuple has:

    - first item: full text, two sentences or more
    - Second item: number of passive sentences
    - Third item: nb of sentences in the text

    - Fourth item: single sentence
    - Fifth item: nb of passive words in the single sentences
    - Sixth item: bool, true if single sentence is passive
    """

    TEST_CASES = [

        ("@RT This is just a text. It was supposed to be funny",
         1, 2,
         "it was supposed to be you in this case",
         2, True),

        ("apple is releasing a new software update. The savannah is roamed by "
         "beautiful giraffes.",
         1, 2,
         "At dinner, six shrimp were eaten by Harry",
         2, True),

        ("I ran the obstacle course in record time."
         " The crew paved the entire stretch of highway.",
         0, 2,
         "it was supposed to be you in this case",
         2, True),

        ("The entire house was painted by Tom.. It was supposed to look nice",
         2, 2,
         "it was supposed to be you in this case",
         2, True),

        ("Susan will bake two dozen cupcakes for the bake sale."
         " The wedding planner is making all the reservations. "
         "The science class viewed the comet.",
         0, 3,
         "Thousands of tourists visit the Grand Canyon every year.",
         0, False),

        ("The homeowners remodeled the house to help it sell."
         " The metal beams were corroded by the saltwater. "
         "I will clean the house every Saturday.",
         1, 3,
         "Harry ate six shrimp at dinner.",
         0, False),
        ]

    TEXTQUALITYINSTANCE = TextQualityClient(
        'http://skb-viewer-lexical.prod.i.weblyzard.net:8443')

    # testing on single sentence
    def test_text_quality_sentence(self):
        for value in self.TEST_CASES:
            passive_words = self.TEXTQUALITYINSTANCE. \
                get_single_sentence_passive_words(value[3])
            assert len(passive_words) == value[4]

            is_passive = self.TEXTQUALITYINSTANCE. \
                is_single_sentence_passive(value[3])
            assert is_passive == value[5]

    # testing on full text
    def test_text_quality_full_text(self):
        for value in self.TEST_CASES:
            passive_sent_cnt = self.TEXTQUALITYINSTANCE. \
                get_passive_sentences_count_from_text(value[0])
            assert passive_sent_cnt == value[1]

            sent_cnt = self.TEXTQUALITYINSTANCE. \
                get_sentences_count_from_text(value[0])
            assert sent_cnt == value[2]


if __name__ == '__main__':
    unittest.main()
