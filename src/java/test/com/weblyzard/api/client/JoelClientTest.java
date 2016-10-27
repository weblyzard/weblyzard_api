package com.weblyzard.api.client;

import static org.junit.Assert.assertNotNull;

import java.util.ArrayList;
import java.util.List;

import javax.ws.rs.core.Response;

import org.junit.Test;

import com.weblyzard.api.document.Document;

public class JoelClientTest {

	@Test
	public void testAddDocument() {
		JoelClient client = new JoelClient();
		List<Document> request = new ArrayList<>();
		request.add(new Document("Fast Track's Karen Bowerman asks what the changes in penguin population"
				+ " could mean for the rest of us in the event of climate change."));

		Response result = client.addDocuments(request);
		assertNotNull(result);
	}
}
