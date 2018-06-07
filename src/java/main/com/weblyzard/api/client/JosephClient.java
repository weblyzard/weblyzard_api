package com.weblyzard.api.client;

import java.util.List;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.model.recognyze.RecognyzeResult;

/** @author philipp.kuntschik@htwchur.ch */
public class JosephClient extends BasicClient {

    private static final String TEMPLATE_PROFILE_NAME = "profileName";
    private static final String TEMPLATE_CATEGORY = "category1";

    private static final String LOAD_PROFILE_SERVICE_URL =
            "/joseph/rest/load_profile/{" + TEMPLATE_PROFILE_NAME + "}";
    private static final String UNLOAD_PROFILE_SERVICE_URL =
            "/joseph/rest/unload_profile/{" + TEMPLATE_PROFILE_NAME + "}";
    private static final String CLEAN_PROFILE_SERVICE_URL =
            "joseph/rest/clean/{" + TEMPLATE_PROFILE_NAME + "}";
    private static final String CLASSIFY_SERVICE_URL =
            "/joseph/rest/classify/{" + TEMPLATE_PROFILE_NAME + "}";
    private static final String TRAIN_SERVICE_URL =
            "/joseph/rest/train/{" + TEMPLATE_PROFILE_NAME + "}/{" + TEMPLATE_CATEGORY + "}";
    private static final String RETRAIN_SERVICE_URL =
            "/joseph/rest/retrain/{" + TEMPLATE_PROFILE_NAME + "}/{" + TEMPLATE_CATEGORY + "}";
    private static final String FORGET_SERVICE_URL =
            "/joseph/rest/forget/{" + TEMPLATE_PROFILE_NAME + "}/{" + TEMPLATE_CATEGORY + "}";

    private static final String PARAM_LIMIT = "limit";
    private static final String PARAM_WITH_FEATURES = "full";

    public JosephClient() {
        super();
    }

    public JosephClient(String weblyzardUrl) {
        super(weblyzardUrl);
    }

    public JosephClient(String weblyzardUrl, String username, String password) {
        super(weblyzardUrl, username, password);
    }

    public boolean loadProfile(String profileName) {
        Response response = super.getTarget(LOAD_PROFILE_SERVICE_URL)
                .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                .request(MediaType.APPLICATION_JSON_TYPE).get();

        super.checkResponseStatus(response);
        boolean result = response.readEntity(Boolean.class);
        response.close();

        return result;
    }

    public boolean cleanProfile(String profileName) {
        Response response = super.getTarget(CLEAN_PROFILE_SERVICE_URL)
                .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                .request(MediaType.APPLICATION_JSON_TYPE).get();

        super.checkResponseStatus(response);
        boolean result = response.readEntity(Boolean.class);
        response.close();

        return result;
    }

    public boolean unloadProfile(String profileName) {
        Response response = super.getTarget(UNLOAD_PROFILE_SERVICE_URL)
                .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                .request(MediaType.APPLICATION_JSON_TYPE).get();

        super.checkResponseStatus(response);
        boolean result = response.readEntity(Boolean.class);
        response.close();

        return result;
    }

    public boolean train(String profileName, Document document, String category) {
        Response response = super.getTarget(TRAIN_SERVICE_URL)
                .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                .resolveTemplate(TEMPLATE_CATEGORY, category)
                .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(document));

        super.checkResponseStatus(response);
        boolean result = response.readEntity(Boolean.class);
        response.close();

        return result;
    }

    public boolean retrain(String profileName, Document document, String category) {
        Response response = super.getTarget(RETRAIN_SERVICE_URL)
                .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                .resolveTemplate(TEMPLATE_CATEGORY, category)
                .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(document));

        super.checkResponseStatus(response);
        boolean result = response.readEntity(Boolean.class);
        response.close();

        return result;
    }

    public boolean forget(String profileName, Document document, String category) {
        Response response = super.getTarget(FORGET_SERVICE_URL)
                .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                .resolveTemplate(TEMPLATE_CATEGORY, category)
                .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(document));

        super.checkResponseStatus(response);
        boolean result = response.readEntity(Boolean.class);
        response.close();

        return result;
    }

    public List<RecognyzeResult> classify(String profileName, Document request) {
        return this.classify(profileName, request, 0, false);
    }

    public List<RecognyzeResult> classify(String profileName, Document request, int limit,
            boolean withFeatures) throws WebApplicationException {

        Response response = super.getTarget(CLASSIFY_SERVICE_URL)
                .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName).queryParam(PARAM_LIMIT, limit)
                .queryParam(PARAM_WITH_FEATURES, withFeatures)
                .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(request));

        super.checkResponseStatus(response);
        List<RecognyzeResult> result =
                response.readEntity(new GenericType<List<RecognyzeResult>>() {});
        response.close();

        return result;
    }
}
