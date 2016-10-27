package com.weblyzard.api.client.joel;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;
import java.util.zip.GZIPInputStream;


import org.junit.Before;

import com.weblyzard.api.document.Document;

import javax.json.Json; 
import javax.json.stream.JsonParser; 
import javax.json.stream.JsonParser.Event;

/**
 * 
 * @author Norman Suesstrunk
 *
 */
public class JoelTestBase {
	
	public static final String PSALMS_DOCS_WEBLYZARDFORMAT_JSON_GZ = "psalms-docs-weblyzardformat.json.gz";

	public Logger logger = Logger.getLogger(getClass().getName());
	
	public File ROOT_PATH = new File(this.getClass().getResource("/").getFile());
	
	public List<Document> psalmDocs;
	
	
	@Before
	public void before() {
		psalmDocs = readWeblyzardDocumentsFromZip(); 
	}
	
	public List<Document> readWeblyzardDocumentsFromZip() {
		try {
			List<Document> docs = new ArrayList<>();
			JsonParser jsonParser = Json.createParser(new GZIPInputStream(
					JoelTestBase.class.getClassLoader().getResourceAsStream(PSALMS_DOCS_WEBLYZARDFORMAT_JSON_GZ)));
			while (jsonParser.hasNext()) {
				Event xmlDocument = jsonParser.next();
				if (xmlDocument.equals(Event.VALUE_STRING)) {
					docs.add(Document.unmarshallDocumentXMLString(jsonParser.getString()));
				}
			}
			return docs;
		} catch (IOException e) {
			e.printStackTrace();
			return null; 
		}
	}

}
