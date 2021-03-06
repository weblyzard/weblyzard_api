package com.weblyzard.api.client;

import java.util.Collections;
import java.util.List;
import java.util.Map;
import javax.json.JsonObject;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.model.jesaja.KeywordCalculationProfile;

/**
 * Jesaja keyword extraction service.
 * 
 * @author Philipp Kuntschik
 * @author Albert Weichselbraun
 *
 */
public class JesajaClient extends BasicClient {

    private static final String TEMPLATE_MATVIEW = "matview";
    private static final String TEMPLATE_PROFILE = "profile";

    private static final String GET_KEYWORDS_SERVICE_URL = "/rest/get_keywords/{" + TEMPLATE_MATVIEW + "}";
    private static final String SET_REFERENCE_CORPUS_SERVICE_URL = "/rest/add_csv/{" + TEMPLATE_MATVIEW + "}";
    private static final String ADD_DOCUMENTS_SERVICE_URL = "/rest/add_documents/{" + TEMPLATE_MATVIEW + "}";
    private static final String GET_NEK_ANNOTATIONS_SERVICE_URL =
                    "/rest/get_nek_annotations/{" + TEMPLATE_MATVIEW + "}";
    private static final String ROTATE_SHARD_SERVICE_URL = "/rest/rotate_shard/{" + TEMPLATE_MATVIEW + "}";
    private static final String SET_MATVIEW_PROFILE_URL =
                    "/rest/set_matview_profile/{" + TEMPLATE_PROFILE + "}/{" + TEMPLATE_PROFILE + "}";
    private static final String SET_KEYWORD_PROFILE_URL = "/rest/set_keyword_profile/{" + TEMPLATE_PROFILE + "}";

    WebserviceClientConfig config;

    public JesajaClient(WebserviceClientConfig c) {
        super(c, "/jesaja");
        this.config = c;
    }

    public Response setReferenceCorpus(String matviewId, Map<String, Integer> corpusMapping) {

        try (Response response =
                        super.getTarget(SET_REFERENCE_CORPUS_SERVICE_URL).resolveTemplate(TEMPLATE_MATVIEW, matviewId)
                                        .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(corpusMapping))) {

            super.checkResponseStatus(response);
            return response;
        }
    }


    public Response addDocuments(String matviewId, List<Document> documents) {

        try (Response response = super.getTarget(ADD_DOCUMENTS_SERVICE_URL).resolveTemplate(TEMPLATE_MATVIEW, matviewId)
                        .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(documents))) {

            super.checkResponseStatus(response);
            return response;
        }
    }

    public Map<String, Map<String, Double>> getKeywords(String matviewId, List<Document> documents) {
        try (Response response = super.getTarget(GET_KEYWORDS_SERVICE_URL).resolveTemplate(TEMPLATE_MATVIEW, matviewId)
                        .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(documents))) {

            super.checkResponseStatus(response);
            Map<String, Map<String, Double>> result =
                            response.readEntity(new GenericType<Map<String, Map<String, Double>>>() {});
            return result == null ? Collections.emptyMap() : result;
        }
    }

    public JsonObject getNonEntityKeywordAnnotations(String matviewId, List<Document> documents) {
        try (Response response =
                        super.getTarget(GET_NEK_ANNOTATIONS_SERVICE_URL).resolveTemplate(TEMPLATE_MATVIEW, matviewId)
                                        .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(documents))) {

            super.checkResponseStatus(response);
            return response.readEntity(JsonObject.class);
        }
    }

    public int rotateShard(String matviewId) {
        try (Response response = super.getTarget(ROTATE_SHARD_SERVICE_URL).resolveTemplate(TEMPLATE_MATVIEW, matviewId)
                        .request(MediaType.APPLICATION_JSON_TYPE).get()) {

            super.checkResponseStatus(response);
            return response.readEntity(Integer.class);
        }
    }

    public void setMatviewProfile(String profileName, String matviewId) {
        try (Response response = super.getTarget(SET_MATVIEW_PROFILE_URL).resolveTemplate(TEMPLATE_PROFILE, profileName)
                        .resolveTemplate(TEMPLATE_MATVIEW, matviewId).request(MediaType.APPLICATION_JSON_TYPE).get()) {

            super.checkResponseStatus(response);
        }
    }

    public void setKeywordProfile(String profileName, KeywordCalculationProfile keywordProfile) {
        try (Response response = super.getTarget(SET_KEYWORD_PROFILE_URL).resolveTemplate(TEMPLATE_PROFILE, profileName)
                        .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(keywordProfile))) {

            super.checkResponseStatus(response);
        }
    }

}
