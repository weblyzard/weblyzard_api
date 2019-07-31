package com.weblyzard.api.client.integration;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Disabled;
import com.weblyzard.api.client.InscriptisClient;
import com.weblyzard.api.client.WebserviceClientConfig;

public class InscriptisClientIT extends TestClientBase {

    private InscriptisClient inscriptisClient;

    @BeforeEach
    public void before() {
        inscriptisClient = new InscriptisClient(
                        new WebserviceClientConfig().setUrl("http://localhost").setServicePrefix(":5000"));
    }

    @Disabled
    public void testInscriptisClient() {
        String parseResult = inscriptisClient.parseHtml("<html><body><h1>Test Titel</h1></body></html>");
        System.out.println(parseResult);
    }
}
