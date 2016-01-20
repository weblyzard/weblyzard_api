package com.weblyzard.api;

import java.io.IOException;
import java.io.InputStream;

import org.apache.http.auth.AuthenticationException;

import com.weblyzard.api.domain.joseph.ClassifyRequest;
import com.weblyzard.api.domain.joseph.ClassifyResponse;
import com.weblyzard.api.domain.joseph.LearnRequest;
import com.weblyzard.api.domain.joseph.LearnResponse;
import com.weblyzard.util.GSONHelper;
import com.weblyzard.util.http.HTTPPOST;

public class JosephConnector extends BasicConnector {

	private static final String CLASSIFYSERVICEURL = "/rest/1/classify/";
	private static final String LEARNSERVICEURL = "/rest/learn/";



	/**
	 * @see BasicConnector
	 */
	public JosephConnector() {
		super();
	}



	/**
	 * @see BasicConnector
	 */
	public JosephConnector(String weblyzard_url) {
		super(weblyzard_url);
	}



	/**
	 * @see BasicConnector
	 */
	public JosephConnector(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}



	public ClassifyResponse[] callClassify(String profileName, ClassifyRequest request) throws IOException, AuthenticationException {

		String url = super.weblyzard_url + CLASSIFYSERVICEURL + profileName;

		InputStream responseStream = HTTPPOST.requestJSON(url, GSONHelper.parseObject(request, ClassifyRequest.class),
				super.username, super.password, APPLICATIONJSON);

		return (ClassifyResponse[]) GSONHelper.parseInputStream(responseStream, ClassifyResponse[].class);
	}



	public LearnResponse callLearn(String profileName, LearnRequest request) throws IOException, AuthenticationException {

		String url = super.weblyzard_url + LEARNSERVICEURL + profileName;

		InputStream responseStream = HTTPPOST.requestJSON(url, GSONHelper.parseObject(request, LearnRequest.class),
				super.username, super.password, APPLICATIONJSON);

		return (LearnResponse) GSONHelper.parseInputStream(responseStream, LearnResponse.class);
	}
}
