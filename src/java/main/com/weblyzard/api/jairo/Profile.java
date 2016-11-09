package com.weblyzard.api.jairo;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;

import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * 
 * @author Norman Suesstrunk
 *
 */

public class Profile implements Serializable {
		
	private static final long serialVersionUID = 1L;

	private Map<String, String> types = new HashMap<>(); 
	
	@JsonProperty("sparqlEndpoint")
	private String sparqlEndpoint; 
	
	@JsonProperty("query")
	private String query; 


	public String getQuery() {
		return query;
	}

	public void setQuery(String query) {
		this.query = query;
	}

	public Map<String, String> getTypes() {
		return types;
	}

	public void setTypes(Map<String, String> types) {
		this.types = types;
	}

	public String getSparqlEndpoint() {
		return sparqlEndpoint;
	}

	public void setSparqlEndpoint(String sparqlEndpoint) {
		this.sparqlEndpoint = sparqlEndpoint;
	}
	
	public void addType(String key, String value) {
		types.put(key, value);
	}
	

	@Override
	public boolean equals(Object obj) {
		if (obj == null) {
	        return false;
	    }
	    if (obj == this) {
	        return true;
	    }
	    if (this.getClass() != obj.getClass()) {
	        return false;
	    }
	    final Profile other = (Profile) obj;
	    
	    return new EqualsBuilder()
                .appendSuper(super.equals(obj))
                .append(this.query, other.query)
                .append(this.sparqlEndpoint, other.sparqlEndpoint)
                .isEquals();
	}
	
	@Override
	public int hashCode() {
		return new HashCodeBuilder(17, 37)
        .append(this.query)
        .append(this.sparqlEndpoint)
        .toHashCode();
	}
}
