package com.weblyzard.api.client;

import javax.ws.rs.ClientErrorException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import com.weblyzard.api.joseph.ClassifyRequest;
import com.weblyzard.api.joseph.ClassifyResponse;
import com.weblyzard.api.joseph.LearnRequest;
import com.weblyzard.api.joseph.LearnResponse;

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



	public ClassifyResponse[] classify(String profileName, ClassifyRequest request) throws ClientErrorException{

		Response response = super.target.path(CLASSIFYSERVICEURL + profileName).request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(request));
		
		super.checkResponseStatus(response);
		ClassifyResponse[] result = response.readEntity(ClassifyResponse[].class);
		response.close();

		return result;
	}



	public ClassifyResponse[] classifyExtended(String profileName, ClassifyRequest request) throws ClientErrorException{

		Response response = super.target.path(CLASSIFYEXTENDEDSERVICEURL + profileName)
				.request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(request));
		
		super.checkResponseStatus(response);
		ClassifyResponse[] result = response.readEntity(ClassifyResponse[].class);
		response.close();

		return result;
	}



	public LearnResponse learn(String profileName, LearnRequest request) throws ClientErrorException{
		

		Response response = super.target.path(LEARNSERVICEURL + profileName)
				.request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(request));
		
		super.checkResponseStatus(response);
		LearnResponse result = response.readEntity(LearnResponse.class);
		response.close();

		return result;
	}
}