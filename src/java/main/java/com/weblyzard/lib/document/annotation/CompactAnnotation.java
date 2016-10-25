package com.weblyzard.lib.document.annotation;

import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.weblyzard.lib.document.Document;

/**
 * Compact form of an annotation
 * 
 * @author Max Goebel <goebel@weblyzard.com>
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
		super(annotation.key, annotation.surfaceForm, annotation.preferredName, 
				annotation.start, annotation.end, annotation.annotationType);
		this.entities = new ArrayList<>();
		if (end>start) 
			addSurface(new AnnotationSurface(start, end, annotation.sentence, surfaceForm));
	}
	
	public void addSurface(AnnotationSurface entitiy) {
		if (this.entities == null)
			entities = new ArrayList<>();
		if (!this.entities.contains(entitiy))
			this.entities.add(entitiy);
	}

	public List<AnnotationSurface> getEntities() {
		return entities;
	}
}
