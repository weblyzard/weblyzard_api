package com.weblyzard.api.client;

import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import com.weblyzard.api.joseph.ClassifyRequest;
import com.weblyzard.api.joseph.ClassifyResponse;
import com.weblyzard.api.joseph.LearnRequest;
import com.weblyzard.api.joseph.LearnResponse;

public class JosephClient extends BasicClient {

	private static final String CLASSIFY_SERVICE_URL = "/joseph/rest/1/classify/";
	private static final String CLASSIFY_EXTENDED_SERVICE_URL = "/joseph/rest/enhancedClassify/";
	private static final String LEARN_SERVICE_URL = "/joseph/rest/learn/";

	public JosephClient() {
		super();
	}

	public JosephClient(String weblyzard_url) {
		super(weblyzard_url);
	}

	public JosephClient(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}



	public ClassifyResponse[] classify(String profileName, ClassifyRequest request) throws WebApplicationException{

		Response response = super.getTarget().path(CLASSIFY_SERVICE_URL + profileName).request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(request));
		
		super.checkResponseStatus(response);
		ClassifyResponse[] result = response.readEntity(ClassifyResponse[].class);
		response.close();

		return result;
	}



	public ClassifyResponse[] classifyExtended(String profileName, ClassifyRequest request) throws WebApplicationException{

		Response response = super.getTarget().path(CLASSIFY_EXTENDED_SERVICE_URL + profileName)
				.request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(request));
		
		super.checkResponseStatus(response);
		ClassifyResponse[] result = response.readEntity(ClassifyResponse[].class);
		response.close();

		return result;
	}



	public LearnResponse learn(String profileName, LearnRequest request) throws WebApplicationException{
		

		Response response = super.getTarget().path(LEARN_SERVICE_URL + profileName)
				.request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(request));
		
		super.checkResponseStatus(response);
		LearnResponse result = response.readEntity(LearnResponse.class);
		response.close();

		return result;
	}
}
