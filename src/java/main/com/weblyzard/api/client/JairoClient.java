package com.weblyzard.api.client;

import java.util.List;

import javax.ws.rs.ClientErrorException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import com.weblyzard.lib.document.annotation.Annotation;

public class JairoClient extends BasicClient

{

	private static final String EXTEND_ANNOTATIONS = "/jairo/extend_annotations/";



	/**
	 * @see BasicClient
	 */
	public JairoClient() {
		super();
	}



	/**
	 * @see BasicClient
	 */
	public JairoClient(String weblyzard_url) {
		super(weblyzard_url);
	}



	/**
	 * @see BasicClient
	 */
	public JairoClient(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}



	public List<Annotation> extendAnnotations(String profileName, List<Annotation> annotations)
			throws ClientErrorException {

		Response response = super.target.path(EXTEND_ANNOTATIONS + profileName).request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(annotations));

		super.checkResponseStatus(response);
		List<Annotation> result = response.readEntity(new GenericType<List<Annotation>>() {
		});
		response.close();

		return result;
	}
}
