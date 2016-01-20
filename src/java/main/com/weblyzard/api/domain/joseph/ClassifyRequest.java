package com.weblyzard.api.domain.joseph;

import java.util.Date;
import java.util.List;

import javax.xml.bind.annotation.XmlRootElement;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.weblyzard.api.domain.weblyzard.Document;

/**
 * Domain Transfer Object defining the interface for other services to use this
 * Webservice. DaoClassifyRequest is returned by the service after a
 * <code>webservice.classify()</code> call and contains the estimated
 * classification for the given featureSet and searchagents.
 * 
 * 
 * @author Philipp Kuntschik
 * 
 */
@XmlRootElement
@JsonIgnoreProperties(ignoreUnknown = true)
public class ClassifyRequest {

	public Document document;
	/**
	 * List of SearchAgents used by the classifier. This is necessary, there
	 * must be at least one searchagent.
	 */
	public List<Searchagent> searchAgents;

	/**
	 * Number of results that will be returned by the service. This is optional,
	 * if not set the number of results will be set to the value specified in
	 * defaultproperties.
	 */
	public int numOfResults;

	/**
	 * Timestamp of the document, used to learn and retrain the features to
	 * seasonal-knowledgebases. This is optional, if not set the current month
	 * will automatically be used.
	 */
	public Date documentTimeStamp;



	public ClassifyRequest() {
	}



	public ClassifyRequest setDocument(Document document) {
		this.document = document;
		return this;
	}



	public ClassifyRequest setNumOfResults(int numOfResults) {
		this.numOfResults = numOfResults;
		return this;
	}



	public ClassifyRequest setDocumentTimeStamp(Date documentTimeStamp) {
		this.documentTimeStamp = documentTimeStamp;
		return this;
	}



	public ClassifyRequest setSearchAgents(List<Searchagent> searchAgents) {
		this.searchAgents = searchAgents;
		return this;
	}
}
