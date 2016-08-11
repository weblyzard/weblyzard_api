package com.weblyzard.api;

import static org.junit.Assert.*;

import java.io.IOException;

import javax.xml.bind.JAXBException;

import org.apache.http.auth.AuthenticationException;
import org.apache.http.client.ClientProtocolException;
import org.junit.Test;

import com.google.gson.JsonElement;
import com.weblyzard.api.domain.weblyzard.Document;

public class RecognyzeConnectorTest {

	RecognyzeConnector connector = new RecognyzeConnector();
	String profile = "yourprofilename";



	@Test
	public void testAddProfile() throws AuthenticationException, ClientProtocolException, IOException, JAXBException {
		assertTrue(loadProfile(profile));
	}



	@Test
	public void testSearchXml() throws AuthenticationException, ClientProtocolException, IOException, JAXBException {
		JsonElement element = searchXml(profile, new Document());
		return;
	}

	private boolean loadProfile(String profileName)
			throws AuthenticationException, ClientProtocolException, IOException, JAXBException {
		return connector.callLoadProfile(profileName);
	}



	private JsonElement searchXml(String profileName, Document data)
			throws AuthenticationException, ClientProtocolException, IOException, JAXBException {
		return connector.callSearchXML(profileName, data);
	}

}
