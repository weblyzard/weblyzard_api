package com.weblyzard.api.document.serialize;


import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.logging.Logger;

import javax.xml.bind.JAXBException;

import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonToken;
import com.weblyzard.api.document.Document;

/**
 * Reads documents from a json array of weblyzard XML documents.
 * @author albert
 *
 */
public class DocumentInputStreamParser {
	
	public final static Logger logger = Logger.getLogger(DocumentInputStreamParser.class.getCanonicalName());
	
	// global helpers for json parsing
	private final static JsonFactory jsonFactory = new JsonFactory();

	/**
	 * parses an input stream to a list of documents
	 * 
	 * @param stream
	 *            the input stream to parse
	 * @return 
	 * 	the parsed document list
	 */
	public static List<Document> readDocumentFromStream(InputStream stream) throws JAXBException {
		List<Document> documentList = new ArrayList<>();
		JsonParser jp;
		try {
			jp = jsonFactory.createParser(stream);
			jp.nextToken();
			Document d = Document.unmarshallDocumentXmlString(jp.getValueAsString());
			if (d != null) {
				documentList.add(d);
			}

			jp.nextToken();
			logger.info(String.format("Read %d document from input stream", documentList.size()));
			return documentList;

		} catch (IOException e) {
			logger.warning(String.format("Cannot read documents - %s", e));
			return Collections.emptyList();
		} 
	}
	
	/**
	 * parses an input stream to a list of documents
	 * 
	 * @param stream
	 *            the input stream to parse
	 * @return 
	 * 	the parsed document list
	 */
	public static List<Document> readDocumentsFromStream(InputStream stream) throws JAXBException {
		List<Document> documentList = new ArrayList<>();
		JsonParser jp;
		try {
			jp = jsonFactory.createParser(stream);
			// read START_ARRAY
			jp.nextToken();
			while (jp.nextToken() == JsonToken.VALUE_STRING) {
				Document d = Document.unmarshallDocumentXmlString(jp.getValueAsString());
				if (d != null) {
					documentList.add(d);
				}
			}
			// read STOP_ARRAY
			jp.nextToken();
			logger.info(String.format("Read %d document from input stream", documentList.size()));
			return documentList;

		} catch (IOException e) {
			logger.warning(String.format("Cannot read documents - %s", e));
			return Collections.emptyList();
		} 
	}
}
