package com.weblyzard.api.client;

import java.util.List;
import java.util.Map;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import com.weblyzard.api.model.annotation.Annotation;
import com.weblyzard.api.model.jairo.Profile;

public class JairoClient extends BasicClient {

    private static final String TEMPLATE_PROFILE_NAME = "profileName";

    private static final String EXTEND_ANNOTATIONS = "/rest/extend_annotations/{" + TEMPLATE_PROFILE_NAME + "}";
    private static final String ADD_PROFILE = "/rest/add_profile/{" + TEMPLATE_PROFILE_NAME + "}";
    private static final String LIST_PROFILES = "/rest/list_profiles";

    public JairoClient(WebserviceClientConfig c) {
        super(c, "/jairo");
    }

    public List<Annotation> extendAnnotations(String profileName, List<Annotation> annotations)
                    throws WebApplicationException {
        try (Response response = super.getTarget(EXTEND_ANNOTATIONS).resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                        .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(annotations))) {

            super.checkResponseStatus(response);
            List<Annotation> result = response.readEntity(new GenericType<List<Annotation>>() {});
            return result;
        }
    }

    public Response addProfile(Profile profile, String profileName) {
        try (Response response = super.getTarget(ADD_PROFILE).resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                        .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(profile))) {

            super.checkResponseStatus(response);
            return response;
        }
    }

    public Map<String, Profile> listProfiles() {
        try (Response response = super.getTarget(LIST_PROFILES).request(MediaType.APPLICATION_JSON_TYPE).get()) {

            super.checkResponseStatus(response);
            Map<String, Profile> profiles = response.readEntity(new GenericType<Map<String, Profile>>() {});
            return profiles;
        }
    }
}
