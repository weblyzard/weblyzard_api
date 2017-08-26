package com.weblyzard.api.document.serialize;

import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonToken;
import com.weblyzard.api.model.document.Document;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import javax.xml.bind.JAXBException;
import lombok.extern.slf4j.Slf4j;

/**
 * Reads documents from a JSON array of weblyzard XML documents.
 *
 * @author Albert Weichselbraun
 */
@Slf4j
public class DocumentInputStreamParser {

    // global helpers for json parsing
    private static final JsonFactory jsonFactory = new JsonFactory();

    /**
     * parses an input stream to a list of documents
     *
     * @param stream the input stream to parse
     * @return the parsed document list
     */
    public static List<Document> readDocumentFromStream(InputStream stream) throws JAXBException {
        List<Document> documentList = new ArrayList<>();
        try (JsonParser jp = jsonFactory.createParser(stream)) {
            jp.nextToken();
            Document d = Document.unmarshallDocumentXmlString(jp.getValueAsString());
            if (d != null) {
                documentList.add(d);
            }

            jp.nextToken();
            log.info("Read {} document from input stream", documentList.size());
            return documentList;

        } catch (IOException e) {
            log.warn("Cannot read documents: {}", e);
            return Collections.emptyList();
        }
    }

    /**
     * parses an input stream to a list of documents
     *
     * @param stream the input stream to parse
     * @return the parsed document list
     */
    public static List<Document> readDocumentsFromStream(InputStream stream) throws JAXBException {
        List<Document> documentList = new ArrayList<>();
        try (JsonParser jp = jsonFactory.createParser(stream)) {
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
            log.info("Read {} document from input stream", documentList.size());
            return documentList;

        } catch (IOException e) {
            log.warn("Cannot read documents: {}", e);
            return Collections.emptyList();
        }
    }
}
