package com.weblyzard.api.model.document;

import java.io.Serializable;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import javax.xml.namespace.QName;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.weblyzard.api.model.Lang;
import com.weblyzard.api.model.annotation.Annotation;
import com.weblyzard.api.serialize.json.LangDeserializer;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

/**
 * The {@link MirrorDocument} represents a document with separate title and body fields as created by mirror processes.
 *
 * @author Albert Weichselbraun
 */
@Data
@Accessors(chain = true)
@NoArgsConstructor
public class MirrorDocument implements Serializable {

    private static final long serialVersionUID = 1L;

    /** a unique document identifier such as the content id. */
    private String id;
    private String title;
    private String body;

    /** the document's content type (e.g. 'text/html'). */
    private String format;
    @JsonDeserialize(using = LangDeserializer.class)
    private Lang lang;

    /** arbitrary header metadata. */
    private Map<QName, String> header;

    /** attributes required for the annotation handling. */
    @JsonProperty("body_annotation")
    private List<Annotation> bodyAnnotations;
    @JsonProperty("title_annotation")
    private List<Annotation> titleAnnotations;

    public List<Annotation> getBodyAnnotations() {
        return bodyAnnotations != null ? bodyAnnotations : Collections.<Annotation>emptyList();
    }

    public List<Annotation> getTitleAnnotations() {
        return titleAnnotations != null ? titleAnnotations : Collections.<Annotation>emptyList();
    }

}
