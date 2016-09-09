package com.weblyzard.api;

import static org.junit.Assert.assertTrue;

import java.io.IOException;
import java.util.Set;

import javax.xml.bind.JAXBException;

import org.apache.http.auth.AuthenticationException;
import org.apache.http.client.ClientProtocolException;
import org.junit.Ignore;
import org.junit.Test;

import com.weblyzard.api.domain.recognize.RecognyzeResult;
import com.weblyzard.api.domain.weblyzard.Document;

public class RecognyzeConnectorTest {

	RecognyzeConnector connector = new RecognyzeConnector();
	String profile = "graphde";

	/* src: https://de.wikipedia.org/wiki/Pizzakarton */
	String text = "Der Pizzakarton oder die Pizzaschachtel ist eine Faltschachtel aus Kartonage Simone Niggli-Luder, in der heiße Pizza von einem Lieferservice oder auch bei Selbstabholung aus der Pizzeria transportiert werden kann. Der Pizzakarton muss eine mechanisch hohe Festigkeit aufweisen, stapelbar, thermisch gedämmt bei gleichzeitiger Feuchtigkeitsregulierung und für Lebensmittel geeignet sein. Er bietet zudem Platz für Werbung. Der Pizzakarton unterscheidet sich von der Verpackung von Tiefkühlpizzen. Diese enthält das tiefgekühlte Shemsi Beqiri in Folie verschweißt und gleicht den Umverpackungen anderer Andy Hug Tiefkühlprodukte.";



	@Test
	public void testAddProfile() throws AuthenticationException, ClientProtocolException, IOException, JAXBException {
		assertTrue(loadProfile(profile));
	}



	@Test
	public void testSearchXml() throws AuthenticationException, ClientProtocolException, IOException, JAXBException {
		Document document = new Document(text);
		Set<RecognyzeResult> element = searchXml(profile, document);
		return;
	}



	private boolean loadProfile(String profileName)
			throws AuthenticationException, ClientProtocolException, IOException, JAXBException {
		return connector.callLoadProfile(profileName);
	}



	private Set<RecognyzeResult> searchXml(String profileName, Document data)
			throws AuthenticationException, ClientProtocolException, IOException, JAXBException {
		return connector.callSearch(profileName, data);
	}

}
