package com.weblyzard.api.client.integration;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;
import java.util.Arrays;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import com.google.common.collect.ImmutableList;
import com.weblyzard.api.client.JairoClient;
import com.weblyzard.api.client.WebserviceClientConfig;
import com.weblyzard.api.model.annotation.Annotation;
import com.weblyzard.api.model.jairo.Profile;

public class JairoClientIT extends TestClientBase {

    private JairoClient jairoClient;

    private Profile mockImagineProfile;
    private String mockJairoProfileName = "IMAGINE";
    private List<Annotation> mockImagineAnnotations;

    @BeforeEach
    public void before() {
        jairoClient = new JairoClient(new WebserviceClientConfig());
        initMockObjects();
    }

    @Test
    public void testJairoWorkflow() {

        assumeTrue(weblyzardServiceAvailable(jairoClient));

        // add a profile
        jairoClient.addProfile(mockImagineProfile, mockJairoProfileName);

        // list loaded profiles
        jairoClient.listProfiles();

        // extend the annotations
        List<Annotation> extendedAnnotations =
                        jairoClient.extendAnnotations(mockJairoProfileName, mockImagineAnnotations);

        assertNotNull(extendedAnnotations);
    }

    /** 
     * Tests from phil.  
     */
    @Test
    public void testExtendAnnotation1() {

        assumeTrue(weblyzardServiceAvailable(jairoClient));

        jairoClient.addProfile(mockImagineProfile, mockJairoProfileName);
        List<Annotation> annotations = Arrays
                        .asList((Annotation) new Annotation().setKey("<http://dbpedia.org/resource/Aurora_(singer)>"));
        List<Annotation> result = jairoClient.extendAnnotations(mockJairoProfileName, annotations);
        assertTrue(!result.isEmpty());

        annotations = Arrays.asList((Annotation) new Annotation().setKey("<http://dbpedia.org/resource/Feusisberg>"),
                        (Annotation) new Annotation().setKey("<http://dbpedia.org/resource/Shani_Tarashaj>"),
                        (Annotation) new Annotation().setKey(
                                        "<http://dbpedia.org/resource/Grasshopper_Club_Zürich__Shani_Tarashaj__1>"),
                        (Annotation) new Annotation().setKey("<http://dbpedia.org/resource/Bruno_Schweizer>"));
        result = jairoClient.extendAnnotations(mockJairoProfileName, annotations);
        assertTrue(result != null);
    }

    public void initMockObjects() {

        // init the profile
        mockImagineProfile = new Profile();
        mockImagineProfile.setQuery("SELECT ?type WHERE { <key> rdf:type ?type }");

        // moses dbpedia
        // mockImagineProfile.setSparqlEndpoint("https://moses.semanticlab.net/rdf4j-server/repositories/en.dbpedia.201510.1");
        // dbpedia official
        mockImagineProfile.setSparqlEndpoint("http://dbpedia.org/sparql");

        // init the annotations
        mockImagineAnnotations = ImmutableList.of(
                        Annotation.build("<http://dbpedia.org/resourceVevey>").setStart(0).setEnd(0).setSentence(0),
                        Annotation.build("<http://dbpedia.org/resource/Sarnen>").setStart(0).setEnd(0).setSentence((0)),
                        Annotation.build("<http://dbpedia.org/resource/Die_(musician)>").setStart(0).setEnd(0)
                                        .setSentence((0)));
    }
}
