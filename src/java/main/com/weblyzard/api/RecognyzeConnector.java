package com.weblyzard.api;

import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.List;

import javax.xml.bind.JAXBException;

import org.apache.http.auth.AuthenticationException;
import org.apache.http.client.ClientProtocolException;

import com.google.gson.JsonElement;
import com.weblyzard.api.domain.weblyzard.Document;
import com.weblyzard.util.GSONHelper;
import com.weblyzard.util.http.HTTPGET;
import com.weblyzard.util.http.HTTPPOST;

public class RecognyzeConnector extends BasicConnector {

	private static final String ADDPROFILESERVICEURL = "/recognize/rest/recognize/add_profile/";
	private static final String SEARCHXMLSERVICEURL = "/recognize/rest/recognize/searchXml";
	private static final String PROFILENAMES = "profileNames=";
	private static final String LIMIT = "limit=";



	/**
	 * @see BasicConnector
	 */
	public RecognyzeConnector() {
		super();
	}



	/**
	 * @see BasicConnector
	 */
	public RecognyzeConnector(String weblyzard_url) {
		super(weblyzard_url);
	}



	/**
	 * @see BasicConnector
	 */
	public RecognyzeConnector(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}



	public void callAddProfile(String profileName)
			throws AuthenticationException, ClientProtocolException, IOException {
		
		String url = super.weblyzard_url + ADDPROFILESERVICEURL + profileName;
		
		HTTPGET.requestJSON(url, super.username, super.password, APPLICATIONXML);
	}



	public JsonElement callSearchXML(String profileName, Document data)
			throws AuthenticationException, ClientProtocolException, JAXBException, IOException {
		
		return callSearchXML(profileName, data, 999);
	}



	public JsonElement callSearchXML(String profileName, Document data, int limit)
			throws AuthenticationException, ClientProtocolException, JAXBException, IOException {
		
		return callSearchXML(Arrays.asList(profileName), data, limit);
	}



	public JsonElement callSearchXML(List<String> profileNames, Document data)
			throws AuthenticationException, ClientProtocolException, JAXBException, IOException {
		
		return callSearchXML(profileNames, data, 999);
	}



	public JsonElement callSearchXML(List<String> profileNames, Document data, int limit)
			throws AuthenticationException, JAXBException, ClientProtocolException, IOException {

		String url = super.weblyzard_url + SEARCHXMLSERVICEURL + "?";
		for (String profileName : profileNames)
			url += PROFILENAMES + profileName + "&";
		url += LIMIT + limit;

		InputStream responseStream = HTTPPOST.requestJSON(url, data.marshal(), super.username, super.password,
				APPLICATIONXML);

		return ((JsonElement) GSONHelper.parseInputStream(responseStream, JsonElement.class));
	}
}
