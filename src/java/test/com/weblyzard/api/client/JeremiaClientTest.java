package com.weblyzard.api.client;

import static org.junit.Assert.assertNotNull;

import org.junit.Test;

import com.weblyzard.api.document.Document;

public class JeremiaClientTest {

	@Test
	public void testSubmitDocument() {
		JeremiaClient client = new JeremiaClient();
		Document request = new Document(
				"Fast Track's Karen Bowerman asks what the changes in penguin population could mean for the rest of us in the event of climate change.");
		request.setLang("en");

		Document response = client.submitDocument(request);
		assertNotNull(response);
	}

}
