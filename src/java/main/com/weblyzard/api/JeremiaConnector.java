package com.weblyzard.api;

import java.io.IOException;
import java.io.InputStream;

import javax.xml.bind.JAXBException;

import com.weblyzard.api.domain.weblyzard.Document;
import com.weblyzard.api.domain.weblyzard.XmlDocument;

import com.weblyzard.util.GSONHelper;
import com.weblyzard.util.http.HTTPPOST;

/**
 * 
 * @author philipp.kuntschik@htwchur.ch
 *
 */
public class JeremiaConnector extends BasicConnector {

	private static final String SUBMITDOCUMENTSERVICEURL = "/rest/submit_document";



	/**
	 * @see BasicConnector
	 */
	public JeremiaConnector() {
		super();
	}



	/**
	 * @see BasicConnector
	 */
	public JeremiaConnector(String weblyzard_url) {
		super(weblyzard_url);
	}



	/**
	 * @see BasicConnector
	 */
	public JeremiaConnector(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}



	public XmlDocument callSubmitDocumentRaw(Document data) throws IOException {

		String url = super.weblyzard_url + SUBMITDOCUMENTSERVICEURL;

		InputStream responseStream = HTTPPOST.requestJSON(url, GSONHelper.parseObject(data, Document.class),
				super.username, super.password, APPLICATIONJSON);

		return (XmlDocument) GSONHelper.parseInputStream(responseStream, XmlDocument.class);
	}



	public Document callSubmitDocument(Document data) throws IOException, JAXBException {
		XmlDocument response = callSubmitDocumentRaw(data);
		return new Document().unmarshal(response.xml_content);
	}
}
