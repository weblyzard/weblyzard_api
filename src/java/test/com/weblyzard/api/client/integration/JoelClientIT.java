package com.weblyzard.api.client.integration;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import javax.ws.rs.ClientErrorException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.weblyzard.api.client.JoelClient;
import com.weblyzard.api.client.WebserviceClientConfig;
import com.weblyzard.api.model.document.LegacyDocument;
import com.weblyzard.api.model.document.Sentence;
import com.weblyzard.api.model.joel.ClusterResult;

/** @author norman.suesstrunk@htwchur.ch */
public class JoelClientIT extends TestClientBase {

    private static final String PSALMS_DOCS_WEBLYZARDFORMAT_JSON =
            "resources/psalms-docs-weblyzardformat.json";

    public List<LegacyDocument> psalmDocs;

    private JoelClient joelClient;

    @BeforeEach
    public void before() {
        psalmDocs = readWeblyzardDocuments();
        joelClient = new JoelClient(new WebserviceClientConfig());
    }

    @Test
    public void testJoelWorkflow() {
        assumeTrue(weblyzardServiceAvailable(joelClient));
        try {
            // 1. send the psalmDocs to the joel
            assertEquals(200, joelClient.addDocuments(psalmDocs).getStatus());
            // 2. cluster the documents
            List<ClusterResult> clusterResults = joelClient.cluster();
            assertTrue(clusterResults.size() > 0);
            // flush the queue
            assertEquals(200, joelClient.flush().getStatus());
        } catch (ClientErrorException e) {
            e.printStackTrace();
        }
    }

    /** tests adding a document without keywords in the header */
    @Test
    public void testDocumentHeaderBadRequest() {
        assumeTrue(weblyzardServiceAvailable(joelClient));
        Exception e = assertThrows(ClientErrorException.class, () -> { 
            joelClient.addDocuments(Arrays.asList(new LegacyDocument[] {
                    new LegacyDocument().setSentences(Arrays.asList(new Sentence("Test")))}));
        });
        assertEquals(JoelClient.NO_KEYWORD_IN_DOCUMENT_HEADER_MESSAGE, e.getMessage());
    }

    public List<LegacyDocument> readWeblyzardDocuments() {
        try {

            logger.info(JoelClientIT.class.getClassLoader().getResource(".").getPath());
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.configure(SerializationFeature.FAIL_ON_EMPTY_BEANS, false);
            return objectMapper.readValue(
                    JoelClientIT.class.getClassLoader()
                            .getResourceAsStream(PSALMS_DOCS_WEBLYZARDFORMAT_JSON),
                    new TypeReference<List<LegacyDocument>>() {});
        } catch (JsonParseException e1) {
            e1.printStackTrace();
        } catch (JsonMappingException e1) {
            e1.printStackTrace();
        } catch (IOException e1) {
            e1.printStackTrace();
        }
        return null;
    }
}
