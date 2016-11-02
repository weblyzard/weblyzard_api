package com.weblyzard.api.joseph;

import java.util.Date;

import javax.xml.bind.JAXBException;
import javax.xml.bind.annotation.XmlRootElement;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.weblyzard.api.document.Document;

/**
 * Domain Transfer Object defining the interface for other services to use this
 * Webservice. This is used to call the <code>webservice.learn()</code> or the
 * <code>webservice.retrain()</code> service.
 * 
 * @author Philipp Kuntschik
 * 
 */
@XmlRootElement
public class LearnRequest {
	@JsonIgnore
	private Document document;

	private String xml_document;
	/**
	 * The category as which the features of the document should be trained for
	 * This must be set for <code>webservice.learn()</code>-Service. This is
	 * optional for <code>webservice.retrain()</code>-Service. If not set, the
	 * featureSet will be just decreased for oldCategory. If set, the featureSet
	 * will be increased for category afterwards.
	 */
	public String category;

	/**
	 * The category, for which the featureSet will be decreased. This will be
	 * ignored for <code>webservice.learn()</code>-Service. This is necessary
	 * for <code>webservice.retrain()</code>-Service.
	 */
	public String oldCategory;

	/**
	 * Timestamp of the document, used to learn and retrain the features to
	 * seasonal-knowledgebases. This is optional, if not set the current month
	 * will automatically be used.
	 */
	public Date documentTimeStamp;



	// JAXB needs this
	public LearnRequest() {
	}



	public LearnRequest setCategory(String category) {
		this.category = category;
		return this;
	}



	public LearnRequest setOldCategory(String oldCategory) {
		this.oldCategory = oldCategory;
		return this;
	}



	public String getXml_document() {
		return xml_document;
	}



	public LearnRequest setXml_document(String xml_document) throws JAXBException {
		this.xml_document = xml_document;
		return this;
	}



	public Document getDocument() throws JAXBException {
		if (this.document == null && this.xml_document.length() > 0)
			this.document = Document.unmarshallDocumentXmlString(xml_document);
		return document;
	}



	public LearnRequest setDocument(Document document) {
		this.document = document;
		return this;
	}



	public LearnRequest setDocumentTimeStamp(Date documentTimeStamp) {
		this.documentTimeStamp = documentTimeStamp;
		return this;
	}
}
