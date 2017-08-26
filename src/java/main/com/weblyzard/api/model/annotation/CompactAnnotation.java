package com.weblyzard.api.model.annotation;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.weblyzard.api.datatype.MD5Digest;
import com.weblyzard.api.model.document.Document;
import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

/**
 * A compact annotation contains the annotation's metadata and a list of all entities (i.e.
 * mentions) of that particular annotation.
 *
 * @author goebel@weblyzard.com
 */
@Data
@Accessors(chain = true)
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@JsonIgnoreProperties({
    "sentence",
    "start",
    "end",
    "surfaceForm",
    "scoreName",
    "grounded",
    "md5sum"
})
public class CompactAnnotation extends Annotation {

    private static final long serialVersionUID = 1L;

    @JsonProperty("entities")
    @XmlElement(name = "entities", namespace = Document.NS_WEBLYZARD)
    public List<AnnotationSurface> entities = new ArrayList<>();

    public CompactAnnotation(Annotation annotation) {
        super(
                annotation.getKey(),
                annotation.getSurfaceForm(),
                annotation.getPreferredName(),
                annotation.getStart(),
                annotation.getEnd(),
                annotation.getSentence(),
                annotation.getMd5sum(),
                annotation.getAnnotationType());
        if (getEnd() > getStart())
            addSurface(
                    new AnnotationSurface(
                            getStart(),
                            getEnd(),
                            annotation.getSentence(),
                            annotation.getMd5sum(),
                            getSurfaceForm()));
    }

    public CompactAnnotation(
            String key,
            String surfaceForm,
            String preferredName,
            int start,
            int end,
            int sentence,
            MD5Digest md5sum,
            String annotationType) {
        super(key, surfaceForm, preferredName, start, end, sentence, md5sum, annotationType);
    }

    public void addSurface(AnnotationSurface entity) {
        if (!entities.contains(entity)) entities.add(entity);
    }
}
