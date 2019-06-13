package com.weblyzard.api.client;

import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;
import com.weblyzard.api.model.flow.Request;
import com.weblyzard.api.model.flow.Response;

/**
 * Provides access to the webLyzard document api.
 * 
 * @author philipp.kuntschik@htwchur.ch
 * 
 *         TODO: untested!
 */
public class FlowClient extends BasicClient {

    private static final String WEBLYZARD_DOCUMENT_API_URL = "";

    public FlowClient(WebserviceClientConfig c) {
        super(c, "/document-api");
    }

    public Response insertNewDocument(Request request) {
        try (javax.ws.rs.core.Response response = super.getTarget(WEBLYZARD_DOCUMENT_API_URL)
                        .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(request))) {

            super.checkResponseStatus(response);
            Response result = response.readEntity(Response.class);
            return result;
        }
    }
}
