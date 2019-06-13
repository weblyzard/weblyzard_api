package com.weblyzard.api.client;

import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import com.weblyzard.api.model.johndoe.JohnDoeDocument;

/**
 * webLyzard annonymization service.
 * 
 * @author Sandro Hörler
 */
public class JohnDoeClient extends BasicClient {
    private static final String ANNON_SERVICE_URL = "/rest/annon";

    public JohnDoeClient(WebserviceClientConfig c) {
        super(c, "/johndoe");
    }

    /**
     * Computes an anonymized identifier for given Document.
     * 
     * @param document {@link JohnDoeDocument#JohnDoeDocument(String, String, java.util.List)}
     * @return {@link JohnDoeDocument} holds the annonymized content.
     */
    public JohnDoeDocument annonymizeContent(JohnDoeDocument document) {
        try (Response response = super.getTarget(ANNON_SERVICE_URL).request(MediaType.APPLICATION_JSON)
                        .post(Entity.entity(document, MediaType.APPLICATION_JSON))) {
            super.checkResponseStatus(response);
            return response.readEntity(JohnDoeDocument.class);
        }
    }
}
