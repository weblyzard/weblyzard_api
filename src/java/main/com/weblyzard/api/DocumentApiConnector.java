package com.weblyzard.api;

import java.io.IOException;
import java.io.InputStream;

import org.apache.http.auth.AuthenticationException;

import com.weblyzard.api.domain.document_api.Request;
import com.weblyzard.api.domain.document_api.Response;
import com.weblyzard.util.GSONHelper;
import com.weblyzard.util.http.HTTPPOST;

/**
 * TODO: untested!
 * 
 * @author philipp.kuntschik@htwchur.ch
 *
 */
public class DocumentApiConnector extends BasicConnector {

	private static final String WEBLYZARDDOCUMENTAPIURL = "";



	/**
	 * @see BasicConnector
	 */
	public DocumentApiConnector() {
		super();
	}



	/**
	 * @see BasicConnector
	 */
	public DocumentApiConnector(String weblyzard_url) {
		super(weblyzard_url);
	}



	/**
	 * @see BasicConnector
	 */
	public DocumentApiConnector(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}



	public Response callInsertNewDocument(Request request) throws IOException, AuthenticationException {

		String url = super.weblyzard_url + WEBLYZARDDOCUMENTAPIURL;

		InputStream responseStream = HTTPPOST.requestJSON(url, GSONHelper.parseObject(request, Request.class),
				super.username, super.password, APPLICATIONJSON);

		return (Response) GSONHelper.parseInputStream(responseStream, Response.class);
	}
}