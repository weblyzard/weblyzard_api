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

    private static final String TEMPLATE_SOURCE_ID = "source_id";
    private static final String TEMPLATE_DOUBLE_SENTENCE_THRESHOLD = "double_sentence_threshold";
    private static final int DEFAULT_DOUBLE_SENTENCE_THRESHOLD = 10;

    private static final String SUBMIT_DOCUMENT_SERVICE_URL = "/rest/submit_document";
    private static final String SUBMIT_DOCUMENTS_SERVICE_URL = "/rest/submit_documents/{"
            + TEMPLATE_SOURCE_ID + "}/{" + TEMPLATE_DOUBLE_SENTENCE_THRESHOLD + "}";
    private static final GenericType<List<Document>> DOCUMENT_LIST_TYPE = new GenericType<>() {};

    public JeremiaClient(WebserviceClientConfig c) {
        super(c, "/jeremia");
    }

    /**
     * Submits a single {@link MirrorDocument} to the document pre-processing service.
     * 
     * @param request the document to process
     * @return the corresponding {@link Document} object
     */
    public Document submitDocument(MirrorDocument request) throws WebApplicationException {
        try (Response response = super.getTarget(SUBMIT_DOCUMENT_SERVICE_URL)
                .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(request))) {
            super.checkResponseStatus(response);
            return response.readEntity(Document.class);
        }
    }

    /**
     * Submits a list of {@link MirrorDocument}s to the document pre-processing service.
     * 
     * @param request the list of mirror documents
     * @param sourceId used for sentence deduplication
     * @return a list of {@link Document} objects
     */
    public List<Document> submitDocuments(List<MirrorDocument> request, String sourceId,
            int doubleSentenceThreshold) {
        try (Response response = super.getTarget(SUBMIT_DOCUMENTS_SERVICE_URL)
                .resolveTemplate(TEMPLATE_SOURCE_ID, sourceId)
                .resolveTemplate(TEMPLATE_DOUBLE_SENTENCE_THRESHOLD,
                        Integer.toString(doubleSentenceThreshold))
                .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(request))) {
            super.checkResponseStatus(response);
            return response.readEntity(DOCUMENT_LIST_TYPE);
        }
    }

    public List<Document> submitDocuments(List<MirrorDocument> request, String sourceId) {
        return submitDocuments(request, sourceId, DEFAULT_DOUBLE_SENTENCE_THRESHOLD);
    }
}
