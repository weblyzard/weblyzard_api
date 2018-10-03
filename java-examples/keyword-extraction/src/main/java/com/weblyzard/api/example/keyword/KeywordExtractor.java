package com.weblyzard.api.example.keyword;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.xml.bind.JAXBException;

import com.google.devtools.common.options.OptionsParser;
import com.weblyzard.api.client.JeremiaClient;
import com.weblyzard.api.client.JesajaClient;
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
	
	private static KeywordCalculationProfile KEYWORD_PROFILE = new KeywordCalculationProfile()
			.setValidPosTags(Set.of("NN", "NNP", "P", "ADJ", "TO", "IN"))
			.setMinPhraseSignificance(2)
			.setNumKeywords(15)
			.setKeywordAlgorithm("com.weblyzard.backend.jesaja.algorithm.keywords.YatesKeywordSignificanceAlgorithm")
			.setMinTokenCount(5)
			.setSkipUnderrepresentedKeywords(true);
	
	public static void main(String[] argv) {
		OptionsParser parser = OptionsParser.newOptionsParser(KeywordExtractorOption.class);
		parser.parseAndExitUponError(argv);
		KeywordExtractorOption options = parser.getOptions(KeywordExtractorOption.class);
		System.out.println("Arguments   : " + Arrays.toString(argv));
		System.out.println("Base URL    : " + options.webServiceBaseUrl);
		System.out.println("Profile name: " + options.profileName);
		
		if (options.printHelp || options.webServiceBaseUrl.isEmpty() || options.profileName.isEmpty()) {
			printUsage(parser);
			return;
		}
		
		// setup keyword service
		keywordExtractionClient.setKeywordProfile(options.profileName, KEYWORD_PROFILE);
		keywordExtractionClient.setMatviewProfile(options.profileName, options.profileName);
		
		// train the component with the provided reference corpus
		if (!options.referenceCorpusDirectory.isEmpty()) {
			List<Document> documents = getDocuments(options.referenceCorpusDirectory);
			trainJesaja(options.profileName, documents);
		}
		
		// compute keywords
		if (!options.targetCorpusDirectory.isEmpty()) {
			List<Document> documents = getDocuments(options.targetCorpusDirectory);
			try {
				Map<String, Map<String, Double>> keywords = keywordExtractionClient.getKeywords(options.profileName, documents);
				System.out.println(Entity.json(keywords));
			} catch (WebApplicationException | JAXBException e) {
				log.error("Cannot extract keywords: {}", e);
				System.exit(-1);
			}
		}
		
	}
	
	private static void trainJesaja(String profileName, List<Document> documents) {
		try {
			while (keywordExtractionClient.rotateShard(profileName) == 0) {
				keywordExtractionClient.addDocuments(profileName, documents);
			}
		} catch (WebApplicationException | JAXBException e) {
			log.error("Cannot train keyword service: {}", e);
			System.exit(-1);
		}
	}
	

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
	 * @return a list of Document objects 
	 */
	private static List<Document> getDocuments(Stream<Path> documents) {
		List<MirrorDocument> inputDocuments = documents.map(documentPath  -> 
			{
				try {
					return new MirrorDocument().setId(documentPath.toString()).setBody(new String(Files.readAllBytes(documentPath)));
				} catch (IOException e) {
					log.warn("Cannot open input document '{}': {}", documentPath, e);
					return null;
				}
			}
		).filter(document -> document != null).collect(Collectors.toList());
		
		// create the input structure for the pre-processing web service
		return preProcessingClient.submitDocuments(inputDocuments);
	}
	
	

	/** provide usage information */
	private static void printUsage(OptionsParser parser) {
		System.out.println("Usage: java -jar example-keyword-extractor OPTIONS");
		System.out.println(parser.describeOptions(Collections.emptyMap(), OptionsParser.HelpVerbosity.LONG));
	}
	
}
