package com.weblyzard.api.domain.joseph;

import java.util.Set;

import javax.xml.bind.annotation.XmlRootElement;

/**
 * Domain Transfer Object defining the interface for other services to use this
 * Webservice. DaoClassifyRequest is returned by the service after a
 * <code>webservice.classify()</code> call and contains the estimated
 * classification for the given featureSet and searchagents.
 * 
 * @author Philipp Kuntschik
 * 
 */
@XmlRootElement
public class ClassifyResponse {

	public int searchagent;
	public Set<Classification> classification;



	public ClassifyResponse() {
	}



	public ClassifyResponse setSearchagent(int searchagent) {
		this.searchagent = searchagent;
		return this;
	}



	public ClassifyResponse setClassification(Set<Classification> classification) {
		this.classification = classification;
		return this;
	}
}
