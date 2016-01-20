package com.weblyzard.api.domain.joseph;

import java.util.Date;

import javax.xml.bind.annotation.XmlRootElement;

import com.weblyzard.api.domain.weblyzard.Document;

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
	public Document document;

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



	public LearnRequest setDocument(Document document) {
		this.document = document;
		return this;
	}



	public LearnRequest setDocumentTimeStamp(Date documentTimeStamp) {
		this.documentTimeStamp = documentTimeStamp;
		return this;
	}
}
