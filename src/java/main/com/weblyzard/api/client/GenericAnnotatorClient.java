package com.weblyzard.api.client;

import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.service.AnnotationService;

/**
 * Provide access to the Recognyze named entity linking Web service
 * 
 * @author Philipp Kuntschik
 * @author Albert Weichselbraun
 */
public class GenericAnnotatorClient extends BasicClient implements AnnotationService {


    private static final String ANNOTATE_DOCUMENT_SERVICE_URL = "/rest/annotate_document";

    public GenericAnnotatorClient(WebserviceClientConfig c) {
        super(c, "/annotator");
    }

    @Override
    public Document annotateDocument(Document data) {

        try (Response response = super.getTarget(ANNOTATE_DOCUMENT_SERVICE_URL)
                .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(data))) {

            super.checkResponseStatus(response);
            Document result = response.readEntity(Document.class);
            return result;
        }
    }
}
