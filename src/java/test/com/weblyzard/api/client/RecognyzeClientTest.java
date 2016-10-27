package com.weblyzard.api.client;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import org.junit.Test;

import com.weblyzard.api.document.Document;
import com.weblyzard.api.recognize.RecognyzeResult;

public class RecognyzeClientTest {

	private static final String profile = "test";



	@Test
	public void testLoadProfile() {
		RecognyzeClient client = new RecognyzeClient();
		boolean result = client.loadProfile(profile);

		assertTrue(result);
	}



	@Test
	public void testText() {
		RecognyzeClient client = new RecognyzeClient();
		String request = "Fast Track's Karen Bowerman asks what the changes in penguin"
				+ " population could mean for the rest of us in the event of climate change.";

		Set<RecognyzeResult> result = client.searchText(profile, request);

		// TODO: validate that the resultset is not empty (compose a small test
		// profile, find a nice sentence to test)
		assertNotNull(result);
		assertTrue(result.size() >= 1);
	}



	@Test
	public void testSearchDocument() {
		RecognyzeClient client = new RecognyzeClient();
		Document request = new Document("Fast Track's Karen Bowerman asks what the changes in penguin population"
				+ " could mean for the rest of us in the event of climate change.");

		Set<RecognyzeResult> result = client.searchDocument(profile, request);
		// TODO: validate that the resultset is not empty (compose a small test
		// profile, find a nice sentence to test)
		assertNotNull(result);
		assertTrue(result.size() >= 1);
	}



	@Test
	public void testSearchDocuments() {
		RecognyzeClient client = new RecognyzeClient();
		Set<Document> request = new HashSet<>();
		request.add(new Document("Fast Track's Karen Bowerman asks what the changes in penguin population"
				+ " could mean for the rest of us in the event of climate change.").setId("1"));

		Map<String, Set<RecognyzeResult>> result = client.searchDocuments(profile, request);
		// TODO: validate that the resultset is not empty (compose a small test
		// profile, find a nice sentence to test)
		assertNotNull(result);
		assertTrue(result.size() >= 1);
		assertTrue(result.get("1").size() >= 1);
	}



	@Test
	public void testSearchDocumentsWithoutId() {
		RecognyzeClient client = new RecognyzeClient();
		Set<Document> request = new HashSet<>();
		request.add(new Document("Fast Track's Karen Bowerman asks what the changes in penguin population"
				+ " could mean for the rest of us in the event of climate change."));

		Map<String, Set<RecognyzeResult>> result = client.searchDocuments(profile, request);
		// TODO: validate that the resultset is not empty (compose a small test
		// profile, find a nice sentence to test)
		assertNotNull(result);
		assertTrue(result.size() == 0);
	}



	@Test
	public void testStatus() {
		RecognyzeClient client = new RecognyzeClient();

		Map<String, Object> result = client.status();
		// TODO: validate that the resultset is not empty (compose a small test
		// profile, find a nice sentence to test)
		assertNotNull(result);
	}
}
