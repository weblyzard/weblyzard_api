package com.weblyzard.api;

import java.io.IOException;
import java.io.InputStream;

import javax.xml.bind.JAXBException;

import org.apache.http.auth.AuthenticationException;
import org.apache.http.client.ClientProtocolException;

import com.google.gson.JsonElement;
import com.weblyzard.api.domain.recognize.RecognyzeResult;
import com.weblyzard.api.domain.weblyzard.Document;
import com.weblyzard.util.GSONHelper;
import com.weblyzard.util.http.HTTPGET;
import com.weblyzard.util.http.HTTPPOST;

public class RecognyzeConnector extends BasicConnector {

	private static final String ADDPROFILESERVICEURL = "/Recognize/rest/recognize/load_profile/";
	private static final String SEARCHXMLSERVICEURL = "/Recognize/rest/recognize/searchXml";
	private static final String STATUSSERVICEURL = "/Recognize/rest/recognize/status";
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



	public boolean callLoadProfile(String profileName)
			throws AuthenticationException, ClientProtocolException, IOException {

		String url = super.weblyzard_url + ADDPROFILESERVICEURL + profileName;

		InputStream responseStream = HTTPGET.requestJSON(url, super.username, super.password, APPLICATIONJSON);
		return (boolean) (GSONHelper.parseInputStream(responseStream, Boolean.class));
	}



	public RecognyzeResult[] callSearch(String profileName, Document data)
			throws AuthenticationException, ClientProtocolException, JAXBException, IOException {

		return callSearch(profileName, data, 999);
	}



	public RecognyzeResult[] callSearch(String profileName, Document data, int limit)
			throws AuthenticationException, ClientProtocolException, JAXBException, IOException {

		String url = super.weblyzard_url + SEARCHXMLSERVICEURL + "?" + PROFILENAMES + profileName + "&" + LIMIT + limit;

		InputStream responseStream = HTTPPOST.requestJSON(url, data.marshal(), super.username, super.password,
				APPLICATIONXML);

		return (RecognyzeResult[]) (GSONHelper.parseInputStream(responseStream, RecognyzeResult[].class));
	}



	public JsonElement callStatus() throws AuthenticationException, ClientProtocolException, IOException {

		String url = super.weblyzard_url + STATUSSERVICEURL;

		InputStream responseStream = HTTPGET.requestJSON(url, super.username, super.password, APPLICATIONXML);

		return ((JsonElement) GSONHelper.parseInputStream(responseStream, JsonElement.class));
	}
}
