package com.weblyzard.api.client.integration;

import static org.hamcrest.CoreMatchers.is;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertThat;
import static org.junit.Assert.assertTrue;
import static org.junit.Assume.assumeTrue;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.weblyzard.api.client.JoelClient;
import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.model.joel.ClusterResult;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import javax.ws.rs.ClientErrorException;
import javax.xml.bind.JAXBException;
import org.junit.Before;
import org.junit.Test;

/** @author norman.suesstrunk@htwchur.ch */
public class JoelClientIT extends TestClientBase {

    private static final String PSALMS_DOCS_WEBLYZARDFORMAT_JSON =
            "resources/psalms-docs-weblyzardformat.json";

    public List<Document> psalmDocs;

    private JoelClient joelClient;

    @Before
    public void before() {
        psalmDocs = readWeblyzardDocuments();
        joelClient = new JoelClient();
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
        } catch (ClientErrorException | JAXBException e) {
            e.printStackTrace();
        }
    }

    /** tests adding a document without keywords in the header */
    @Test
    public void testDocumentHeaderBadRequest() {
        assumeTrue(weblyzardServiceAvailable(joelClient));
        try {
            joelClient.addDocuments(Arrays.asList(new Document[] {new Document("Test")}));
        } catch (ClientErrorException clientErrorException) {
            assertThat(
                    clientErrorException.getMessage(),
                    is(JoelClient.NO_KEYWORD_IN_DOCUMENT_HEADER_MESSAGE));
        } catch (JAXBException jaxbException) {
            jaxbException.printStackTrace();
        }
    }

    public List<Document> readWeblyzardDocuments() {
        try {

            logger.info(JoelClientIT.class.getClassLoader().getResource(".").getPath());
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.configure(SerializationFeature.FAIL_ON_EMPTY_BEANS, false);
            return objectMapper.readValue(
                    JoelClientIT.class
                            .getClassLoader()
                            .getResourceAsStream(PSALMS_DOCS_WEBLYZARDFORMAT_JSON),
                    new TypeReference<List<Document>>() {});
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
