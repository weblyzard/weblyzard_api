package com.weblyzard.api.domain.recognize;

import java.util.Set;

public class RecognyzeResult {

	public String key;
	public Set<SurfaceForm> surfaceForms;
	public String entityType;
	public double confidence;



	public RecognyzeResult setConfidence(double confidence) {
		this.confidence = confidence;
		return this;
	}



	public RecognyzeResult setEntityType(String entityType) {
		this.entityType = entityType;
		return this;
	}



	public RecognyzeResult setKey(String key) {
		this.key = key;
		return this;
	}



	public RecognyzeResult setSurfaceForms(Set<SurfaceForm> surfaceForms) {
		this.surfaceForms = surfaceForms;
		return this;
	}

}
