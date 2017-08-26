package com.weblyzard.api.client;

import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.recognyze.RecognyzeResult;
import java.util.List;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

/** @author philipp.kuntschik@htwchur.ch */
public class JosephClient extends BasicClient {

    private static final String template_profileName = "profileName";
    private static final String template_category1 = "category1";

    private static final String LOAD_PROFILE_SERVICE_URL =
            "/joseph/rest/load_profile/{" + template_profileName + "}";
    private static final String UNLOAD_PROFILE_SERVICE_URL =
            "/joseph/rest/unload_profile/{" + template_profileName + "}";
    private static final String CLEAN_PROFILE_SERVICE_URL =
            "joseph/rest/clean/{" + template_profileName + "}";
    private static final String CLASSIFY_SERVICE_URL =
            "/joseph/rest/classify/{" + template_profileName + "}";
    private static final String TRAIN_SERVICE_URL =
            "/joseph/rest/train/{" + template_profileName + "}/{" + template_category1 + "}";
    private static final String RETRAIN_SERVICE_URL =
            "/joseph/rest/retrain/{" + template_profileName + "}/{" + template_category1 + "}";
    private static final String FORGET_SERVICE_URL =
            "/joseph/rest/forget/{" + template_profileName + "}/{" + template_category1 + "}";

    private static final String param_limit = "limit";
    private static final String param_withFeatures = "full";

    public JosephClient() {
        super();
    }

    public JosephClient(String weblyzard_url) {
        super(weblyzard_url);
    }

    public JosephClient(String weblyzard_url, String username, String password) {
        super(weblyzard_url, username, password);
    }

    public boolean loadProfile(String profileName) {
        Response response =
                super.getTarget(LOAD_PROFILE_SERVICE_URL)
                        .resolveTemplate(template_profileName, profileName)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .get();

        super.checkResponseStatus(response);
        boolean result = response.readEntity(Boolean.class);
        response.close();

        return result;
    }

    public boolean cleanProfile(String profileName) {
        Response response =
                super.getTarget(CLEAN_PROFILE_SERVICE_URL)
                        .resolveTemplate(template_profileName, profileName)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .get();

        super.checkResponseStatus(response);
        boolean result = response.readEntity(Boolean.class);
        response.close();

        return result;
    }

    public boolean unloadProfile(String profileName) {
        Response response =
                super.getTarget(UNLOAD_PROFILE_SERVICE_URL)
                        .resolveTemplate(template_profileName, profileName)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .get();

        super.checkResponseStatus(response);
        boolean result = response.readEntity(Boolean.class);
        response.close();

        return result;
    }

    public boolean train(String profileName, Document document, String category) {
        Response response =
                super.getTarget(TRAIN_SERVICE_URL)
                        .resolveTemplate(template_profileName, profileName)
                        .resolveTemplate(template_category1, category)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(document));

        super.checkResponseStatus(response);
        boolean result = response.readEntity(Boolean.class);
        response.close();

        return result;
    }

    public boolean retrain(String profileName, Document document, String category) {
        Response response =
                super.getTarget(RETRAIN_SERVICE_URL)
                        .resolveTemplate(template_profileName, profileName)
                        .resolveTemplate(template_category1, category)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(document));

        super.checkResponseStatus(response);
        boolean result = response.readEntity(Boolean.class);
        response.close();

        return result;
    }

    public boolean forget(String profileName, Document document, String category) {
        Response response =
                super.getTarget(FORGET_SERVICE_URL)
                        .resolveTemplate(template_profileName, profileName)
                        .resolveTemplate(template_category1, category)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(document));

        super.checkResponseStatus(response);
        boolean result = response.readEntity(Boolean.class);
        response.close();

        return result;
    }

    public List<RecognyzeResult> classify(String profileName, Document request) {
        return this.classify(profileName, request, 0, false);
    }

    public List<RecognyzeResult> classify(
            String profileName, Document request, int limit, boolean withFeatures)
            throws WebApplicationException {

        Response response =
                super.getTarget(CLASSIFY_SERVICE_URL)
                        .resolveTemplate(template_profileName, profileName)
                        .queryParam(param_limit, limit)
                        .queryParam(param_withFeatures, withFeatures)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(request));

        super.checkResponseStatus(response);
        List<RecognyzeResult> result =
                response.readEntity(new GenericType<List<RecognyzeResult>>() {});
        response.close();

        return result;
    }
}
