package com.weblyzard.api.client;

import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import com.weblyzard.api.domain.joseph.ClassifyRequest;
import com.weblyzard.api.domain.joseph.ClassifyResponse;
import com.weblyzard.api.domain.joseph.LearnRequest;
import com.weblyzard.api.domain.joseph.LearnResponse;

public class JosephClient extends BasicClient {

	private static final String CLASSIFYSERVICEURL = "/joseph/rest/1/classify/";
	private static final String CLASSIFYEXTENDEDSERVICEURL = "/joseph/rest/enhancedClassify/";
	private static final String LEARNSERVICEURL = "/joseph/rest/learn/";



	/**
	 * @see BasicClient
	 */
	public JosephClient() {
		super();
	}



	/**
	 * @see BasicClient
	 */
	public JosephClient(String weblyzard_url) {
		super(weblyzard_url);
	}



	/**
	 * @see BasicClient
	 */
	public JosephClient(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}



	public ClassifyResponse[] classify(String profileName, ClassifyRequest request) {

		Response response = super.target.path(CLASSIFYSERVICEURL + profileName).request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(request));

		ClassifyResponse[] result = response.readEntity(ClassifyResponse[].class);
		response.close();

		return result;
	}



	public ClassifyResponse[] classifyExtended(String profileName, ClassifyRequest request) {

		Response response = super.target.path(CLASSIFYEXTENDEDSERVICEURL + profileName)
				.request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(request));

		ClassifyResponse[] result = response.readEntity(ClassifyResponse[].class);
		response.close();

		return result;
	}



	public LearnResponse call_learn(String profileName, LearnRequest request) {
		

		Response response = super.target.path(LEARNSERVICEURL + profileName)
				.request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(request));

		LearnResponse result = response.readEntity(LearnResponse.class);
		response.close();

		return result;
	}
}
