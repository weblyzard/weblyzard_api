package com.weblyzard.api.client;

import com.weblyzard.api.document_api.Request;
import com.weblyzard.api.document_api.Response;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;

/**
 * TODO: untested!
 *
 * @author philipp.kuntschik@htwchur.ch
 */
public class DocumentApiClient extends BasicClient {

    private static final String WEBLYZARD_DOCUMENT_API_URL = "";

    public DocumentApiClient() {
        super();
    }

    public DocumentApiClient(String weblyzard_url) {
        super(weblyzard_url);
    }

    public DocumentApiClient(String weblyzard_url, String username, String password) {
        super(weblyzard_url, username, password);
    }

    public Response insertNewDocument(Request request) {

        javax.ws.rs.core.Response response =
                super.getTarget(WEBLYZARD_DOCUMENT_API_URL)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(request));

        super.checkResponseStatus(response);
        Response result = response.readEntity(Response.class);
        response.close();

        return result;
    }
}
