package com.weblyzard.api.client;

import java.util.List;
import java.util.Map;

import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import com.weblyzard.api.document.annotation.Annotation;
import com.weblyzard.api.jairo.Profile;
import com.weblyzard.api.jairo.RDFPrefix;

public class JairoClient extends BasicClient {
	
	private static final String template_profileName = "profileName";

	private static final String EXTEND_ANNOTATIONS 		= "/jairo/rest/extend_annotations/{" + template_profileName + "}";
	private static final String ADD_PROFILE 			= "/jairo/rest/add_profile/{" + template_profileName + "}";
	private static final String LIST_PROFILES 			= "/jairo/rest/list_profiles";
	private static final String LIST_RDF_PREFIXES 		= "/jairo/rest/list_rdf_prefixes";
	private static final String ADD_RDF_PREFIX 			= "/jairo/rest/add_rdf_prefix";

	public JairoClient() {
		super();
	}

	public JairoClient(String weblyzard_url) {
		super(weblyzard_url);
	}

	public JairoClient(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}

	public List<Annotation> extendAnnotations(String profileName, List<Annotation> annotations)
			throws WebApplicationException {

		Response response = super.getTarget(EXTEND_ANNOTATIONS)
				.resolveTemplate(template_profileName, profileName)
				.request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(annotations));

		super.checkResponseStatus(response);
		List<Annotation> result = response.readEntity(new GenericType<List<Annotation>>() {});
		response.close();
		return result;
	}
	
	public Response addProfile(Profile profile, String profileName) {
		
		Response response = super.getTarget(ADD_PROFILE)
				.resolveTemplate(template_profileName, profileName)
				.request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(profile));
		
		super.checkResponseStatus(response);
		response.close(); 
		return response;
		
	}
	
	public Map<String, Profile> listProfiles() {
		Response response = super.getTarget(LIST_PROFILES)
				.request(MediaType.APPLICATION_JSON_TYPE).get(); 
		
		super.checkResponseStatus(response);
		Map<String, Profile> profiles = response.readEntity(new GenericType<Map<String, Profile>>() {});
		response.close(); 
		return profiles;
	}
	
	public Response addPrefix(RDFPrefix rdfPrefix) {
		Response response = super.getTarget(ADD_RDF_PREFIX)
				.request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(rdfPrefix));
		
		super.checkResponseStatus(response);
		response.close(); 
		return response;
	}
	
	
	public Map<String, String> listRdfPrefixes() {
		Response response = super.getTarget(LIST_RDF_PREFIXES)
				.request(MediaType.APPLICATION_JSON_TYPE).get(); 
		
		super.checkResponseStatus(response);
		Map<String, String> profiles = response.readEntity(new GenericType<Map<String, String>>() {});
		response.close(); 
		return profiles;
	}
}
