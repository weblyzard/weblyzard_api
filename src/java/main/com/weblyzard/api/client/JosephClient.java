package com.weblyzard.api.client;

import java.io.IOException;
import java.io.InputStream;

import org.apache.http.auth.AuthenticationException;

import com.weblyzard.api.domain.joseph.ClassifyRequest;
import com.weblyzard.api.domain.joseph.ClassifyResponse;
import com.weblyzard.api.domain.joseph.LearnRequest;
import com.weblyzard.api.domain.joseph.LearnResponse;
import com.weblyzard.util.GSONHelper;
import com.weblyzard.util.http.HTTPPOST;

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



	public ClassifyResponse[] call_classify(String profileName, ClassifyRequest request)
			throws IOException, AuthenticationException {

		String url = super.weblyzard_url + CLASSIFYSERVICEURL + profileName;

		InputStream responseStream = HTTPPOST.requestJSON(url, GSONHelper.parseObject(request, ClassifyRequest.class),
				super.username, super.password, APPLICATIONJSON);

		return (ClassifyResponse[]) GSONHelper.parseInputStream(responseStream, ClassifyResponse[].class);
	}

	
	public ClassifyResponse[] call_classifyExtended(String profileName, ClassifyRequest request)
			throws IOException, AuthenticationException {

		String url = super.weblyzard_url + CLASSIFYEXTENDEDSERVICEURL + profileName;

		InputStream responseStream = HTTPPOST.requestJSON(url, GSONHelper.parseObject(request, ClassifyRequest.class),
				super.username, super.password, APPLICATIONJSON);

		return (ClassifyResponse[]) GSONHelper.parseInputStream(responseStream, ClassifyResponse[].class);
	}


	public LearnResponse call_learn(String profileName, LearnRequest request)
			throws IOException, AuthenticationException {

		String url = super.weblyzard_url + LEARNSERVICEURL + profileName;

		InputStream responseStream = HTTPPOST.requestJSON(url, GSONHelper.parseObject(request, LearnRequest.class),
				super.username, super.password, APPLICATIONJSON);

		return (LearnResponse) GSONHelper.parseInputStream(responseStream, LearnResponse.class);
	}
}
