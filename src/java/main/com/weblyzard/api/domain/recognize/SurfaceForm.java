package com.weblyzard.api.domain.recognize;

public class SurfaceForm {

	public String value;
	public int startIndex;
	public int endIndex;
	public boolean isContext;



	public SurfaceForm setValue(String value) {
		this.value = value;
		return this;
	}



	public SurfaceForm setStartIndex(int startIndex) {
		this.startIndex = startIndex;
		return this;
	}



	public SurfaceForm setEndIndex(int endIndex) {
		this.endIndex = endIndex;
		return this;
	}



	public SurfaceForm setContext(boolean isContext) {
		this.isContext = isContext;
		return this;
	}
}
