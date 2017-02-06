package com.weblyzard.api.document.annotation;

import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.weblyzard.api.document.Document;

/**
 * Compact form of an annotation
 * 
 * @author goebel@weblyzard.com
 *
 */
@XmlAccessorType(XmlAccessType.FIELD) 
@JsonIgnoreProperties({ "sentence", "start", "end", "surfaceForm", "scoreName", "grounded" })
public class CompactAnnotation extends Annotation {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	
	@JsonProperty("entities")
	@XmlElement(name="entities", namespace=Document.NS_WEBLYZARD)
	public List<AnnotationSurface> entities;
	
	public CompactAnnotation() { }
	
	public CompactAnnotation(Annotation annotation) {
		super(annotation.getKey(), annotation.getSurfaceForm(), annotation.getPreferredName(), 
				annotation.getStart(), annotation.getEnd(), annotation.getSentence(),
				annotation.getAnnotationType());
		this.entities = new ArrayList<>();
		if (getEnd()>getStart()) 
			addSurface(new AnnotationSurface(getStart(), getEnd(), 
					annotation.getSentence(), getSurfaceForm()));
	}
	
	public CompactAnnotation(String key, String surfaceForm, String preferredName, int start, 
			int end, int sentence, String annotationType) {
		super(key, surfaceForm, preferredName, start, end, sentence, annotationType);
	}
	
	public CompactAnnotation addSurface(AnnotationSurface entity) {
		if (this.entities == null)
			entities = new ArrayList<>();
		if (!this.entities.contains(entity))
			this.entities.add(entity);
		return this;
	}

	public void setEntities(List<AnnotationSurface> entities) {
		this.entities = entities;
	}
	
	public List<AnnotationSurface> getEntities() {
		return entities;
	}
}
