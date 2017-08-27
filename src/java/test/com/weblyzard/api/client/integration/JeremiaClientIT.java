package com.weblyzard.api.client.integration;

import static org.junit.Assert.assertNotNull;

import com.weblyzard.api.client.JeremiaClient;
import com.weblyzard.api.model.document.Document;
import javax.ws.rs.ClientErrorException;
import javax.xml.bind.JAXBException;
import org.junit.Before;
import org.junit.Test;

public class JeremiaClientIT extends TestClientBase {

    private JeremiaClient jeremiaClient;

    @Before
    public void before() {
        jeremiaClient = new JeremiaClient();
    }

    @Test
    public void testSubmitDocument() throws ClientErrorException, JAXBException {
        //assumeTrue(weblyzardServiceAvailable(jeremiaClient));
        Document request =
                new Document(
                        "Fast Track's Karen Bowerman asks what the changes in penguin population could mealenn for the rest of us in the event of climate change.");
        request.setLang("en");
        Document response1 = jeremiaClient.submitDocument(request);
        assertNotNull(response1);
    }
}
