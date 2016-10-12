package com.weblyzard.api;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

import javax.ws.rs.core.Response;
import javax.xml.bind.JAXBException;

import org.apache.http.auth.AuthenticationException;

import com.google.gson.JsonObject;
import com.google.gson.reflect.TypeToken;
import com.weblyzard.api.domain.weblyzard.Document;
import com.weblyzard.util.GSONHelper;
import com.weblyzard.util.http.HTTPGET;
import com.weblyzard.util.http.HTTPPOST;

/**
 * 
 * @author philipp.kuntschik@htwchur.ch
 *
 */
public class JoelConnector extends BasicConnector {

	private static final String ADDDOCUMENTSSERVICEURL = "/joel/rest/addDocuments";
	private static final String CLUSTERDOCUMENTSERVICEURL = "/joel/rest/cluster";
	private static final String FLUSHDOCUMENTSERVICEURL = "/joel/rest/flush";



	/**
	 * @see BasicConnector
	 */
	public JoelConnector() {
		super();
	}



	/**
	 * @see BasicConnector
	 */
	public JoelConnector(String weblyzard_url) {
		super(weblyzard_url);
	}



	/**
	 * @see BasicConnector
	 */
	public JoelConnector(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}



	public Response call_addDocuments(List<Document> documents) throws IOException, AuthenticationException {
		String url = super.weblyzard_url + ADDDOCUMENTSSERVICEURL;

		List<String> xml = new ArrayList<>();
		for (Document document : documents)
			try {
				xml.add(document.marshal());
			} catch (JAXBException e) {
				e.printStackTrace();
			}
		// TODO: compare xml with documents (size, .. )

		InputStream responseStream = HTTPPOST.requestJSON(url, GSONHelper.parseObject(xml, 
				new TypeToken<List<String>>() {}.getType()),
				super.username, super.password, APPLICATIONJSON);

		return (Response) GSONHelper.parseInputStream(responseStream, Response.class);
	}



	public Response call_flush() throws AuthenticationException, IllegalStateException, IOException {
		String url = super.weblyzard_url + FLUSHDOCUMENTSERVICEURL;

		InputStream responseStream = HTTPGET.requestJSON(url, super.username, super.password, APPLICATIONJSON);

		return (Response) GSONHelper.parseInputStream(responseStream, Response.class);
	}



	public JsonObject call_cluster() throws AuthenticationException, IllegalStateException, IOException {
		String url = super.weblyzard_url + CLUSTERDOCUMENTSERVICEURL;

		InputStream responseStream = HTTPGET.requestJSON(url, super.username, super.password, APPLICATIONJSON);

		return (JsonObject) GSONHelper.parseInputStream(responseStream, JsonObject.class);
	}
}
