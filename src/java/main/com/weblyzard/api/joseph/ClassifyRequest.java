package com.weblyzard.api.joseph;

import java.util.Date;
import java.util.List;

import javax.xml.bind.JAXBException;
import javax.xml.bind.annotation.XmlRootElement;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.weblyzard.api.document.Document;

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

	@JsonIgnore
	private Document document;

	private String xml_document;
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
	@Deprecated
	public int numOfResults;

	/**
	 * Timestamp of the document, used to learn and retrain the features to
	 * seasonal-knowledgebases. This is optional, if not set the current month
	 * will automatically be used.
	 */
	public Date documentTimeStamp;



	public ClassifyRequest() {
	}



	public String getXml_document() {
		return xml_document;
	}



	public ClassifyRequest setXml_document(String xml_document) throws JAXBException {
		this.xml_document = xml_document;
		return this;
	}



	public Document getDocument() throws JAXBException {
		if (this.document == null && this.xml_document.length() > 0)
			this.document = Document.unmarshallDocumentXmlString(xml_document);
		return document;
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
