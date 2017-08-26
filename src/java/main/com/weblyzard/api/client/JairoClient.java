package com.weblyzard.api.client;

import com.weblyzard.api.model.annotation.Annotation;
import com.weblyzard.api.model.jairo.Profile;
import com.weblyzard.api.model.jairo.RDFPrefix;
import java.util.List;
import java.util.Map;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

public class JairoClient extends BasicClient {

    private static final String TEMPLATE_PROFILE_NAME = "profileName";

    private static final String EXTEND_ANNOTATIONS =
            "/jairo/rest/extend_annotations/{" + TEMPLATE_PROFILE_NAME + "}";
    private static final String ADD_PROFILE =
            "/jairo/rest/add_profile/{" + TEMPLATE_PROFILE_NAME + "}";
    private static final String LIST_PROFILES = "/jairo/rest/list_profiles";
    private static final String LIST_RDF_PREFIXES = "/jairo/rest/list_rdf_prefixes";
    private static final String ADD_RDF_PREFIX = "/jairo/rest/add_rdf_prefix";

    public JairoClient() {
        super();
    }

    public JairoClient(String weblyzardUrl) {
        super(weblyzardUrl);
    }

    public JairoClient(String weblyzardUrl, String username, String password) {
        super(weblyzardUrl, username, password);
    }

    public List<Annotation> extendAnnotations(String profileName, List<Annotation> annotations)
            throws WebApplicationException {

        Response response =
                super.getTarget(EXTEND_ANNOTATIONS)
                        .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(annotations));

        super.checkResponseStatus(response);
        List<Annotation> result = response.readEntity(new GenericType<List<Annotation>>() {});
        response.close();
        return result;
    }

    public Response addProfile(Profile profile, String profileName) {

        Response response =
                super.getTarget(ADD_PROFILE)
                        .resolveTemplate(TEMPLATE_PROFILE_NAME, profileName)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(profile));

        super.checkResponseStatus(response);
        response.close();
        return response;
    }

    public Map<String, Profile> listProfiles() {
        Response response =
                super.getTarget(LIST_PROFILES).request(MediaType.APPLICATION_JSON_TYPE).get();

        super.checkResponseStatus(response);
        Map<String, Profile> profiles =
                response.readEntity(new GenericType<Map<String, Profile>>() {});
        response.close();
        return profiles;
    }

    public Response addPrefix(RDFPrefix rdfPrefix) {
        Response response =
                super.getTarget(ADD_RDF_PREFIX)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(rdfPrefix));

        super.checkResponseStatus(response);
        response.close();
        return response;
    }

    public Map<String, String> listRdfPrefixes() {
        Response response =
                super.getTarget(LIST_RDF_PREFIXES).request(MediaType.APPLICATION_JSON_TYPE).get();

        super.checkResponseStatus(response);
        Map<String, String> profiles =
                response.readEntity(new GenericType<Map<String, String>>() {});
        response.close();
        return profiles;
    }
}
