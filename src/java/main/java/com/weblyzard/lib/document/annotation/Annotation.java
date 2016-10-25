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
import com.weblyzard.lib.MD5Digest;
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
	public Map<String, List<String>> header = new HashMap<>(); 
     
    /** 
     * unique identifier of the annotation 
     */ 
    @XmlAttribute(name="key", namespace=Document.NS_WEBLYZARD) 
    public String key;  
 
    @XmlAttribute(name="surfaceForm", namespace=Document.NS_WEBLYZARD) 
    public String surfaceForm;     
 
    @XmlAttribute(name="preferredName", namespace=Document.NS_WEBLYZARD) 
    public String preferredName;   
    
    @XmlAttribute(name="start", namespace=Document.NS_WEBLYZARD) 
    public int start;  
     
    @XmlAttribute(name="end", namespace=Document.NS_WEBLYZARD) 
    public int end; 
    
    @XmlAttribute(name="pos", namespace=Document.NS_WEBLYZARD) 
    public String pos; 
    
    @XmlAttribute(name="sentence", namespace=Document.NS_WEBLYZARD) 
    public int sentence; 
 
    @XmlAttribute(name="md5sum", namespace=Document.NS_WEBLYZARD) 
    @XmlJavaTypeAdapter(MD5Digest.class) 
    public MD5Digest md5sum; 
     
    @XmlAttribute(name="annotationType", namespace=Document.NS_WEBLYZARD) 
    public String annotationType;     
     
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
     
}