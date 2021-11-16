from weblyzard_api.client import MultiRESTClient


class TextQualityClient(MultiRESTClient):
    TEXT_QUALITY_PATH = '/1.0/text_quality'

    def __init__(self, url):
        MultiRESTClient.__init__(self, service_urls=url)

    def get_document_text_quality(self, body: str, fetch_passive: bool = True,
                                  fetch_transition_words: bool = True):

        """
        "fetch_passive" means that the tokens indicating passive voice and
        the sentences containing them will be returned.

        "transition_words" means that the endpoint attempts to detect
        different types of transition/linking words
        (types are "addition", "contrast", "emphasis", and "order")
        """

        result = None
        retrycount = 1
        retries = 0
        while retries <= retrycount:
            retries += 1
            try:
                result = self.request(
                    self.TEXT_QUALITY_PATH,
                    parameters={
                        'passive': fetch_passive,
                        'body': body,
                        'transition_words': fetch_transition_words
                    }
                )
                break
            except Exception as e:
                if retries <= retrycount:
                    pass  # silently retry
                else:
                    result = {
                        'error': 'Request to text quality '
                                 'webservice timed out %d times' % retries}
        return result

    def get_sentences_count_from_text(self, body: str):
        if body:
            result = self.get_document_text_quality(body=body)
            return len(result['raw_annotation']['partitions']['SENTENCE'])

    def get_passive_sentences_count_from_text(self, body: str):
        if body:
            result = self.get_document_text_quality(body=body)
            count = 0
            if "passive" in result:
                for value in result['passive']:
                    if value['@type'] == 'SentenceCharSpan':
                        count += 1
        return count

    # accept input sentence, returns True if passive Flase otherwise
    def is_single_sentence_passive(self, sentence: str):
        if sentence:
            result = self.get_document_text_quality(body=sentence)
            if len(result['passive']) > 0:
                out = True
            else:
                out = False
        return out

    # return a list of words indicating the passive content
    def get_single_sentence_passive_words(self, sentence: str):
        if sentence:

            result = self.get_document_text_quality(body=sentence)
            words = []

            if len(result['passive']) > 0:
                for word in result['passive'][1:]:
                    word_start = word['start']
                    word_end = word['end']
                    words.append(sentence[word_start:word_end])
        return words

