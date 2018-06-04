package com.weblyzard.api.client;

import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.model.document.MirrorDocument;

/** @author philipp.kuntschik@htwchur.ch */
public class JeremiaClient extends BasicClient {

    private static final String SUBMIT_DOCUMENT_SERVICE_URL = "/jeremia/rest/submit_document";

    public JeremiaClient() {
        super();
    }

    public JeremiaClient(String weblyzardUrl) {
        super(weblyzardUrl);
    }

    public JeremiaClient(String weblyzardUrl, String username, String password) {
        super(weblyzardUrl, username, password);
    }

    public Document submitDocument(MirrorDocument request) throws WebApplicationException {

        Response response = super.getTarget(SUBMIT_DOCUMENT_SERVICE_URL)
                .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(request));

        super.checkResponseStatus(response);
        Document result = response.readEntity(Document.class);
        response.close();

        return result;
    }
}
