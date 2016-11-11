package com.weblyzard.api.joel;

import java.util.List;

public class Cluster {
	
	private String label; 
	
	private List<KeywordDocument> docs;
	
	public Cluster(){}

	public Cluster(List<KeywordDocument> docs) {
		super();
		this.docs = docs;
	}
	
	public Cluster(List<KeywordDocument> docs, String lable) {
		super();
		this.docs = docs;
		this.label = lable; 
	}
	
	public List<KeywordDocument> getDocs() {
		return this.docs; 
	}
	
	public String getLabel() {
		return this.label; 
	}
}
