package com.weblyzard.api;

import java.io.IOException;
import java.io.InputStream;
import java.util.Map;
import java.util.Set;

import javax.xml.bind.JAXBException;

import org.apache.http.auth.AuthenticationException;
import org.apache.http.client.ClientProtocolException;

import com.google.gson.reflect.TypeToken;
import com.weblyzard.api.domain.recognize.RecognyzeResult;
import com.weblyzard.api.domain.weblyzard.Document;
import com.weblyzard.util.GSONHelper;
import com.weblyzard.util.http.HTTPGET;
import com.weblyzard.util.http.HTTPPOST;

public class RecognyzeConnector extends BasicConnector {

	private static final String ADDPROFILESERVICEURL = "/Recognize/rest/load_profile/";
	private static final String SEARCHTEXTSERVICEURL = "/Recognize/rest/searchText";
	private static final String SEARCHDOCUMENTSERVICEURL = "/Recognize/rest/searchDocument";
	private static final String SEARCHDOCUMENTSSERVICEURL = "/Recognize/rest/searchDocuments";
	private static final String STATUSSERVICEURL = "/Recognize/rest/status";
	private static final String PROFILENAMES = "profileName=";
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



	public boolean call_loadProfile(String profileName)
			throws AuthenticationException, ClientProtocolException, IOException {

		String url = super.weblyzard_url + ADDPROFILESERVICEURL + profileName;

		InputStream responseStream = HTTPGET.requestJSON(url, super.username, super.password, APPLICATIONJSON);

		return (boolean) (GSONHelper.parseInputStream(responseStream, Boolean.class));
	}



	public Set<RecognyzeResult> call_searchText(String profileName, String data)
			throws AuthenticationException, ClientProtocolException, JAXBException, IOException {

		return this.call_searchText(profileName, data, 0);
	}



	public Set<RecognyzeResult> call_searchText(String profileName, String data, int limit)
			throws AuthenticationException, ClientProtocolException, JAXBException, IOException {

		String url = super.weblyzard_url + SEARCHTEXTSERVICEURL + "?" + PROFILENAMES + profileName + "&" + LIMIT + limit;

		InputStream responseStream = HTTPPOST.requestJSON(url, data,
				super.username, super.password, APPLICATIONJSON);

		return (Set<RecognyzeResult>) (GSONHelper.parseInputStream(responseStream,
				new TypeToken<Set<RecognyzeResult>>() {}.getType()));
	}



	public Set<RecognyzeResult> call_searchDocument(String profileName, Document data)
			throws AuthenticationException, ClientProtocolException, IOException {

		return this.call_searchDocument(profileName, data, 0);
	}



	public Set<RecognyzeResult> call_searchDocument(String profileName, Document data, int limit)
			throws AuthenticationException, ClientProtocolException, IOException {

		String url = super.weblyzard_url + SEARCHDOCUMENTSERVICEURL + "?" + PROFILENAMES + profileName + "&" + LIMIT
				+ limit;

		InputStream responseStream = HTTPPOST.requestJSON(url,GSONHelper.parseObject(data, Document.class), 
				super.username, super.password, APPLICATIONJSON);

		return (Set<RecognyzeResult>) (GSONHelper.parseInputStream(responseStream,
				new TypeToken<Set<RecognyzeResult>>() {}.getType()));
	}



	public Map<String, Set<RecognyzeResult>> call_searchDocuments(String profileName, Set<Document> data)
			throws AuthenticationException, ClientProtocolException, IOException {

		return this.call_searchDocuments(profileName, data, 0);
	}



	public Map<String, Set<RecognyzeResult>> call_searchDocuments(String profileName, Set<Document> data, int limit)
			throws AuthenticationException, ClientProtocolException, IOException {

		String url = super.weblyzard_url + SEARCHDOCUMENTSSERVICEURL + "?" + PROFILENAMES + profileName + "&" + LIMIT
				+ limit;

		InputStream responseStream = HTTPPOST.requestJSON(url,
				GSONHelper.parseObject(data, new TypeToken<Set<Document>>() {}.getType()), 
				super.username, super.password, APPLICATIONJSON);

		return (Map<String, Set<RecognyzeResult>>) (GSONHelper.parseInputStream(responseStream,
				new TypeToken<Map<String, Set<RecognyzeResult>>>() {}.getType()));
	}



	public Map<String, Object> call_status() throws AuthenticationException, ClientProtocolException, IOException {

		String url = super.weblyzard_url + STATUSSERVICEURL;

		InputStream responseStream = HTTPGET.requestJSON(url, super.username, super.password, APPLICATIONXML);

		return ((Map<String, Object>) GSONHelper.parseInputStream(responseStream, 
				new TypeToken<Map<String, Object>>() {}.getType()));
	}

}
