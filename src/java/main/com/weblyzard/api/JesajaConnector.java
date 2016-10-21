package com.weblyzard.api;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import javax.ws.rs.core.Response;
import javax.xml.bind.JAXBException;

import org.apache.http.auth.AuthenticationException;
import org.apache.http.client.ClientProtocolException;

import com.google.gson.reflect.TypeToken;
import com.weblyzard.api.domain.weblyzard.Document;
import com.weblyzard.util.GSONHelper;
import com.weblyzard.util.http.HTTPPOST;

public class JesajaConnector extends BasicConnector {

	private static final String GETKEYWORDS_SERVICEURL = "/jesaja/rest/get_keywords/";
	private static final String SETREFERENCECORPUS_SERVICEURL = "/jesaja/rest/add_csv/";
	private static final String ADDDOCUMENTS_SERVICEURL = "/jesaja/rest/add_documents/";
	private static final String GETNEKANNOTATIONS_SERVICEURL = "/jesaja/rest/get_nek_annotations/";



	/**
	 * @see BasicConnector
	 */
	public JesajaConnector() {
		super();
	}



	/**
	 * @see BasicConnector
	 */
	public JesajaConnector(String weblyzard_url) {
		super(weblyzard_url);
	}



	/**
	 * @see BasicConnector
	 */
	public JesajaConnector(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}



	public Response call_setReferenceCorpus(String matviewId, Map<String, Integer> corpusMapping)
			throws AuthenticationException, ClientProtocolException, IOException {

		String url = super.weblyzard_url + SETREFERENCECORPUS_SERVICEURL + matviewId;

		InputStream responseStream = HTTPPOST.requestJSON(url,
				GSONHelper.parseObject(corpusMapping, new TypeToken<Map<String, Integer>>() {
				}.getType()), super.username, super.password, APPLICATIONJSON);

		return (Response) GSONHelper.parseInputStream(responseStream, Response.class);
	}



	public Response call_addDocuments(String matviewId, List<Document> documents)
			throws AuthenticationException, ClientProtocolException, IOException {

		String url = super.weblyzard_url + ADDDOCUMENTS_SERVICEURL + matviewId;

		InputStream responseStream = HTTPPOST.requestJSON(url,
				GSONHelper.parseObject(documents, new TypeToken<List<Document>>() {
				}.getType()), super.username, super.password, APPLICATIONJSON);

		return (Response) GSONHelper.parseInputStream(responseStream, Response.class);
	}



	public Map<String, Map<String, Double>> call_getKeywords(String matviewId, List<Document> documents)
			throws AuthenticationException, ClientProtocolException, IOException {

		String url = super.weblyzard_url + GETKEYWORDS_SERVICEURL + matviewId;

		List<String> xml = new ArrayList<>();
		for (Document document : documents)
			try {
				xml.add(document.marshal());
			} catch (JAXBException e) {
				e.printStackTrace();
			}

		InputStream responseStream = HTTPPOST.requestJSON(url,
				GSONHelper.parseObject(xml, new TypeToken<List<String>>() {
				}.getType()), super.username, super.password, APPLICATIONJSON);

		return (Map<String, Map<String, Double>>) GSONHelper.parseInputStream(responseStream,
				new TypeToken<Map<String, Map<String, Double>>>() {
				}.getType());
	}

	// public JsonObject call_getNonEntityKeywordAnnotations(String matviewId,
	// List<Document> documents)
	// throws AuthenticationException, ClientProtocolException, IOException {
	//
	// String url = super.weblyzard_url + GETNEKANNOTATIONS_SERVICEURL +
	// matviewId;
	//
	// InputStream responseStream = HTTPPOST.requestJSON(url,
	// GSONHelper.parseObject(documents, new TypeToken<List<Document>>()
	// {}.getType()),
	// super.username, super.password, APPLICATIONJSON);
	//
	// return (JsonObject) GSONHelper.parseInputStream(responseStream,
	// JsonObject.class);
	// }

}
