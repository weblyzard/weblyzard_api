package com.weblyzard.api.client.integration;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.junit.Assume.assumeTrue;
import java.io.File;
import java.io.IOException;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import javax.xml.bind.JAXBException;
import org.junit.Before;
import org.junit.Test;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.weblyzard.api.client.RecognyzeClient;
import com.weblyzard.api.model.annotation.Annotation;
import com.weblyzard.api.model.document.Document;

public class RecognyzeClientIT extends TestClientBase {


    private static final ObjectMapper objectMapper = new ObjectMapper();
    private static final String profile = "JOBCOCKPIT";

    private static final String PSALMS_DOCS_WEBLYZARDFORMAT =
            "resources/reference/weblyzard-example.json";

    private static Document loadDocument() throws JAXBException, IOException {
        return objectMapper.readValue(new File(PSALMS_DOCS_WEBLYZARDFORMAT), Document.class);
    }

    private RecognyzeClient recognizeClient;

    @Before
    public void testLoadProfile() {
        recognizeClient = new RecognyzeClient();
        assumeTrue(weblyzardServiceAvailable(recognizeClient));
        boolean profileLoaded = recognizeClient.loadProfile(profile);
        assumeTrue(profileLoaded);
    }

    @Test
    public void testSearchDocument() throws JAXBException, IOException {
        assumeTrue(weblyzardServiceAvailable(recognizeClient));

        Document request = loadDocument();

        List<Annotation> result = recognizeClient.searchDocument(profile, request).getAnnotations();
        // TODO: validate that the resultset is not empty (compose a small test
        // profile, find a nice sentence to test)
        assertNotNull(result);
        assertTrue(result.size() >= 1);
    }

    @Test
    public void testSearchDocuments() throws JAXBException, IOException {
        assumeTrue(weblyzardServiceAvailable(recognizeClient));
        Set<Document> request = new HashSet<>();
        Document document = loadDocument();
        document.setId("1");
        request.add(document);
        List<Document> result = recognizeClient.searchDocuments(profile, request);
        // TODO: validate that the resultset is not empty (compose a small test
        // profile, find a nice sentence to test)
        assertNotNull(result);
        assertTrue(result.size() >= 1);
    }

    @Test
    public void testSearchDocumentsWithoutId() throws JAXBException, IOException {
        assumeTrue(weblyzardServiceAvailable(recognizeClient));
        Set<Document> request = new HashSet<>();
        request.add(loadDocument());

        List<Document> result = recognizeClient.searchDocuments(profile, request);
        // TODO: validate that the resultset is not empty (compose a small test
        // profile, find a nice sentence to test)
        assertNotNull(result);
        assertTrue(result.size() > 0);
    }

    @Test
    public void testStatus() {
        assumeTrue(weblyzardServiceAvailable(recognizeClient));
        Map<String, Object> result = recognizeClient.status();
        // TODO: validate that the resultset is not empty (compose a small test
        // profile, find a nice sentence to test)
        assertNotNull(result);
    }
}
