package com.weblyzard.lib.document.annotation; 
 
import java.io.Serializable;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.xml.bind.annotation.XmlAccessType; 
import javax.xml.bind.annotation.XmlAccessorType; 
import javax.xml.bind.annotation.XmlAttribute; 
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;

import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.weblyzard.api.MD5Digest;
import com.weblyzard.lib.document.Document;
 
/** 
 *  
 * @author Norman Suesstrunk 
 * 
 */ 

@SuppressWarnings("serial")
@XmlAccessorType(XmlAccessType.FIELD) 
@JsonSerialize(using = AnnotationSerializer.class)
public class Annotation implements Serializable { 
	
	/**
	 * field to add custom fields to an annotation 
	 * 
	 * The custom Serializer {@link AnnotationSerializer} writes the keys of this map 
	 * as fields to the json annotation objects 
	 */
	private Map<String, List<String>> header = new HashMap<>(); 
     
    /** 
     * unique identifier of the annotation 
     */ 
    @XmlAttribute(name="key", namespace=Document.NS_WEBLYZARD) 
    private String key;  
 
    @XmlAttribute(name="surfaceForm", namespace=Document.NS_WEBLYZARD) 
    private String surfaceForm;     
 
    @XmlAttribute(name="preferredName", namespace=Document.NS_WEBLYZARD) 
    private String preferredName;   
    
    @XmlAttribute(name="start", namespace=Document.NS_WEBLYZARD) 
    private int start;  
     
    @XmlAttribute(name="end", namespace=Document.NS_WEBLYZARD) 
    private int end; 
    
    @XmlAttribute(name="pos", namespace=Document.NS_WEBLYZARD) 
    private String pos; 
    
    @XmlAttribute(name="sentence", namespace=Document.NS_WEBLYZARD) 
    private int sentence; 
 
    @XmlAttribute(name="md5sum", namespace=Document.NS_WEBLYZARD) 
    @XmlJavaTypeAdapter(MD5Digest.class) 
    private MD5Digest md5sum; 
     
    @XmlAttribute(name="annotationType", namespace=Document.NS_WEBLYZARD) 
    private String annotationType;     
     
    // required for JAXB 
    public Annotation() {} 
     
    public Annotation(String surfaceForm, int start, int end) { 
        this.surfaceForm = surfaceForm; 
        this.start = start; 
        this.end = end;         
    } 
     
    public Annotation(String surfaceForm, int start, int end, String annotationType) { 
        this(surfaceForm, start, end); 
        this.annotationType = annotationType; 
    } 
     
    public Annotation(String key, String surfaceForm, String preferredName, int start, int end, String annotationType) { 
        this(surfaceForm, start, end, annotationType); 
        this.key = key;
        this.preferredName = preferredName;
    } 
     
    @Override 
    public String toString() { 
        return "key: "+key+" surfaceForm: "+surfaceForm+" start: "+start+" end: "+end+" md5: "+md5sum; 
    }

	public Map<String, List<String>> getHeader() {
		return header;
	}

	public void setHeader(Map<String, List<String>> header) {
		this.header = header;
	}

	public String getKey() {
		return key;
	}

	public void setKey(String key) {
		this.key = key;
	}

	public String getSurfaceForm() {
		return surfaceForm;
	}

	public void setSurfaceForm(String surfaceForm) {
		this.surfaceForm = surfaceForm;
	}

	public String getPreferredName() {
		return preferredName;
	}

	public void setPreferredName(String preferredName) {
		this.preferredName = preferredName;
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

	public String getPos() {
		return pos;
	}

	public void setPos(String pos) {
		this.pos = pos;
	}

	public int getSentence() {
		return sentence;
	}

	public void setSentence(int sentence) {
		this.sentence = sentence;
	}

	public MD5Digest getMd5sum() {
		return md5sum;
	}

	public void setMd5sum(MD5Digest md5sum) {
		this.md5sum = md5sum;
	}

	public String getAnnotationType() {
		return annotationType;
	}

	public void setAnnotationType(String annotationType) {
		this.annotationType = annotationType;
	} 
    
    
     
}