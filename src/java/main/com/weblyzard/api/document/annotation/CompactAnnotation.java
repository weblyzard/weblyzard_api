package com.weblyzard.api.document.annotation;

import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
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
	
	@XmlElement(name="entities", namespace=Document.NS_WEBLYZARD)
	public List<AnnotationSurface> entities;
	
	public CompactAnnotation() { }
	
	public CompactAnnotation(Annotation annotation) {
		super(annotation.getKey(), annotation.getSurfaceForm(), annotation.getPreferredName(), 
				annotation.getStart(), annotation.getEnd(), annotation.getAnnotationType());
		this.entities = new ArrayList<>();
		if (getEnd()>getStart()) 
			addSurface(new AnnotationSurface(getEnd(), getStart(), annotation.getSentence(), getSurfaceForm()));
	}
	
	public CompactAnnotation addSurface(AnnotationSurface entitiy) {
		if (this.entities == null)
			entities = new ArrayList<>();
		if (!this.entities.contains(entitiy))
			this.entities.add(entitiy);
		return this;
	}

	public List<AnnotationSurface> getEntities() {
		return entities;
	}
}
