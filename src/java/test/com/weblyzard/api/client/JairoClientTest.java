package com.weblyzard.api.client;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.junit.Assume.assumeTrue;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.logging.Logger;

import org.junit.Before;
import org.junit.Test;

import com.weblyzard.api.document.annotation.Annotation;
import com.weblyzard.api.jairo.Profile;
import com.weblyzard.api.jairo.RDFPrefix;

public class JairoClientTest extends TestClientBase{

	private JairoClient jairoClient; 
	
	private Profile mockImagineProfile; 
	private String mockJairoProfileName = "IMAGINE";
	private List<Annotation> mockImagineAnnotations; 
	
	@SuppressWarnings("unused")
	private Logger logger = Logger.getLogger(getClass().getName());
	
	@Before
	public void before() {
		jairoClient = new JairoClient(); 
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
		List<Annotation> extendedAnnotations = jairoClient.extendAnnotations(mockJairoProfileName, mockImagineAnnotations);
		
		assertNotNull(extendedAnnotations); 
		
	}
	
	@Test 
	public void testRDFPrefixes() {
		
		assumeTrue(weblyzardServiceAvailable(jairoClient));
		
		RDFPrefix rdfPrefix;
		try {
			rdfPrefix = new RDFPrefix("dbr", new URI("http://dbpedia.org/resource/"));
			
			// list the rdf prefixes 
			assertTrue(jairoClient.listRdfPrefixes().size()>0);
			
			// add a rdf prefix 
			jairoClient.addPrefix(rdfPrefix); 
			
			// check if the prefix was added
			assertTrue(jairoClient.listRdfPrefixes().containsKey(rdfPrefix.getPrefix())); 
		} catch (URISyntaxException e) {
			e.printStackTrace();
		}
	}
		
	
	/**
	 * Tests from phil
	 */
	@Test
	public void testExtendAnnotation1() {
		
		assumeTrue(weblyzardServiceAvailable(jairoClient));
		
		jairoClient.addProfile(mockImagineProfile, mockJairoProfileName);
		List<Annotation> annotations = new ArrayList<>(
				Arrays.asList(new Annotation().setKey("<http://dbpedia.org/resource/Aurora_(singer)>")));
		List<Annotation> result = jairoClient.extendAnnotations(mockJairoProfileName, annotations);
		assertTrue(result.size() > 0);

		annotations = Arrays.asList(new Annotation().setKey("<http://dbpedia.org/resource/Feusisberg>"),
				new Annotation().setKey("<http://dbpedia.org/resource/Shani_Tarashaj>"),
				new Annotation().setKey("<http://dbpedia.org/resource/Grasshopper_Club_Zürich__Shani_Tarashaj__1>"),
				new Annotation().setKey("<http://dbpedia.org/resource/Bruno_Schweizer>"));
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
		mockImagineProfile.addType("?type", "type");
		
		// init the annotations
		mockImagineAnnotations = new ArrayList<>();
		mockImagineAnnotations.add(new Annotation("<http://dbpedia.org/resourceVevey>", null, null, 0, 0, null)); 
		mockImagineAnnotations.add(new Annotation("<http://dbpedia.org/resource/Sarnen>", null, null, 0, 0, null));
		mockImagineAnnotations.add(new Annotation("<http://dbpedia.org/resource/Die_(musician)>", null, null, 0, 0, null));
		
	}
}
