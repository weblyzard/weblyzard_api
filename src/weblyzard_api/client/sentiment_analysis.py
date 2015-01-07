'''
.. codeauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''

from eWRT.ws.rest import RESTClient
from unittest import main, TestCase

#SENTIMENT_ANALYSIS_URL = "http://localhost:8000"
SENTIMENT_ANALYSIS_URL = "http://voyager.srv.weblyzard.net/ws"

class SentimentAnalysis(RESTClient):
    '''
    Sentiment Analysis Web Service
    '''
    def __init__(self, url=SENTIMENT_ANALYSIS_URL, usr=None, pwd=None):
        '''
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        '''
        RESTClient.__init__(self, url, usr, pwd)

    def parse_document(self, text, lang):
        ''' Returns the sentiment of the given text for the given
            language.
            
            :param text: the input text
            :param lang: the text's language
            :returns:
                sv; n_pos_terms; n_neg_terms; list of tuples, where each
                tuple contains two dicts:

                 * tuple[0]: ambiguous terms and its sentiment value after \
                         disambiguation
                 * tuple[1]: the context terms with their number of \
                        occurrences in the document.
        '''
        return self.execute("sentiment_parse_document", 
                            None, { 'text': text, 'lang': lang })
    

    def parse_document_list(self, document_list, lang):
        ''' Returns the sentiment of the given text for the given
            language.
            
            :param document_list: the input text
            :param lang: the text's language
            :returns:
                sv; n_pos_terms; n_neg_terms; list of tuples, where each
                tuple contains two dicts:

                  * tuple[0]: ambiguous terms and its sentiment value after \
                        disambiguation
                  * tuple[1]: the context terms with their number of \
                        occurrences in the document.
        '''
        return self.execute("sentiment_parse_document_list", 
                            None, { 'document_list': document_list, 'lang': lang })
    

    def update_context(self, context_dict, lang):
        ''' Uploads the given context dictionary to the Web service.
                    
            :param context_dict: a dictionary containing the context \
                                 information
            :param lang: the used language
        '''
        return self.execute('sentiment_update_context', None,
                            {'context_dict': context_dict, 'lang': lang} )

        
    def update_lexicon(self, corpus_dict, lang):
        ''' Uploads the given corpus dictionary to the Web service.
                    
            :param corpus_dict: a dictionary containing the corpus information
            :param lang: the used language
        '''
        return self.execute('sentiment_update_lexicon', None,
                            {'corpus_dict': corpus_dict, 'lang': lang })


    def update_negation(self, negation_trigger_dict, lang):
        ''' Uploads the given negation triggers to the Web service.
                    
            :param negation_trigger_list: a list of negation triggers to
                    use with the given language
                    example: ``{'doesn't': 'doesnt', ....}``
            :param lang: the used language
        '''
        return self.execute('sentiment_update_negation', None,
                            {'negation_trigger_dict': negation_trigger_dict, 
                             'lang': lang} )

    def reset(self, lang):
        ''' Restores the default data files for the given language
            (if available).

                   
            :param lang: the used language

            .. note::
                Currently this operation is only supported for German and
                English.
         '''
        return self.execute('sentiment_reset', None,
                            {'lang': lang} )


class SentimentAnalysisTest(TestCase):
    
    TEST_LANG = 'test'
    TEST_CONTEXT = {}
    TEST_LEXICON = {'gut': 1, 'schlecht': -1}
    
    def test_lexica(self):
        sa = self._prepare_sentiment_analysis()
        
        sent, cnt_pos, cnt_neg, _, _ =   sa.parse_document("Schwimmen ist gut fuer die Knochen", self.TEST_LANG)
        self.assertEqual(sent, 1.0)
        self.assertEqual(cnt_pos, 1)
        self.assertEqual(cnt_neg, 0)
        
        sent, cnt_pos, cnt_neg, _, _ =  sa.parse_document("Alkohol trinken ist schlecht.", self.TEST_LANG)
        self.assertEqual(sent, -1.0)
        self.assertEqual(cnt_pos, 0)
        self.assertEqual(cnt_neg, 1)

    def test_document_list(self):
        sa = self._prepare_sentiment_analysis()
        doc_list = ['Schwimmen ist gut fuer die Knochen', 'Jujitsu ist schlecht fuer die Knochen']
        result = sa.parse_document_list( doc_list, self.TEST_LANG )
        print 'list', result
        self.assertEqual(len(result), 2)
         
    def test_negation(self):
        sa = self._prepare_sentiment_analysis()
        sa.update_negation({'nicht':'nicht', 'kein': 'kein'}, self.TEST_LANG)
        print sa.parse_document("Schwimmen ist kein gut fuer die Knochen", self.TEST_LANG)
        sent, cnt_pos, cnt_neg, _, _ =   sa.parse_document("Schwimmen ist nicht gut fuer die Knochen", self.TEST_LANG)
        self.assertEqual(sent, -1.0)
        self.assertEqual(cnt_pos, 1)
        self.assertEqual(cnt_neg, 0)
        
    def test_french(self):
        lang = 'fr'
        # first version
        posDict = {'cristalline': 1, 'in\xc3\xa9galable': 1, 'filmique': 1, 'chaudement': 1, 'somptueuse': 1, 'zen': 1, 'chaleureusement': 1, 'envo\xc3\xaatantes': 1, 'envoutantes': 1, 'formidablement': 1, 'septique': 1, 'id\xc3\xa9ales': 1, 'suffisament': 1, 'uniques': 1, 'f\xc3\xa9\xc3\xa9rique': 1, 'g\xc3\xa9niaux': 1, 'incontournable': 1, 'grace': 1, 'd\xc3\xa9licieusement': 1, 'inou\xc3\xaae': 1, 'spontan\xc3\xa9e': 1, 'naissante': 1, 'r\xc3\xa9active': 1, 'redoutable': 1, 'vari\xc3\xa9e': 1, 'pianistique': 1, 'extraordinairement': 1, 'a\xc3\xa9riens': 1, 'magistrale': 1, 't\xc3\xa9l\xc3\xa9commande': 1, 'recommand\xc3\xa9e': 1, 'qualitatif': 1, 'silencieuse': 1, 'ais\xc3\xa9e': 1, 'horror': 1, 'sophistiqu\xc3\xa9e': 1, '\xc3\xa9mouvant': 1, 'vives': 1, 'hallucinante': 1, '\xc3\xa9patants': 1, 'parfaite': 1, 'ais\xc3\xa9': 1, 'discrets': 1, 'james': 1, '\xc3\xa9poustouflants': 1, 'ambitieuse': 1, 'indiscutable': 1, 'envo\xc3\xaatante': 1, 'superbement': 1, 'intemporel': 1, 'accro': 1, '\xc3\xa9poustouflante': 1, 'marquante': 1, 'in\xc3\xa9dite': 1, 'exceptionnels': 1, 'fameuses': 1, 'multijoueur': 1, 'pleinement': 1, 'rires': 1, 'in\xc3\xa9gal\xc3\xa9e': 1, 'cr\xc3\xa9pusculaire': 1, 'playmobil': 1, 'fabuleuse': 1, 'touchante': 1, 'd\xc3\xa9licates': 1, 'vifs': 1, 'd\xc3\xa9ferlante': 1, 'maitris\xc3\xa9': 1, 'incontournables': 1, 'parfaits': 1, 'ant\xc3\xa9rieures': 1, 'contenu': 1, 'gr\xc3\xaace': 1, 'hostile': 1, 'r\xc3\xa9ducteur': 1, 'tendre': 1, 'inhabituelle': 1, 'rythm\xc3\xa9e': 1, 'explosive': 1, 'tr\xc3\xa9pidante': 1, 'd\xc3\xa9licieux': 1, 'rude': 1, 'subtilement': 1, 'l\xe2\x80\x99': 1, 'londonien': 1, 'n\xc3\xa9gligeable': 1, 'sobres': 1, 'palpitante': 1, 'intens\xc3\xa9ment': 1, 'violoncelle': 1, 'inimitable': 1, 'humaniste': 1, 'admirablement': 1, 'sanglante': 1, 'sublimes': 1, '\xc3\xa9mouvante': 1, 'saisissante': 1, 'colorim\xc3\xa9trique': 1, 'remarquablement': 1, 'parfaites': 1, 'merveilleusement': 1, 'agr\xc3\xa9ablement': 1, 'orientable': 1, 'fluides': 1, 'suffisantes': 1, '>>': 1, 'grandioses': 1, 'satisfaite': 1, 'bouleversante': 1, 'captivants': 1, 'incisif': 1, 'fascinante': 1, 'm\xc3\xa9connue': 1, 'raffin\xc3\xa9e': 1, 'qualit\xc3\xa9-prix': 1, 'fonctionnelle': 1, 'consid\xc3\xa9rable': 1, 'aimable': 1, 'onirique': 1, 'profonds': 1, 'comp\xc3\xa9titif': 1, '\xc3\xa9poustouflant': 1, 'alcoolique': 1, 'imparable': 1, 'film\xc3\xa9': 1, 'irr\xc3\xa9sistiblement': 1, 'communicatif': 1, 'lucide': 1, 'subjective': 1, 'm\xc3\xa9lancolique': 1, 'inestimable': 1, 'with': 1, 'effrayante': 1, 'imbattable': 1, 'assur\xc3\xa9ment': 1, 'poignante': 1, 'hilarants': 1, 'splendide': 1, 'irlandais': 1, 'paradoxal': 1, 'adore': 1, 'mature': 1, 'macro': 1, 'magistral': 1, 'instrumentaux': 1, 'my': 1, 'somptueux': 1, 'envoutante': 1, 'merveilleuses': 1, 'entrainante': 1, 'initiatique': 1, 'have': 1, 'd\xc3\xa9chirante': 1, 'cisel\xc3\xa9s': 1, 'pass\xc3\xa9s': 1, 'polyvalent': 1, 'arm\xc3\xa9': 1, 'physique': 1, 'mythiques': 1, 'ideal': 1, '\xc3\xa9clair\xc3\xa9': 1, 'orchestral': 1, 'encombrement': 1, 'hilarantes': 1, 'ind\xc3\xa9modable': 1, 'fid\xc3\xa8lement': 1, 'sensuel': 1, 'sudiste': 1, 'in\xc3\xa9puisable': 1, 'viens': 1, 'primordial': 1, 'douces': 1, 'embl\xc3\xa9matique': 1, 'prenante': 1, 'cultissime': 1, 'annexes': 1, 'loufoques': 1, 'satisfait': 1, 'silencieux': 1, 'coupees': 1, 'incontest\xc3\xa9': 1, 'light': 1, 'bourrins': 1, 'indiscutablement': 1, '\xc3\xa9pur\xc3\xa9': 1, 'egalement': 1, 'mouvement\xc3\xa9e': 1, 'romanesque': 1, 'machiav\xc3\xa9lique': 1, 'intime': 1, 'stup\xc3\xa9fiante': 1}
        negDict = {'tristement':-1, 'lassant':-1, 'honteuse':-1, 'm\xc3\xa9diocre':-1, 'd\xc3\xa9sesp\xc3\xa9r\xc3\xa9ment':-1, 'ignoble':-1, 'inutilisable':-1, 'grossiers':-1, 'bonjour':-1, 'porno':-1, 'vilains':-1, 'grotesque':-1, 'vide':-1, 'd\xc3\xa9cevant':-1, 'all\xc3\xa9chant':-1, 'fade':-1, 'm\xc3\xa9lodiquement':-1, 'uvre':-1, 'irr\xc3\xa9versible':-1, 's\xc3\xa9v\xc3\xa8rement':-1, '\xc3\xa9claire':-1, 'mou':-1, 'mous':-1, 'path\xc3\xa9tiques':-1, 'ni\xc3\xa8me':-1, 'passable':-1, '\xc3\xa9ventuel':-1, 'risible':-1, 'mauvais':-1, 'sp\xc3\xa9cialis\xc3\xa9e':-1, 'ennuyeuses':-1, 'foireux':-1, 'vainement':-1, 'trompeuse':-1, 'd\xc3\xa9cevante':-1, 'd\xc3\xa9\xc3\xaau':-1, 'rat\xc3\xa9e':-1, 'prometteuse':-1, 'd\xc3\xa9plorable':-1, 'p\xc3\xa9niblement':-1, 'financi\xc3\xa8re':-1, 'nul':-1, 'maigre':-1, 'immonde':-1, 'malheureuse':-1, 'commerciales':-1, 'regardable':-1, 'pale':-1, 'nulles':-1, 'opportuniste':-1, 't\xc3\xa9l\xc3\xa9phon\xc3\xa9':-1, 'ex\xc3\xa9crable':-1, 'incompatible':-1, 'honteux':-1, 'approximatifs':-1, 'horrible':-1, 'affreusement':-1, 'pitoyables':-1, 'creux':-1, 'fran\xc3\xa7aise':-1, '\xc3\xa9coutable':-1, 'pr\xc3\xa9tentieux':-1, 'lamentables':-1, 'terne':-1, 's\xc3\xbbrement':-1, 'sid\xc3\xa9ral':-1, 'moches':-1, 'involontaire':-1, 'anormal':-1, 'mitig\xc3\xa9':-1, 'scandaleux':-1, 'inexistant':-1, 'approximative':-1, 'incultes':-1, 'indigeste':-1, 'royalement':-1, 'insipides':-1, 'pitoyable':-1, 'pr\xc3\xa9visible':-1, 'd\xc3\xa9fectueuse':-1, 'potable':-1, 'interminables':-1, 'transparents':-1, 'bof':-1, 'fran\xc3\xa7ais':-1, 'mouais':-1, 'sois':-1, 'inexistante':-1, 'moche':-1, 'poussive':-1, 'd\xc3\xa9bile':-1, 'ridicules':-1, 'd\xc3\xa9fectueux':-1, 'inadmissible':-1, 'alimentaire':-1, 'incompl\xc3\xa8te':-1, 'logiciel':-1, 'lamentable':-1, 'al\xc3\xa9atoire':-1, 'm\xc3\xa9diocres':-1, 'bidon':-1, 'illisible':-1, 'mi\xc3\xa8vre':-1, '\xc3\xa7\xc3\xa0':-1, 'superficiels':-1, 'r\xc3\xa9dhibitoire':-1, 'mauvaise':-1, 'd\xc3\xa9cu':-1, 'pr\xc3\xa9tentieuse':-1, 'ennuyeux':-1, 'pompeuse':-1, 'mortellement':-1, 'superficiel':-1, 'd\xc3\xa9goulinant':-1, 'fades':-1, 'inexistantes':-1, 'pire':-1, 'd\xc3\xa9sastreuse':-1, 'dithyrambiques':-1, 'ais':-1, 'bancal':-1, 'adaptateur':-1, 'all\xc3\xa9chante':-1, 'b\xc3\xaatement':-1, 'impossibles':-1, 'nuls':-1, 'vulgaires':-1, 'ah':-1, 'gnan-gnan':-1, 'naze':-1, 'n\xc3\xa9erlandais':-1, 'd\xc3\xa9sagr\xc3\xa9able':-1, 'cruellement':-1, 'de\xc3\xaau':-1, 'passablement':-1, 'mediocre':-1, 'dispensable':-1, 'poussif':-1, 'douteuse':-1, 'cens\xc3\xa9':-1, 'niais':-1, 's\xc3\xbbr':-1, 'illisibles':-1, 'd\xc3\xa9cue':-1, '\xc3\xa9logieuses':-1, 'faiblardes':-1, 'psychopathe':-1, 'plates':-1, 'catastrophique':-1, 'pires':-1, 'inutilisables':-1, 'laide':-1, 'insupportable':-1, 'molles':-1, 'minable':-1, 'insipide':-1, 'soporifique':-1, 'dr\xc3\xb4le':-1, 'insupportables':-1, 'laids':-1, 'grotesques':-1, 'intrins\xc3\xa8que':-1, 'risibles':-1, 'tordu':-1, 'plut\xc3\xb4t':-1, 'd\xc3\xa9\xc3\xaaue':-1, 'archi':-1, 'd\xc3\xa9biles':-1, 'confus':-1, 'affligeante':-1, 'stupide':-1, 'decevant':-1, 'compar\xc3\xa9s':-1, 'mortel':-1, 'inint\xc3\xa9ressant':-1}
        # intellectually reviewed version 2013-02-20
        posDict = {'incontest\xc3\xa9e': 1, 'satisfaits': 1, 'd\xc3\xa9chirantes': 1, 'fascinants': 1, 'grandioses': 1, 'chaudement': 1, 'comp\xc3\xa9titives': 1, 'somptueuses': 1, 'captivantes': 1, 'ais\xc3\xa9e': 1, 'captivants': 1, 'chaleureusement': 1, 'hallucinante': 1, 'fascinante': 1, 'formidablement': 1, 'd\xc3\xa9chirant': 1, 'in\xc3\xa9gal\xc3\xa9': 1, 'captivante': 1, 'qualitatives': 1, 'parfaits': 1, 'raffin\xc3\xa9e': 1, 'palpitant': 1, 'fascinantes': 1, 'aimables': 1, 'uniques': 1, '\xc3\xa9poustouflants': 1, 'g\xc3\xa9niaux': 1, 'recommand\xc3\xa9e': 1, 'fonctionnelle': 1, 'satisfaites': 1, 'id\xc3\xa9ale': 1, 'sophistiqu\xc3\xa9s': 1, 'd\xc3\xa9licieusement': 1, 'envo\xc3\xbbtantes': 1, 'somptueuse': 1, 'aimable': 1, 'suffisante': 1, 'fascinant': 1, 'magistraux': 1, 'comp\xc3\xa9titif': 1, '\xc3\xa9poustouflant': 1, 'extraordinairement': 1, 'fabuleux': 1, 'magistrale': 1, 'd\xc3\xa9licate': 1, 'discr\xc3\xa8te': 1, 'ambitieux': 1, 'irr\xc3\xa9sistiblement': 1, '\xc3\xa9patante': 1, 'sophistiqu\xc3\xa9e': 1, 'qualitatifs': 1, 'hallucinants': 1, 'fabuleuses': 1, 'suffisantes': 1, 'imparable': 1, 'recommand\xc3\xa9es': 1, 'd\xc3\xa9licats': 1, 'exceptionnel': 1, 'fonctionnel': 1, 'inestimable': 1, 'unique': 1, '\xc3\xa9patants': 1, 'cristallin': 1, 'd\xc3\xa9licieux': 1, 'imbattable': 1, 'ais\xc3\xa9': 1, 'palpitantes': 1, '\xc3\xa9patantes': 1, 'discrets': 1, 'qualitative': 1, 'splendide': 1, 'ambitieuse': 1, 'fonctionnels': 1, 'in\xc3\xa9galable': 1, 'cristallins': 1, 'hallucinant': 1, 'remarquablement': 1, 'captivant': 1, 'magistral': 1, '\xc3\xa9poustouflantes': 1, 'raffin\xc3\xa9es': 1, 'merveilleux': 1, 'sublime': 1, 'd\xc3\xa9chirants': 1, 'exceptionnels': 1, 'somptueux': 1, 'fameux': 1, 'envo\xc3\xbbtants': 1, 'merveilleuses': 1, 'g\xc3\xa9niale': 1, 'pleinement': 1, 'id\xc3\xa9al': 1, 'sophistiqu\xc3\xa9es': 1, 'fonctionnelles': 1, 'envo\xc3\xbbtante': 1, 'sophistiqu\xc3\xa9': 1, 'in\xc3\xa9gal\xc3\xa9e': 1, 'd\xc3\xa9chirante': 1, 'd\xc3\xa9licieuses': 1, 'fabuleuse': 1, 'cristallines': 1, 'd\xc3\xa9licates': 1, 'grandiose': 1, 'saisissant': 1, 'magistrales': 1, 'id\xc3\xa9aux': 1, 'raffin\xc3\xa9s': 1, 'cristalline': 1, 'comp\xc3\xa9titifs': 1, 'saisissants': 1, 'raffin\xc3\xa9': 1, 'recommand\xc3\xa9s': 1, 'suffisants': 1, 'stup\xc3\xa9fiantes': 1, 'discret': 1, 'suffisament': 1, 'qualitatif': 1, 'fameuse': 1, 'parfaite': 1, 'envo\xc3\xbbtant': 1, 'd\xc3\xa9licieuse': 1, 'comp\xc3\xa9titive': 1, 'hallucinantes': 1, 'superbement': 1, 'id\xc3\xa9ales': 1, 'fameuses': 1, 'fid\xc3\xa8lement': 1, 'exceptionnelles': 1, 'd\xc3\xa9licat': 1, 'palpitants': 1, 'subtilement': 1, 'ambitieuses': 1, 'sublimes': 1, 'palpitante': 1, 'intens\xc3\xa9ment': 1, 'g\xc3\xa9niales': 1, 'satisfaite': 1, 'discr\xc3\xa8tes': 1, 'parfait': 1, 'exceptionnelle': 1, 'admirablement': 1, 'merveilleuse': 1, 'splendides': 1, 'satisfait': 1, 'saisissante': 1, 'incontest\xc3\xa9': 1, '\xc3\xa9poustouflante': 1, '\xc3\xa9patant': 1, 'stup\xc3\xa9fiants': 1, 'g\xc3\xa9nial': 1, 'saisissantes': 1, 'stup\xc3\xa9fiant': 1, 'stup\xc3\xa9fiante': 1, 'suffisant': 1, 'merveilleusement': 1, 'agr\xc3\xa9ablement': 1, 'lucide': 1, 'parfaites': 1, 'recommand\xc3\xa9': 1}
        negDict = {'grossier': -1, 'grotesques': -1, 'inexistante': -1, 'honteuse': -1, 'confuse': -1, 'd\xc3\xa9bile': -1, 'ignoble': -1, 'lassantes': -1, 'foireuses': -1, 'inutilisable': -1, 'scandaleuses': -1, 'nul': -1, 'bancale': -1, 'nuls': -1, 'trompeuse': -1, 'incompl\xc3\xa8tes': -1, 'd\xc3\xa9fectueux': -1, 'catastrophiques': -1, 'inadmissible': -1, 'd\xc3\xa9plorables': -1, 'incompl\xc3\xa8te': -1, 'grotesque': -1, 'lamentable': -1, 'd\xc3\xa9cevant': -1, 'douteux': -1, 'rat\xc3\xa9es': -1, 'fade': -1, 'moches': -1, 'inint\xc3\xa9ressantes': -1, 'superficiels': -1, 'irr\xc3\xa9versible': -1, 'moche': -1, 'm\xc3\xa9diocres': -1, 'malheureuse': -1, 'anormaux': -1, 'm\xc3\xa9diocre': -1, 'lassant': -1, 'mauvaise': -1, 'd\xc3\xa9sesp\xc3\xa9r\xc3\xa9ment': -1, 'pr\xc3\xa9tentieuse': -1, 'd\xc3\xa9cevantes': -1, 'niaise': -1, 'p\xc3\xa9niblement': -1, 'ennuyeux': -1, 'lassants': -1, 'interminable': -1, 'grossiers': -1, 'fades': -1, 'inexistantes': -1, 'ignobles': -1, 'stupide': -1, 'risible': -1, 'mauvais': -1, 'pr\xc3\xa9tentieuses': -1, 'pire': -1, 'd\xc3\xa9sastreuse': -1, 'd\xc3\xa9sagr\xc3\xa9able': -1, 'bancal': -1, 'ennuyeuses': -1, 'ridicules': -1, 'superficiel': -1, 'mauvaises': -1, 'superficielles': -1, 'b\xc3\xaatement': -1, 'incompatible': -1, 'rat\xc3\xa9': -1, 'ex\xc3\xa9crables': -1, 'vainement': -1, 'stupides': -1, 'inadmissibles': -1, 'impossibles': -1, 'lassante': -1, 'd\xc3\xa9cevante': -1, 'horribles': -1, 'immondes': -1, 'decevantes': -1, 'inexistants': -1, 'd\xc3\xa9plorable': -1, 'grossi\xc3\xa8res': -1, 'decevants': -1, 'grossi\xc3\xa8re': -1, 'lamentables': -1, 'd\xc3\xa9cevants': -1, 'inutilisables': -1, 'cruellement': -1, 'immonde': -1, 'impossible': -1, 'decevante': -1, 'douteuse': -1, 'scandaleuse': -1, 'affligeant': -1, 'rat\xc3\xa9s': -1, 'rat\xc3\xa9e': -1, 'insupportables': -1, 'niais': -1, 'ex\xc3\xa9crable': -1, 'faiblarde': -1, 'inculte': -1, 'd\xc3\xa9cue': -1, 'inint\xc3\xa9ressants': -1, 'honteux': -1, 'd\xc3\xa9cu': -1, 'faiblards': -1, 'honteuses': -1, 'horrible': -1, 'tristement': -1, 'inint\xc3\xa9ressante': -1, 'catastrophique': -1, 'pires': -1, 'incompatibles': -1, 'anormale': -1, 'minable': -1, 'pitoyables': -1, 'insupportable': -1, 'nulle': -1, 'affreusement': -1, 'insipide': -1, 'irr\xc3\xa9versibles': -1, 'faiblard': -1, 'insipides': -1, 'pr\xc3\xa9tentieux': -1, 'd\xc3\xa9sastreux': -1, 'foireux': -1, 'minables': -1, 'r\xc3\xa9dhibitoire': -1, 'risibles': -1, 'incomplet': -1, 'affligeantes': -1, 'd\xc3\xa9sagr\xc3\xa9ables': -1, 'anormales': -1, 'anormal': -1, 'd\xc3\xa9biles': -1, 'superficielle': -1, 'incomplets': -1, 'interminables': -1, 'scandaleux': -1, 'affligeante': -1, 'inexistant': -1, 'nulles': -1, 'incultes': -1, 'foireuse': -1, 'faiblardes': -1, 'decevant': -1, 'inint\xc3\xa9ressant': -1, 'pitoyable': -1, 'ridicule': -1, 'd\xc3\xa9fectueuse': -1, 'confus': -1, 'affligeants': -1, 'bof': -1}

        frDict = dict(posDict.items() + negDict.items())
        #frDict = {'cristalline': 1, 'tristement':-1}
        print lang, 'lexicon size:', len(frDict)
        negations = {'ne':'ne', 'n\'':'n\''}
    
        frsa = SentimentAnalysis()
        print 'update lexicon', frsa.update_lexicon(frDict, lang)
        print 'update negations', frsa.update_negation(negations, lang)
        text = "Il est cristalline et septique. Mais pas tristement"
        #text = "Schwimmen ist nicht gut fuer die Knochen"
        #text = "Schwimmen ist cristalline fuer die Knochen"
        #text = "Il est gut abc"
        #result =  frsa.parse_document("Schwimmen ist nicht gut fuer die Knochen", self.TEST_LANG)
        result =  frsa.parse_document(text, lang)
        print 'french:', result
        
        # pos
        sent, cnt_pos, cnt_neg, _, _ =  frsa.parse_document('C\'est aimable', 'fr')
        self.assertEqual(sent, 1.0)
        self.assertEqual(cnt_pos, 1)
        self.assertEqual(cnt_neg, 0)

        # neg
        sent, cnt_pos, cnt_neg, _, _ =  frsa.parse_document('C\'est affligeant', 'fr')
        self.assertEqual(sent, -1.0)
        self.assertEqual(cnt_pos, 0)
        self.assertEqual(cnt_neg, 1)
        
        # pos negation, fails?
        # TODO: negate not only first word after negation

        sent, cnt_pos, cnt_neg, _, _ =  frsa.parse_document('Ce n\'est pas aimable', 'fr')
        sent, cnt_pos, cnt_neg, _, _ =  frsa.parse_document('Ce ne aimable', 'fr')        
        print "pos negation", sent, cnt_pos, cnt_neg
        self.assertEqual(sent, -1.0)
        self.assertEqual(cnt_pos, 1)
        self.assertEqual(cnt_neg, 0)
        '''

        # neg negation
        sent, cnt_pos, cnt_neg, _, _ =  frsa.parse_document('Ce n\'est pas affligeant', 'fr')
        self.assertEqual(sent, 1.0)
        self.assertEqual(cnt_pos, 1)
        self.assertEqual(cnt_neg, 0)
        '''
        
        
    
    def _prepare_sentiment_analysis(self):
        ''' prepares the sentiment analysis object and uploads the
            language resources.
        '''
        sa = SentimentAnalysis()
        sa.update_context(self.TEST_CONTEXT, self.TEST_LANG)
        sa.update_lexicon(self.TEST_LEXICON, self.TEST_LANG)
        sa.update_negation({}, self.TEST_LANG)
        return sa

    def test_reset_lang(self):
        sa = SentimentAnalysis()
        sa.reset('de')
        sa.reset('en')

    def test_custom_lexicon_fench(self):
        sa = SentimentAnalysis()
        sa.update_context({}, 'fr')
        sa.update_lexicon({'bueno': 1., 'merci': 1., 'mal': -1.}, 'fr')
        sa.update_negation( {'no':'no', 'ne':'ne'}, 'fr' )
        sent, cnt_pos, cnt_neg, _, _ =  sa.parse_document('Es uno bueno momento.', 'fr')
        self.assertEqual(sent, 1.0)
        self.assertEqual(cnt_pos, 1)
        self.assertEqual(cnt_neg, 0)


if __name__ == '__main__':
    main()
