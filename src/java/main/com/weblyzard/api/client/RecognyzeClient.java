package com.weblyzard.api.client;

import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.model.recognyze.RecognyzeResult;
import java.util.Collections;
import java.util.Map;
import java.util.Set;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

/** @author philipp.kuntschik@htwchur.ch */
public class RecognyzeClient extends BasicClient {

    private static final String TEMPLATE_PROFILE_NAME = "profileName";

    private static final String ADD_PROFILE_SERVICE_URL =
            "/Recognize/rest/load_profile/{" + TEMPLATE_PROFILE_NAME + "}";
    private static final String SEARCH_TEXT_SERVICE_URL = "/Recognize/rest/searchText";
    private static final String SEARCH_DOCUMENT_SERVICE_URL = "/Recognize/rest/searchDocument";
    private static final String SEARCH_DOCUMENTS_SERVICE_URL = "/Recognize/rest/searchDocuments";
    private static final String STATUS_SERVICE_URL = "/Recognize/rest/status";

    private static final String PARAM_PROFILE_NAME = "profileName";
    private static final String PARAM_LIMIT = "limit";

    public RecognyzeClient() {
        super();
    }

    public RecognyzeClient(String weblyzardUrl) {
        super(weblyzardUrl);
    }

    public RecognyzeClient(String weblyzardUrl, String username, String password) {
        super(weblyzardUrl, username, password);
    }

    public boolean loadProfile(String profileName) throws WebApplicationException {

        Response response =
                super.getTarget(ADD_PROFILE_SERVICE_URL)
                        .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .get();

        super.checkResponseStatus(response);
        boolean result = response.readEntity(Boolean.class);
        response.close();

        return result;
    }

    public Set<RecognyzeResult> searchText(String profileName, String data)
            throws WebApplicationException {
        return this.searchText(profileName, data, 0);
    }

    public Set<RecognyzeResult> searchText(String profileName, String data, int limit)
            throws WebApplicationException {

        Response response =
                super.getTarget(SEARCH_TEXT_SERVICE_URL)
                        .queryParam(PARAM_PROFILE_NAME, profileName)
                        .queryParam(PARAM_LIMIT, limit)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(data));

        super.checkResponseStatus(response);
        Set<RecognyzeResult> result =
                response.readEntity(new GenericType<Set<RecognyzeResult>>() {});
        response.close();

        return result == null ? Collections.emptySet() : result;
    }

    public Set<RecognyzeResult> searchDocument(String profileName, Document data)
            throws WebApplicationException {

        return this.searchDocument(profileName, data, 0);
    }

    public Set<RecognyzeResult> searchDocument(String profileName, Document data, int limit)
            throws WebApplicationException {

        Response response =
                super.getTarget(SEARCH_DOCUMENT_SERVICE_URL)
                        .queryParam(PARAM_PROFILE_NAME, profileName)
                        .queryParam(PARAM_LIMIT, limit)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(data));

        super.checkResponseStatus(response);
        Set<RecognyzeResult> result =
                response.readEntity(new GenericType<Set<RecognyzeResult>>() {});
        response.close();

        return result == null ? Collections.emptySet() : result;
    }

    public Map<String, Set<RecognyzeResult>> searchDocuments(String profileName, Set<Document> data)
            throws WebApplicationException {

        return this.searchDocuments(profileName, data, 0);
    }

    public Map<String, Set<RecognyzeResult>> searchDocuments(
            String profileName, Set<Document> data, int limit) throws WebApplicationException {

        Response response =
                super.getTarget(SEARCH_DOCUMENTS_SERVICE_URL)
                        .queryParam(PARAM_PROFILE_NAME, profileName)
                        .queryParam(PARAM_LIMIT, limit)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(data));

        super.checkResponseStatus(response);
        Map<String, Set<RecognyzeResult>> result =
                response.readEntity(new GenericType<Map<String, Set<RecognyzeResult>>>() {});
        response.close();

        return result == null ? Collections.emptyMap() : result;
    }

    public Map<String, Object> status() throws WebApplicationException {

        Response response =
                super.getTarget(STATUS_SERVICE_URL).request(MediaType.APPLICATION_JSON_TYPE).get();

        super.checkResponseStatus(response);
        Map<String, Object> result = response.readEntity(new GenericType<Map<String, Object>>() {});
        response.close();

        return result == null ? Collections.emptyMap() : result;
    }
}
