package com.weblyzard.api.client;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.junit.Assume.assumeTrue;

import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.recognyze.RecognyzeResult;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import org.junit.Before;
import org.junit.Test;

public class RecognyzeClientTest extends TestClientBase {

    private static final String profile = "graphfullen2";

    private RecognyzeClient recognizeClient;

    @Before
    public void testLoadProfile() {
        recognizeClient = new RecognyzeClient();
        assumeTrue(weblyzardServiceAvailable(recognizeClient));
        boolean profileLoaded = recognizeClient.loadProfile(profile);
        assumeTrue(profileLoaded);
    }

    @Test
    public void testText() {
        assumeTrue(weblyzardServiceAvailable(recognizeClient));
        String request =
                "Fast Track's Karen Bowerman asks what the changes in penguin"
                        + " population could mean for the rest of us in the event of climate change.";

        Set<RecognyzeResult> result = recognizeClient.searchText(profile, request);

        // TODO: validate that the resultset is not empty (compose a small test
        // profile, find a nice sentence to test)
        assertNotNull(result);
        assertTrue(result.size() >= 1);
    }

    @Test
    public void testSearchDocument() {
        assumeTrue(weblyzardServiceAvailable(recognizeClient));
        Document request =
                new Document(
                        "Fast Track's Karen Bowerman asks what the changes in penguin population"
                                + " could mean for the rest of us in the event of climate change.");

        Set<RecognyzeResult> result = recognizeClient.searchDocument(profile, request);
        // TODO: validate that the resultset is not empty (compose a small test
        // profile, find a nice sentence to test)
        assertNotNull(result);
        assertTrue(result.size() >= 1);
    }

    @Test
    public void testSearchDocuments() {
        assumeTrue(weblyzardServiceAvailable(recognizeClient));
        Set<Document> request = new HashSet<>();
        Document document =
                new Document(
                        "Fast Track's Karen Bowerman asks what the changes in penguin population"
                                + " could mean for the rest of us in the event of climate change.");
        document.setId("1");
        request.add(document);
        Map<String, Set<RecognyzeResult>> result =
                recognizeClient.searchDocuments(profile, request);
        // TODO: validate that the resultset is not empty (compose a small test
        // profile, find a nice sentence to test)
        assertNotNull(result);
        assertTrue(result.size() >= 1);
        assertTrue(result.get("1").size() >= 1);
    }

    @Test
    public void testSearchDocumentsWithoutId() {
        assumeTrue(weblyzardServiceAvailable(recognizeClient));
        Set<Document> request = new HashSet<>();
        request.add(
                new Document(
                        "Fast Track's Karen Bowerman asks what the changes in penguin population"
                                + " could mean for the rest of us in the event of climate change."));

        Map<String, Set<RecognyzeResult>> result =
                recognizeClient.searchDocuments(profile, request);
        // TODO: validate that the resultset is not empty (compose a small test
        // profile, find a nice sentence to test)
        assertNotNull(result);
        assertTrue(result.size() == 0);
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
