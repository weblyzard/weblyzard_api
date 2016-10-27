package com.weblyzard.api.document.annotation; 
 
import java.io.Serializable;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;

import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.weblyzard.api.datatype.MD5Digest;
import com.weblyzard.api.document.Document;
import com.weblyzard.api.document.serialize.json.AnnotationSerializer;
 
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
	public Map<String, List<String>> header = new HashMap<>(); 
     
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
     
    @XmlAttribute(name="annotationType", namespace=Document.NS_WEBLYZARD, required=false) 
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

	public Annotation setHeader(Map<String, List<String>> header) {
		this.header = header;
		return this;
	}

	public String getKey() {
		return key;
	}

	public Annotation setKey(String key) {
		this.key = key;
		return this;
	}

	public String getSurfaceForm() {
		return surfaceForm;
	}

	public Annotation setSurfaceForm(String surfaceForm) {
		this.surfaceForm = surfaceForm;
		return this;
	}

	public String getPreferredName() {
		return preferredName;
	}

	public Annotation setPreferredName(String preferredName) {
		this.preferredName = preferredName;
		return this;
	}

	public int getStart() {
		return start;
	}

	public Annotation setStart(int start) {
		this.start = start;
		return this;
	}

	public int getEnd() {
		return end;
	}

	public Annotation setEnd(int end) {
		this.end = end;
		return this;
	}

	public String getPos() {
		return pos;
	}

	public Annotation setPos(String pos) {
		this.pos = pos;
		return this;
	}

	public int getSentence() {
		return sentence;
	}

	public Annotation setSentence(int sentence) {
		this.sentence = sentence;
		return this;
	}

	public MD5Digest getMd5sum() {
		return md5sum;
	}

	public Annotation setMd5sum(MD5Digest md5sum) {
		this.md5sum = md5sum;
		return this;
	}

	public String getAnnotationType() {
		return annotationType;
	}

	public Annotation setAnnotationType(String annotationType) {
		this.annotationType = annotationType;
		return this;
	} 
    
    
     
}