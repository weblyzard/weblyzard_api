package com.weblyzard.api.client.legacy;

import java.io.IOException;
import java.io.InputStream;

import javax.xml.bind.JAXBException;

import org.apache.http.auth.AuthenticationException;

import com.weblyzard.api.client.BasicClient;
import com.weblyzard.api.domain.weblyzard.Document;
import com.weblyzard.api.domain.weblyzard.XmlDocument;
import com.weblyzard.util.GSONHelper;
import com.weblyzard.util.http.HTTPPOST;

/**
 * 
 * @author philipp.kuntschik@htwchur.ch
 *
 */
public class JeremiaConnector extends BasicClient {

	private static final String SUBMITDOCUMENTSERVICEURL = "/jeremia/rest/submit_document";



	/**
	 * @see BasicClient
	 */
	public JeremiaConnector() {
		super();
	}



	/**
	 * @see BasicClient
	 */
	public JeremiaConnector(String weblyzard_url) {
		super(weblyzard_url);
	}



	/**
	 * @see BasicClient
	 */
	public JeremiaConnector(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}



	public XmlDocument call_submitDocumentRaw(Document data) throws IOException, AuthenticationException {

		String url = super.weblyzard_url + SUBMITDOCUMENTSERVICEURL;

		InputStream responseStream = HTTPPOST.requestJSON(url, GSONHelper.parseObject(data, Document.class),
				super.username, super.password, APPLICATIONJSON);

		return (XmlDocument) GSONHelper.parseInputStream(responseStream, XmlDocument.class);
	}



	public Document call_submitDocument(Document data) throws IOException, JAXBException, AuthenticationException {
		XmlDocument response = call_submitDocumentRaw(data);
		return new Document().unmarshal(response.xml_content);
	}
}
