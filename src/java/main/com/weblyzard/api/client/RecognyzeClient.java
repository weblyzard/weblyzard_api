package com.weblyzard.api.client;

import java.util.Collections;
import java.util.Map;
import java.util.Set;

import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import com.weblyzard.api.document.Document;
import com.weblyzard.api.recognyze.RecognyzeResult;

/**
 * 
 * @author philipp.kuntschik@htwchur.ch
 *
 */
public class RecognyzeClient extends BasicClient {

	private static final String ADD_PROFILE_SERVICE_URL = "/Recognize/rest/load_profile/";
	private static final String SEARCH_TEXT_SERVICE_URL = "/Recognize/rest/searchText";
	private static final String SEARCH_DOCUMENT_SERVICE_URL = "/Recognize/rest/searchDocument";
	private static final String SEARCH_DOCUMENTS_SERVICE_URL = "/Recognize/rest/searchDocuments";
	private static final String STATUS_SERVICE_URL = "/Recognize/rest/status";
	private static final String PROFILENAME = "profileName=";
	private static final String LIMIT = "limit=";

	public RecognyzeClient() {
		super();
	}

	public RecognyzeClient(String weblyzard_url) {
		super(weblyzard_url);
	}

	public RecognyzeClient(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}

	public boolean loadProfile(String profileName) throws WebApplicationException {

		Response response = super.target
				.path(ADD_PROFILE_SERVICE_URL + profileName)
				.request(MediaType.APPLICATION_JSON_TYPE)
				.get();

		super.checkResponseStatus(response);
		boolean result = response
				.readEntity(Boolean.class);
		response.close();

		return result;
	}



	public Set<RecognyzeResult> searchText(String profileName, String data) throws WebApplicationException {
		return this.searchText(profileName, data, 0);
	}



	public Set<RecognyzeResult> searchText(String profileName, String data, int limit) throws WebApplicationException {

		Response response = super.target
				.path(SEARCH_TEXT_SERVICE_URL + "?" + PROFILENAME + profileName + "&" + LIMIT + limit)
				.request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(data));

		super.checkResponseStatus(response);
		Set<RecognyzeResult> result = response
				.readEntity(new GenericType<Set<RecognyzeResult>>() {});
		response.close();

		return result == null ? Collections.emptySet() : result;
	}



	public Set<RecognyzeResult> searchDocument(String profileName, Document data) throws WebApplicationException {

		return this.searchDocument(profileName, data, 0);
	}



	public Set<RecognyzeResult> searchDocument(String profileName, Document data, int limit)
			throws WebApplicationException {

		Response response = super.target
				.path(SEARCH_DOCUMENT_SERVICE_URL + "?" + PROFILENAME + profileName + "&" + LIMIT + limit)
				.request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(data));

		super.checkResponseStatus(response);
		Set<RecognyzeResult> result = response
				.readEntity(new GenericType<Set<RecognyzeResult>>() {});
		response.close();

		return result == null ? Collections.emptySet() : result;
	}



	public Map<String, Set<RecognyzeResult>> searchDocuments(String profileName, Set<Document> data)
			throws WebApplicationException {

		return this.searchDocuments(profileName, data, 0);
	}



	public Map<String, Set<RecognyzeResult>> searchDocuments(String profileName, Set<Document> data, int limit)
			throws WebApplicationException {
		
		Response response = super.target
				.path(SEARCH_DOCUMENTS_SERVICE_URL + "?" + PROFILENAME + profileName + "&" + LIMIT + limit)
				.request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(data));

		super.checkResponseStatus(response);
		Map<String, Set<RecognyzeResult>> result = response
				.readEntity(new GenericType<Map<String, Set<RecognyzeResult>>>() {});
		response.close();

		return result == null ? Collections.emptyMap() : result;
	}



	public Map<String, Object> status() throws WebApplicationException {
		
		Response response = super.target.path(STATUS_SERVICE_URL)
				.request(MediaType.APPLICATION_JSON_TYPE)
				.get();

		super.checkResponseStatus(response);
		Map<String, Object> result = response
				.readEntity(new GenericType<Map<String, Object>>() {});
		response.close();

		return result == null ? Collections.emptyMap() : result;
	}
}