package com.weblyzard.api.document.annotation;

import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.weblyzard.api.datatype.MD5Digest;
import com.weblyzard.api.document.serialize.json.AnnotationSerializer;
import com.weblyzard.api.model.document.Document;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;
import lombok.Data;
import lombok.NoArgsConstructor;

/** @author norman.suesstrunk@htwchur.ch */
@Data
@NoArgsConstructor
@SuppressWarnings("serial")
@XmlAccessorType(XmlAccessType.FIELD)
@JsonSerialize(using = AnnotationSerializer.class)
public class Annotation implements Serializable {

    /**
     * field to add custom fields to an annotation
     *
     * <p>The custom Serializer {@link AnnotationSerializer} writes the keys of this map as fields
     * to the json annotation objects
     */
    public Map<String, ArrayList<String>> header = new HashMap<>();

    /** field to store types when annotation is extended with jairo service */
    private List<String> type = new ArrayList<>();

    /** unique identifier of the annotation */
    @XmlAttribute(name = "key", namespace = Document.NS_WEBLYZARD)
    private String key;

    @XmlAttribute(name = "surfaceForm", namespace = Document.NS_WEBLYZARD)
    private String surfaceForm;

    @XmlAttribute(name = "preferredName", namespace = Document.NS_WEBLYZARD)
    private String preferredName;

    @XmlAttribute(name = "start", namespace = Document.NS_WEBLYZARD)
    private int start;

    @XmlAttribute(name = "end", namespace = Document.NS_WEBLYZARD)
    private int end;

    @XmlAttribute(name = "pos", namespace = Document.NS_WEBLYZARD)
    private String pos;

    @XmlAttribute(name = "sentence", namespace = Document.NS_WEBLYZARD)
    private int sentence;

    @XmlAttribute(name = "md5sum", namespace = Document.NS_WEBLYZARD)
    @XmlJavaTypeAdapter(MD5Digest.class)
    private MD5Digest md5sum;

    @XmlAttribute(name = "annotationType", namespace = Document.NS_WEBLYZARD, required = false)
    private String annotationType;

    public Annotation(String surfaceForm, int start, int end, int sentence, MD5Digest md5sum) {
        this.surfaceForm = surfaceForm;
        this.start = start;
        this.end = end;
        this.sentence = sentence;
        this.md5sum = md5sum;
    }

    public Annotation(String surfaceForm, int start, int end, int sentence, String annotationType) {
        this.surfaceForm = surfaceForm;
        this.start = start;
        this.end = end;
        this.sentence = sentence;
        this.annotationType = annotationType;
    }

    public Annotation(String surfaceForm, int start, int end, int sentence) {
        this.surfaceForm = surfaceForm;
        this.start = start;
        this.end = end;
        this.sentence = sentence;
    }

    public Annotation(String surfaceForm, int start, int end) {
        this.surfaceForm = surfaceForm;
        this.start = start;
        this.end = end;
    }

    public Annotation(String surfaceForm, int start, int end, String annotationType) {
        this.surfaceForm = surfaceForm;
        this.start = start;
        this.end = end;
        this.annotationType = annotationType;
    }

    public Annotation(
            String surfaceForm,
            int start,
            int end,
            int sentence,
            MD5Digest md5sum,
            String annotationType) {
        this(surfaceForm, start, end, sentence, md5sum);
        this.annotationType = annotationType;
    }

    public Annotation(
            String key,
            String surfaceForm,
            String preferredName,
            int start,
            int end,
            int sentence,
            MD5Digest md5sum,
            String annotationType) {
        this(surfaceForm, start, end, sentence, md5sum, annotationType);
        this.key = key;
        this.preferredName = preferredName;
    }

    public Annotation(
            String key,
            String surfaceForm,
            String preferredName,
            int start,
            int end,
            int sentence,
            String annotationType) {
        this(surfaceForm, start, end, annotationType);
        this.key = key;
        this.preferredName = preferredName;
        this.sentence = sentence;
    }
}
