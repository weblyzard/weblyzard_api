package com.weblyzard.api.client;

import java.util.List;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.model.joseph.Classification;

/**
 * @author Philipp Kuntschik
 */
public class JosephClient extends BasicClient {

    private static final String TEMPLATE_PROFILE_NAME = "profileName";
    private static final String TEMPLATE_CATEGORY = "category1";

    private static final String LOAD_PROFILE_SERVICE_URL =
            "/rest/load_profile/{" + TEMPLATE_PROFILE_NAME + "}";
    private static final String UNLOAD_PROFILE_SERVICE_URL =
            "/rest/unload_profile/{" + TEMPLATE_PROFILE_NAME + "}";
    private static final String CLEAN_PROFILE_SERVICE_URL =
            "/rest/clean/{" + TEMPLATE_PROFILE_NAME + "}";
    private static final String CLASSIFY_SERVICE_URL =
            "/rest/classify/{" + TEMPLATE_PROFILE_NAME + "}";
    private static final String TRAIN_SERVICE_URL =
            "/rest/train/{" + TEMPLATE_PROFILE_NAME + "}/{" + TEMPLATE_CATEGORY + "}";
    private static final String RETRAIN_SERVICE_URL =
            "/rest/retrain/{" + TEMPLATE_PROFILE_NAME + "}/{" + TEMPLATE_CATEGORY + "}";
    private static final String FORGET_SERVICE_URL =
            "/rest/forget/{" + TEMPLATE_PROFILE_NAME + "}/{" + TEMPLATE_CATEGORY + "}";

    private static final String PARAM_LIMIT = "limit";
    private static final String PARAM_WITH_FEATURES = "full";

    public JosephClient(WebserviceClientConfig c) {
        super(c, "/joseph");
    }

    public boolean loadProfile(String profileName) {
        try (Response response = super.getTarget(LOAD_PROFILE_SERVICE_URL)
                .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                .request(MediaType.APPLICATION_JSON_TYPE).get()) {

            super.checkResponseStatus(response);
            boolean result = response.readEntity(Boolean.class);
            return result;
        }
    }

    public boolean cleanProfile(String profileName) {
        try (Response response = super.getTarget(CLEAN_PROFILE_SERVICE_URL)
                .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                .request(MediaType.APPLICATION_JSON_TYPE).get()) {

            super.checkResponseStatus(response);
            boolean result = response.readEntity(Boolean.class);
            return result;
        }
    }

    public boolean unloadProfile(String profileName) {
        try (Response response = super.getTarget(UNLOAD_PROFILE_SERVICE_URL)
                .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                .request(MediaType.APPLICATION_JSON_TYPE).get()) {

            super.checkResponseStatus(response);
            boolean result = response.readEntity(Boolean.class);
            return result;
        }
    }

    public boolean train(String profileName, Document document, String category) {
        try (Response response = super.getTarget(TRAIN_SERVICE_URL)
                .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                .resolveTemplate(TEMPLATE_CATEGORY, category)
                .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(document))) {

            super.checkResponseStatus(response);
            boolean result = response.readEntity(Boolean.class);
            return result;
        }
    }

    public boolean retrain(String profileName, Document document, String category) {
        try (Response response = super.getTarget(RETRAIN_SERVICE_URL)
                .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                .resolveTemplate(TEMPLATE_CATEGORY, category)
                .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(document))) {

            super.checkResponseStatus(response);
            boolean result = response.readEntity(Boolean.class);
            return result;
        }
    }

    public boolean forget(String profileName, Document document, String category) {
        try (Response response = super.getTarget(FORGET_SERVICE_URL)
                .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                .resolveTemplate(TEMPLATE_CATEGORY, category)
                .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(document))) {

            super.checkResponseStatus(response);
            boolean result = response.readEntity(Boolean.class);
            return result;
        }
    }

    public List<Classification> classify(String profileName, Document request) {
        return this.classify(profileName, request, 0, false);
    }

    public List<Classification> classify(String profileName, Document request, int limit,
            boolean withFeatures) throws WebApplicationException {

        try (Response response = super.getTarget(CLASSIFY_SERVICE_URL)
                .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName).queryParam(PARAM_LIMIT, limit)
                .queryParam(PARAM_WITH_FEATURES, withFeatures)
                .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(request))) {

            super.checkResponseStatus(response);
            List<Classification> result =
                    response.readEntity(new GenericType<List<Classification>>() {});
            return result;
        }
    }
}
