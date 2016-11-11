package com.weblyzard.api.joseph;

import java.util.Set;

import javax.xml.bind.annotation.XmlRootElement;

/**
 * Wrapper for a single classification. Used to respond only relevant data.
 * 
 * @author Philipp Kuntschik
 * 
 */
@XmlRootElement
public class Classification {

	public String category;
	public float probability;
	public int productId;
	public Set<Significance> featureSignificances;



	public Classification() {
	}



	public Classification(String category, float probability) {
		super();
		this.category = category;
		this.probability = probability;
	}



	public Classification(String category, float probability, Set<Significance> featureSignificances) {
		super();
		this.category = category;
		this.probability = probability;
		this.featureSignificances = featureSignificances;
	}



	public Classification(String category) {
		this.category = category;
	}



	public Classification setCategory(String category) {
		this.category = category;
		return this;
	}



	public Classification setProbability(float probability) {
		if (Double.isNaN(probability))
			probability = 0f;
		this.probability = probability;
		return this;
	}



	public Classification setProductId(int productId) {
		this.productId = productId;
		return this;
	}



	public Classification setFeatureSignificances(Set<Significance> significances) {
		this.featureSignificances = significances;
		return this;
	}

}
