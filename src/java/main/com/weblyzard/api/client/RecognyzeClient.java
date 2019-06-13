package com.weblyzard.api.client;

import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import com.weblyzard.api.model.document.Document;

/**
 * Provide access to the Recognyze named entity linking Web service.
 * 
 * @author Philipp Kuntschik
 * @author Albert Weichselbraun
 */
public class RecognyzeClient extends BasicClient {

    private static final String TEMPLATE_PROFILE_NAME = "profileName";

    private static final String ADD_PROFILE_SERVICE_URL = "/rest/load_profile/{" + TEMPLATE_PROFILE_NAME + "}";
    private static final String SEARCH_DOCUMENT_SERVICE_URL = "/rest/search_document";
    private static final String SEARCH_DOCUMENTS_SERVICE_URL = "/rest/search_documents";
    private static final String STATUS_SERVICE_URL = "/rest/status";

    private static final String PARAM_PROFILE_NAME = "profileName";
    private static final String PARAM_LIMIT = "limit";

    public RecognyzeClient(WebserviceClientConfig c) {
        super(c, "/recognize");
    }


    public boolean loadProfile(String profileName) throws WebApplicationException {

        try (Response response =
                        super.getTarget(ADD_PROFILE_SERVICE_URL).resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                                        .request(MediaType.APPLICATION_JSON_TYPE).get()) {

            super.checkResponseStatus(response);
            boolean result = response.readEntity(Boolean.class);
            return result;
        }
    }

    public Document searchDocument(String profileName, Document data) throws WebApplicationException {

        return this.searchDocument(profileName, data, 0);
    }

    public Document searchDocument(String profileName, Document data, int limit) throws WebApplicationException {

        try (Response response = super.getTarget(SEARCH_DOCUMENT_SERVICE_URL)
                        .queryParam(PARAM_PROFILE_NAME, profileName).queryParam(PARAM_LIMIT, limit)
                        .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(data))) {

            super.checkResponseStatus(response);
            Document result = response.readEntity(Document.class);
            return result;
        }
    }

    public List<Document> searchDocuments(String profileName, Set<Document> data) throws WebApplicationException {

        return this.searchDocuments(profileName, data, 0);
    }

    public List<Document> searchDocuments(String profileName, Set<Document> data, int limit)
                    throws WebApplicationException {

        try (Response response = super.getTarget(SEARCH_DOCUMENTS_SERVICE_URL)
                        .queryParam(PARAM_PROFILE_NAME, profileName).queryParam(PARAM_LIMIT, limit)
                        .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(data))) {

            super.checkResponseStatus(response);
            List<Document> result = response.readEntity(new GenericType<List<Document>>() {});
            return result == null ? Collections.emptyList() : result;
        }
    }

    public Map<String, Object> status() throws WebApplicationException {

        try (Response response = super.getTarget(STATUS_SERVICE_URL).request(MediaType.APPLICATION_JSON_TYPE).get()) {

            super.checkResponseStatus(response);
            Map<String, Object> result = response.readEntity(new GenericType<Map<String, Object>>() {});
            return result == null ? Collections.emptyMap() : result;
        }
    }
}
