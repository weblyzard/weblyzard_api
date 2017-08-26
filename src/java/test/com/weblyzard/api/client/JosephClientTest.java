package com.weblyzard.api.client;

import static org.junit.Assert.*;
import static org.junit.Assume.assumeTrue;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.weblyzard.api.model.document.Document;
import java.io.IOException;
import java.util.List;
import org.junit.Before;
import org.junit.Test;

public class JosephClientTest extends TestClientBase {

    private static final String PSALMS_DOCS_WEBLYZARDFORMAT_JSON =
            "resources/psalms-docs-weblyzardformat.json";

    public List<Document> psalmDocs;

    private JosephClient client;

    private String profileName = "smc";

    @Before
    @Test
    public void before() {
        psalmDocs = readWeblyzardDocuments();
        client = new JosephClient();
        assumeTrue(weblyzardServiceAvailable(client));
        assertTrue(client.loadProfile(profileName));
    }

    @Test
    public void testTrain() {
        assumeTrue(weblyzardServiceAvailable(client));
        psalmDocs.stream().forEach(document -> client.train("smc", document, "category"));
    }

    public List<Document> readWeblyzardDocuments() {
        try {

            logger.info(JoelClientTest.class.getClassLoader().getResource(".").getPath());
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.configure(SerializationFeature.FAIL_ON_EMPTY_BEANS, false);
            return objectMapper.readValue(
                    JoelClientTest.class
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
