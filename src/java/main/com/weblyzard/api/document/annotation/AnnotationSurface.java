package com.weblyzard.api.document.annotation;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

import com.weblyzard.api.datatype.MD5Digest;

/**
 * The surfaced annotation
 * 
 * @author goebel@weblyzard.com
 *
 */
@XmlAccessorType(XmlAccessType.FIELD) 
//@JsonIgnoreProperties({ "sentence", "start", "end", "surfaceForm", "scoreName", "grounded" })
public class AnnotationSurface {

	private int sentence = 0;
	private int start;
	private int end;
	private String surfaceForm;
	private MD5Digest md5sum;

	public AnnotationSurface() {}

	public AnnotationSurface(int start, int end, int sentence, 
			MD5Digest md5sum, String surfaceForm) {
		this.start = start;
		this.end = end;
		this.sentence = sentence;
		this.md5sum = md5sum;
		this.surfaceForm = surfaceForm;
	}

	@Override
	public boolean equals(Object obj) {
		if (obj instanceof AnnotationSurface) {
			AnnotationSurface other = (AnnotationSurface) obj;
			return start==other.start && end==other.end && sentence==other.sentence;
		}
		return false;
	}

	public int getSentence() {
		return sentence;
	}

	public AnnotationSurface setSentence(int sentence) {
		this.sentence = sentence;
		return this;
	}

	public int getStart() {
		return start;
	}

	public AnnotationSurface setStart(int start) {
		this.start = start;
		return this;
	}

	public int getEnd() {
		return end;
	}
	
	public MD5Digest getMd5sum() {
		return md5sum;
	}
	
	public void setMd5sum(MD5Digest md5sum) {
		this.md5sum = md5sum;
	}

	public AnnotationSurface setEnd(int end) {
		this.end = end;
		return this;
	}

	public String getSurfaceForm() {
		return surfaceForm;
	}

	public AnnotationSurface setSurfaceForm(String surfaceForm) {
		this.surfaceForm = surfaceForm;
		return this;
	}

}