package com.weblyzard.api.client;

import java.util.List;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.model.document.MirrorDocument;

/**
 * webLyzard document pre-processing services.
 * 
 * @author Philipp Kuntschik
 * @author Albert Weichselbraun
 */
public class JeremiaClient extends BasicClient {

    private static final String SUBMIT_DOCUMENT_SERVICE_URL = "/rest/submit_document";
    private static String prefix = "/jeremia";
    private static final GenericType<List<Document>> DOCUMENT_LIST_TYPE = new GenericType<>() {};

    public JeremiaClient() {
        super();
    }

    public JeremiaClient(String weblyzardUrl) {
        super(weblyzardUrl);
    }

    /**
     * prefix and Url is overwritable
     * 
     * @param weblyzardUrl e.g. http://localhost:63001
     * @param prefix if prefix is null, no prefix will be applied, otherwise prefix is used before
     *        resource
     */
    public JeremiaClient(String weblyzardUrl, String prefix) {
        super(weblyzardUrl);
        JeremiaClient.prefix = prefix == null ? "" : prefix;
    }

    public JeremiaClient(String weblyzardUrl, String username, String password) {
        super(weblyzardUrl, username, password);
    }

    /**
     * Submits a single {@link MirrorDocument} to the document pre-processing service
     * 
     * @param request the document to process
     * @return the corresponding {@link Document} object
     */
    public Document submitDocument(MirrorDocument request) throws WebApplicationException {
        try (Response response = super.getTarget(prefix + SUBMIT_DOCUMENT_SERVICE_URL)
                .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(request))) {
            super.checkResponseStatus(response);
            return response.readEntity(Document.class);
        }
    }

    /**
     * Submits a list of {@link MirrorDocument}s to the document pre-processing service.
     * 
     * @param request the list of mirror documents
     * @return a list of {@link Document} objects
     */
    public List<Document> submitDocuments(List<MirrorDocument> request)
            throws WebApplicationException {
        try (Response response = super.getTarget(prefix + SUBMIT_DOCUMENT_SERVICE_URL)
                .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(request))) {
            super.checkResponseStatus(response);
            return response.readEntity(DOCUMENT_LIST_TYPE);
        }
    }
}
