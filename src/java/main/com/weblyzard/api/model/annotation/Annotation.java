package com.weblyzard.api.model.annotation;

import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.weblyzard.api.datatype.MD5Digest;
import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.serialize.json.AnnotationSerializer;
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
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

/** @author norman.suesstrunk@htwchur.ch */
@Data
@Accessors(chain = true)
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@SuppressWarnings("serial")
@XmlAccessorType(XmlAccessType.FIELD)
@JsonSerialize(using = AnnotationSerializer.class)
public class Annotation extends EntityDescriptor implements Serializable {

    /**
     * field to add custom fields to an annotation
     *
     * <p>The custom Serializer {@link AnnotationSerializer} writes the keys of this map as fields
     * to the json annotation objects
     */
    @XmlAttribute(name = "header", namespace = Document.NS_WEBLYZARD)
    private Map<String, ArrayList<String>> header = new HashMap<>();

    /** field to store types when annotation is extended with jairo service */
    private List<String> type = new ArrayList<>();

    @XmlAttribute(name = "surfaceForm", namespace = Document.NS_WEBLYZARD)
    private String surfaceForm;

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
        setAnnotationType(annotationType);
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
        setAnnotationType(annotationType);
    }

    public Annotation(
            String surfaceForm,
            int start,
            int end,
            int sentence,
            MD5Digest md5sum,
            String annotationType) {
        this(surfaceForm, start, end, sentence, md5sum);
        setAnnotationType(annotationType);
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
        setKey(key);
        setPreferredName(preferredName);
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
        setKey(key);
        setPreferredName(preferredName);
        this.sentence = sentence;
    }
}
