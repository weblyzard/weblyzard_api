package com.weblyzard.api.domain.weblyzard;

import java.io.Serializable;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;

/**
 * 
 * @author Norman Suesstrunk
 *
 */

@XmlAccessorType(XmlAccessType.FIELD)
public class Annotation implements Serializable {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	/**
	 * unique identifier of the annotation
	 */
	@XmlAttribute(name = "key")
	public String key;

	@XmlAttribute(name = "surfaceForm")
	public String surfaceForm;

	@XmlAttribute(name = "start")
	public int start;

	@XmlAttribute(name = "end")
	public int end;

	@XmlAttribute(name = "pos")
	public String pos;

	@XmlAttribute(name = "md5sum")
	public String md5sum;



	public Annotation() {
	}



	public Annotation(String wordForm, int start, int end) {
		super();
		this.surfaceForm = wordForm;
		this.start = start;
		this.end = end;
	}



	public Annotation setSurfaceForm(String surfaceForm) {
		this.surfaceForm = surfaceForm;
		return this;
	}



	public Annotation setKey(String key) {
		this.key = key;
		return this;
	}



	public Annotation setStart(int start) {
		this.start = start;
		return this;
	}



	public Annotation setEnd(int end) {
		this.end = end;
		return this;
	}



	public Annotation setPos(String pos) {
		this.pos = pos;
		return this;
	}



	public Annotation setMd5sum(String md5sum) {
		this.md5sum = md5sum;
		return this;
	}



	@Override
	public String toString() {
		return this.surfaceForm;
	}

}
