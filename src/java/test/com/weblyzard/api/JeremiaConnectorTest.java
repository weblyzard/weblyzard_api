package com.weblyzard.api;

import java.io.IOException;

import javax.xml.bind.JAXBException;

import org.apache.http.auth.AuthenticationException;
import org.apache.http.client.ClientProtocolException;
import org.junit.Test;

import com.weblyzard.api.domain.weblyzard.Document;

public class JeremiaConnectorTest {

	JeremiaConnector connector = new JeremiaConnector();

	String title = "Your test title";
	String body = "Your test body";



	@Test
	public void testSubmitDocument()
			throws AuthenticationException, ClientProtocolException, IOException, JAXBException {
		Document response = connector.call_submitDocument(new Document(title, body));
		return;
	}
}
