package com.weblyzard.api.domain.joseph;

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
	public double probability;
	public int productId;
	public Set<Significance> featureSignificances;



	public Classification() {
	}



	public Classification setCategory(String category) {
		this.category = category;
		return this;
	}



	public Classification setProbability(double probability) {
		if (Double.isNaN(probability))
			probability = 0d;
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
