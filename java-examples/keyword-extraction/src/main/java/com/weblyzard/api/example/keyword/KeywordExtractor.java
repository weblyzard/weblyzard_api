package com.weblyzard.api.example.keyword;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import javax.ws.rs.WebApplicationException;
import javax.xml.bind.JAXBException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.google.common.collect.ImmutableMap;
import com.google.common.collect.Lists;
import com.google.devtools.common.options.OptionsParser;
import com.weblyzard.api.client.JeremiaClient;
import com.weblyzard.api.client.JesajaClient;
import com.weblyzard.api.client.WebserviceClientConfig;
import com.weblyzard.api.model.Lang;
import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.model.document.MirrorDocument;
import com.weblyzard.api.model.jesaja.KeywordCalculationProfile;
import lombok.extern.slf4j.Slf4j;

@Slf4j
/**
 * An Example keyword extractor client
 *
 * @author Albert Weichselbraun
 *
 */
public class KeywordExtractor {

    private static JeremiaClient preProcessingClient;
    private static JesajaClient keywordExtractionClient;

    private static final ObjectMapper OBJECT_MAPPER =
            new ObjectMapper().enable(SerializationFeature.INDENT_OUTPUT);

    private static KeywordCalculationProfile KEYWORD_PROFILE = new KeywordCalculationProfile()
            .setMinPhraseSignificance(2).setNumKeywords(15)
            .setPosGrammarGroupMapping(ImmutableMap.<String, String>builder().put("ADJA", "adj")
                    .put("ADJD", "adj").put("ADV", "adv").put("APPR", "prep").put("APPRART", "prep")
                    .put("APPO", "prep").put("APZR", "prep").put("ART", "art").put("FM", "noun")
                    .put("NE", "noun").put("NN", "noun").put("XY", "noun").build())
            .setKeywordAlgorithm(
                    "com.weblyzard.backend.jesaja.algorithm.keywords.YatesKeywordSignificanceAlgorithm")
            .setMinTokenCount(5).setSkipUnderrepresentedKeywords(true);

    private static Lang documentLanguage;

    public static void main(String[] argv) throws IOException, JAXBException {
        OptionsParser parser = OptionsParser.newOptionsParser(KeywordExtractorOption.class);
        parser.parseAndExitUponError(argv);
        KeywordExtractorOption options = parser.getOptions(KeywordExtractorOption.class);

        if (options.printHelp || options.webServiceBaseUrl.isEmpty()
                || options.profileName.isEmpty()) {
            printUsage(parser);
            return;
        }

        // number of keywords to extract
        KEYWORD_PROFILE.setNumKeywords(Integer.parseInt(options.numKeywords));

        // determine the valid pos tags
        List<String> validGrammarGroupPatterns =
                Lists.newArrayList(options.validGrammarGroupPatterns.split(","));
        KEYWORD_PROFILE.setValidGrammarGroupPatterns(validGrammarGroupPatterns);

        // set document language, if available
        documentLanguage = Lang.getLanguage(options.documentLanguage).orElse(null);

        // setup web services
        setupWebServices(options);

        // train the component with the provided reference corpus
        if (!options.referenceCorpusDirectory.isEmpty()) {
            List<Document> documents = getDocuments(options.referenceCorpusDirectory);
            if (!options.debugJeremiaDocumentFile.isEmpty()) {
                File jeremiaDocuments = new File(options.debugJeremiaDocumentFile);
                OBJECT_MAPPER.writeValue(jeremiaDocuments, documents);
            }
            trainJesaja(options.profileName, documents);
        }

        // compute keywords
        if (!options.targetCorpusDirectory.isEmpty()) {
            List<Document> documents = getDocuments(options.targetCorpusDirectory);
            if (!options.documentLanguage.isEmpty()) {
                documents.forEach(d -> d.setLang(documentLanguage));
            }
            try {
                Map<String, Map<String, Double>> keywords =
                        keywordExtractionClient.getKeywords(options.profileName, documents);
                System.out.println(OBJECT_MAPPER.writeValueAsString(keywords));
            } catch (WebApplicationException e) {
                log.error("Cannot extract keywords: {}", e);
                System.exit(-1);
            }
        }

    }

