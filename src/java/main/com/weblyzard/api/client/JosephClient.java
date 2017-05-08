package com.weblyzard.api.client;

import java.util.List;

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
public class JosephClient extends BasicClient {

	private static final String LOAD_PROFILE_SERVICE_URL = "/joseph/rest/load_profile/";
	private static final String UNLOAD_PROFILE_SERVICE_URL = "/joseph/rest/unload_profile/";
	private static final String CLEAN_PROFILE_SERVICE_URL = "joseph/rest/clean/";
	private static final String CLASSIFY_SERVICE_URL = "/joseph/rest/classify/";
	private static final String TRAIN_SERVICE_URL = "/joseph/rest/train/";
	private static final String RETRAIN_SERVICE_URL = "/joseph/rest/retrain/";
	private static final String FORGET_SERVICE_URL = "/joseph/rest/forget/";



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
		Response response = super.getTarget().path(LOAD_PROFILE_SERVICE_URL + profileName)
				.request(MediaType.APPLICATION_JSON_TYPE).get();

		super.checkResponseStatus(response);
		boolean result = response.readEntity(Boolean.class);
		response.close();

		return result;
	}



	public boolean cleanProfile(String profileName) {
		Response response = super.getTarget().path(CLEAN_PROFILE_SERVICE_URL + profileName)
				.request(MediaType.APPLICATION_JSON_TYPE).get();

		super.checkResponseStatus(response);
		boolean result = response.readEntity(Boolean.class);
		response.close();

		return result;
	}



	public boolean unloadProfile(String profileName) {
		Response response = super.getTarget().path(UNLOAD_PROFILE_SERVICE_URL + profileName)
				.request(MediaType.APPLICATION_JSON_TYPE).get();

		super.checkResponseStatus(response);
		boolean result = response.readEntity(Boolean.class);
		response.close();

		return result;
	}



	public boolean train(String profileName, Document document, String category) {
		Response response = super.getTarget().path(TRAIN_SERVICE_URL + profileName + "/" + category)
				.request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(document));

		super.checkResponseStatus(response);
		boolean result = response.readEntity(Boolean.class);
		response.close();

		return result;
	}



	public boolean retrain(String profileName, Document document, String category) {
		Response response = super.getTarget().path(RETRAIN_SERVICE_URL + profileName + "/" + category)
				.request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(document));

		super.checkResponseStatus(response);
		boolean result = response.readEntity(Boolean.class);
		response.close();

		return result;
	}



	public boolean forget(String profileName, Document document, String category) {
		Response response = super.getTarget().path(FORGET_SERVICE_URL + profileName + "/" + category)
				.request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(document));

		super.checkResponseStatus(response);
		boolean result = response.readEntity(Boolean.class);
		response.close();

		return result;
	}



	public List<RecognyzeResult> classify(String profileName, Document request) {
		return this.classify(profileName, request, 0, false);
	}



	public List<RecognyzeResult> classify(String profileName, Document request, int limit, boolean withFeatures)
			throws WebApplicationException {

		Response response = super.getTarget().path(CLASSIFY_SERVICE_URL + profileName).queryParam("limit", limit)
				.queryParam("full", withFeatures).request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(request));

		super.checkResponseStatus(response);
		List<RecognyzeResult> result = response.readEntity(new GenericType<List<RecognyzeResult>>() {
		});
		response.close();

		return result;
	}

}
