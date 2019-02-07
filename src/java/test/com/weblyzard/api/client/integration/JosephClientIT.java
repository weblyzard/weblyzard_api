package com.weblyzard.api.client.integration;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.IOException;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.weblyzard.api.client.JosephClient;
import com.weblyzard.api.client.WebserviceClientConfig;
import com.weblyzard.api.model.document.Document;

public class JosephClientIT extends TestClientBase {

    private static final String PSALMS_DOCS_WEBLYZARDFORMAT_JSON =
            "resources/psalms-docs-weblyzardformat.json";

    public List<Document> psalmDocs;

    private JosephClient client;

    private String profileName = "smc";

    @BeforeEach
    @Test
    public void before() {
        psalmDocs = readWeblyzardDocuments();
        client = new JosephClient(new WebserviceClientConfig());
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

            logger.info(JoelClientIT.class.getClassLoader().getResource(".").getPath());
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.configure(SerializationFeature.FAIL_ON_EMPTY_BEANS, false);
            return objectMapper.readValue(
                    JoelClientIT.class.getClassLoader()
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
