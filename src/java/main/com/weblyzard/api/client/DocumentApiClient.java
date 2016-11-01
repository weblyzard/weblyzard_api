package com.weblyzard.api.client;

import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;

import com.weblyzard.api.document_api.Request;
import com.weblyzard.api.document_api.Response;

/**
 * TODO: untested!
 * 
 * @author philipp.kuntschik@htwchur.ch
 *
 */
public class DocumentApiClient extends BasicClient {

	private static final String WEBLYZARDDOCUMENTAPIURL = "";



	/**
	 * @see BasicClient
	 */
	public DocumentApiClient() {
		super();
	}



	/**
	 * @see BasicClient
	 */
	public DocumentApiClient(String weblyzard_url) {
		super(weblyzard_url);
	}



	/**
	 * @see BasicClient
	 */
	public DocumentApiClient(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}



	public Response insertNewDocument(Request request) {

		javax.ws.rs.core.Response response = super.target.path(WEBLYZARDDOCUMENTAPIURL)
				.request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(request));

		super.checkResponseStatus(response);
		Response result = response.readEntity(Response.class);
		response.close();

		return result;
	}
}