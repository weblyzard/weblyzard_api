package com.weblyzard.api.client;

import static org.junit.Assert.assertTrue;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.logging.Logger;

import javax.ws.rs.client.Entity;

import org.junit.Before;
import org.junit.Test;

import com.weblyzard.api.document.annotation.Annotation;
import com.weblyzard.api.jairo.Profile;
import com.weblyzard.api.jairo.RDFPrefix;

public class JairoClientTest {

	private JairoClient jairoClient; 
	
	private Profile mockImagineProfile; 
	private String mockJairoProfileName = "IMAGINE";
	private List<Annotation> mockImagineAnnotations; 
	
	private Logger logger = Logger.getLogger(getClass().getName());
	
	@Before
	public void before() {
		jairoClient = new JairoClient(); 
		initMockObjects();
	}
	
	
	@Test
	public void testJairoWorkflow() {
		
		// add a profile 
		jairoClient.addProfile(mockImagineProfile, mockJairoProfileName); 
		
		// list loaded profiles 
		jairoClient.listProfiles();
		
		// extend the annotations
		List<Annotation> extendedAnnotations = jairoClient.extendAnnotations(mockJairoProfileName, mockImagineAnnotations);
		
		logger.info(Entity.json(extendedAnnotations).toString()); 
		
	}
	
	@Test 
	public void testRDFPrefixes() {
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
		jairoClient.addProfile(mockImagineProfile, mockJairoProfileName);
		List<Annotation> annotations = new ArrayList<>(
				Arrays.asList(new Annotation().setKey("<http://dbpedia.org/resource/Aurora_(singer)>")));
		List<Annotation> result = jairoClient.extendAnnotations(mockJairoProfileName, annotations);
		assertTrue(result.size() > 0);
	}

	@Test
	public void testExtendAnnotation2() {
		JairoClient client = new JairoClient();
		List<Annotation> annotations = new ArrayList<>(
				Arrays.asList(
						new Annotation().setKey("<http://dbpedia.org/resource/Feusisberg>"),
						new Annotation().setKey("<http://dbpedia.org/resource/Shani_Tarashaj>"),
						new Annotation().setKey("<http://dbpedia.org/resource/Grasshopper_Club_Zürich__Shani_Tarashaj__1>"),
						new Annotation().setKey("<http://dbpedia.org/resource/Bruno_Schweizer>")));
		List<Annotation> result = client.extendAnnotations(mockJairoProfileName, annotations);
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
