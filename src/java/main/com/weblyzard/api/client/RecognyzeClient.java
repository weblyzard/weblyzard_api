package com.weblyzard.api.client;

import java.util.Map;
import java.util.Set;

import javax.ws.rs.ClientErrorException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import com.weblyzard.api.domain.recognize.RecognyzeResult;
import com.weblyzard.lib.document.Document;

public class RecognyzeClient extends BasicClient {

	private static final String ADDPROFILESERVICEURL = "/Recognize/rest/load_profile/";
	private static final String SEARCHTEXTSERVICEURL = "/Recognize/rest/searchText";
	private static final String SEARCHDOCUMENTSERVICEURL = "/Recognize/rest/searchDocument";
	private static final String SEARCHDOCUMENTSSERVICEURL = "/Recognize/rest/searchDocuments";
	private static final String STATUSSERVICEURL = "/Recognize/rest/status";
	private static final String PROFILENAME = "profileName=";
	private static final String LIMIT = "limit=";



	/**
	 * @see BasicClient
	 */
	public RecognyzeClient() {
		super();
	}



	/**
	 * @see BasicClient
	 */
	public RecognyzeClient(String weblyzard_url) {
		super(weblyzard_url);
	}



	/**
	 * @see BasicClient
	 */
	public RecognyzeClient(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}



	public boolean loadProfile(String profileName) throws ClientErrorException {

		Response response = super.target
				.path(ADDPROFILESERVICEURL + profileName)
				.request(MediaType.APPLICATION_JSON_TYPE)
				.get();

		super.checkResponseStatus(response);
		boolean result = response
				.readEntity(Boolean.class);
		response.close();

		return result;
	}



	public Set<RecognyzeResult> searchText(String profileName, String data) throws ClientErrorException {
		return this.searchText(profileName, data, 0);
	}



	public Set<RecognyzeResult> searchText(String profileName, String data, int limit) throws ClientErrorException {

		Response response = super.target
				.path(SEARCHTEXTSERVICEURL + "?" + PROFILENAME + profileName + "&" + LIMIT + limit)
				.request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(data));

		super.checkResponseStatus(response);
		Set<RecognyzeResult> result = response
				.readEntity(new GenericType<Set<RecognyzeResult>>() {});
		response.close();

		return result;
	}



	public Set<RecognyzeResult> searchDocument(String profileName, Document data) throws ClientErrorException {

		return this.searchDocument(profileName, data, 0);
	}



	public Set<RecognyzeResult> searchDocument(String profileName, Document data, int limit)
			throws ClientErrorException {

		Response response = super.target
				.path(SEARCHDOCUMENTSERVICEURL + "?" + PROFILENAME + profileName + "&" + LIMIT + limit)
				.request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(data));

		super.checkResponseStatus(response);
		Set<RecognyzeResult> result = response
				.readEntity(new GenericType<Set<RecognyzeResult>>() {});
		response.close();

		return result;
	}



	public Map<String, Set<RecognyzeResult>> searchDocuments(String profileName, Set<Document> data)
			throws ClientErrorException {

		return this.searchDocuments(profileName, data, 0);
	}



	public Map<String, Set<RecognyzeResult>> searchDocuments(String profileName, Set<Document> data, int limit)
			throws ClientErrorException {
		
		Response response = super.target
				.path(SEARCHDOCUMENTSSERVICEURL + "?" + PROFILENAME + profileName + "&" + LIMIT + limit)
				.request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(data));

		super.checkResponseStatus(response);
		Map<String, Set<RecognyzeResult>> result = response
				.readEntity(new GenericType<Map<String, Set<RecognyzeResult>>>() {});
		response.close();

		return result;
	}



	public Map<String, Object> status() throws ClientErrorException {
		
		Response response = super.target.path(STATUSSERVICEURL)
				.request(MediaType.APPLICATION_JSON_TYPE)
				.get();

		super.checkResponseStatus(response);
		Map<String, Object> result = response
				.readEntity(new GenericType<Map<String, Object>>() {});
		response.close();

		return result;
	}
}