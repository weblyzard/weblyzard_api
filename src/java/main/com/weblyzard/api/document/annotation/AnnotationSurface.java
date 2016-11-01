package com.weblyzard.api.document.annotation;


/**
 * The surfaced annotation
 * 
 * @author Max Goebel <goebel@weblyzard.com>
 *
 */
public class AnnotationSurface {

	private int sentence = 0;
	private int start;
	private int end;
	private String surfaceForm;

	public AnnotationSurface() {}

	public AnnotationSurface(int start, int end, int sentence, String surfaceForm) {
		this.start = start;
		this.end = end;
		this.sentence = sentence;
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

	public void setSentence(int sentence) {
		this.sentence = sentence;
	}

	public int getStart() {
		return start;
	}

	public void setStart(int start) {
		this.start = start;
	}

	public int getEnd() {
		return end;
	}

	public void setEnd(int end) {
		this.end = end;
	}

	public String getSurfaceForm() {
		return surfaceForm;
	}

	public void setSurfaceForm(String surfaceForm) {
		this.surfaceForm = surfaceForm;
	}

}