    /**
     * Setup and configure the Web services based on the provided {@link KeywordExtractorOption}s.
     * 
     * @param options used for the Web service configuration
     */
    private static void setupWebServices(KeywordExtractorOption options) {
        WebserviceClientConfig jeremiaConfig = new WebserviceClientConfig()
                .setUrl(options.webServiceBaseUrl).setUsername(options.webServiceUserName)
                .setPassword(options.webServiceUserPassword)
                .setUseCompression(Boolean.getBoolean(options.useCompression));
        WebserviceClientConfig jesajaConfig = new WebserviceClientConfig()
                .setUrl(options.webServiceBaseUrl).setUsername(options.webServiceUserName)
                .setPassword(options.webServiceUserPassword)
                .setUseCompression(Boolean.getBoolean(options.useCompression));
        System.out.println(jeremiaConfig);
        // use standard service ports, if the web service has been deployed locally
        if (options.webServiceBaseUrl.startsWith("http://localhost")
                || options.webServiceBaseUrl.startsWith("http://127.0.0.1")) {
            jeremiaConfig.setServicePrefix(":63001");
            jesajaConfig.setServicePrefix(":63002");
        }

        preProcessingClient = new JeremiaClient(jeremiaConfig);
        keywordExtractionClient = new JesajaClient(jesajaConfig);

        // setup keyword service configuration
        keywordExtractionClient.setKeywordProfile(options.profileName, KEYWORD_PROFILE);
        keywordExtractionClient.setMatviewProfile(options.profileName, options.profileName);
    }

    /**
     * Train the keyword extraction service with the documents provided in the reference corpus.
     * 
     * @param profileName the name of the profile to train
     * @param documents the {@link Document}s used for training
     */
    private static void trainJesaja(String profileName, List<Document> documents) {
        try {
            log.warn("Training with {} documents", documents.size());
            while (keywordExtractionClient.rotateShard(profileName) == 0) {
                keywordExtractionClient.addDocuments(profileName, documents);
            }
        } catch (WebApplicationException e) {
            log.error("Cannot train keyword service: {}", e);
            System.exit(-1);
        }
    }

    /**
     * Read all documents from the given directory, perform pre-processing and convert them into a
     * list. of {@link Document} objects.
     * 
     * @param documentDirectory the directory containing the documents
     * @return the list of {@link Document} objects read from the directory
     */
    private static List<Document> getDocuments(String documentDirectory) {
        try {
            return getDocuments(Files.list(Paths.get(documentDirectory)));
        } catch (IOException e) {
            log.error("Cannot open corpus directory '{}': {}", documentDirectory, e);
            System.exit(-1);
        }
        return null;
    }

    /**
     * Returns a list of Document objects.
     */
    private static List<Document> getDocuments(Stream<Path> documents) {
        List<MirrorDocument> inputDocuments = documents.map(documentPath -> {
            try {
                return new MirrorDocument().setId(documentPath.toString()).setLang(documentLanguage)
                        .setBody(new String(Files.readAllBytes(documentPath)));
            } catch (IOException e) {
                log.warn("Cannot open input document '{}': {}", documentPath, e);
                return null;
            }
        }).filter(document -> document != null).collect(Collectors.toList());

        // create the input structure for the pre-processing web service
        return preProcessingClient.submitDocuments(inputDocuments, "-1");
    }

    /**
     * Provide usage information for the given {@link OptionsParser}.
     */
    private static void printUsage(OptionsParser parser) {
        System.out.println("Usage: java -jar example-keyword-extractor OPTIONS");
        System.out.println(
                parser.describeOptions(Collections.emptyMap(), OptionsParser.HelpVerbosity.LONG));
    }

}
