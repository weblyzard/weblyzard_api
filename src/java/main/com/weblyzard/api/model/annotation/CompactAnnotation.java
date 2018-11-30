package com.weblyzard.api.model.annotation;

import java.util.HashSet;
import java.util.Set;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.weblyzard.api.model.document.LegacyDocument;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;
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
@ToString(callSuper = true)
@XmlAccessorType(XmlAccessType.FIELD)
public class CompactAnnotation extends EntityDescriptor {

    @SuppressWarnings("unused")
    private static final long serialVersionUID = 1L;

    @JsonProperty("entities")
    @XmlElement(name = "entities", namespace = LegacyDocument.NS_WEBLYZARD)
    private Set<AnnotationSurface> entities = new HashSet<>();

    public CompactAnnotation(final String key) {
        super(key);
    }

    public CompactAnnotation(final Annotation a) {
        super(a.getKey());
        setPreferredName(a.getPreferredName()).setEntityType(a.getEntityType())
                .setEntityMetadata(a.getEntityMetadata()).compactAnnotation()
                .addSurface(new AnnotationSurface(a.getStart(), a.getEnd(), a.getSentence(),
                        a.getMd5sum(), a.getSurfaceForm(), a.getConfidence()));
    }

    public static CompactAnnotation build(String key) {
        return new CompactAnnotation(key);
    }

    public CompactAnnotation addSurface(AnnotationSurface entity) {
        if (!entities.contains(entity)) {
            entities.add(entity);
        }
        return this;
    }
}
