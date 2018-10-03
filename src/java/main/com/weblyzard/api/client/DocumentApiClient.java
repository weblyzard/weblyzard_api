package com.weblyzard.api.client;

import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;
import com.weblyzard.api.model.document_api.Request;
import com.weblyzard.api.model.document_api.Response;

/**
 * TODO: untested!
 *
 * @author philipp.kuntschik@htwchur.ch
 */
public class DocumentApiClient extends BasicClient {

    private static final String WEBLYZARD_DOCUMENT_API_URL = "";

    public DocumentApiClient(WebserviceClientConfig c) {
        super(c);
        c.setServicePrefixIfEmpty("/document-api");
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
