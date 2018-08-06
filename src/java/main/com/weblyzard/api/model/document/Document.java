package com.weblyzard.api.model.document;

import java.io.Serializable;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.xml.namespace.QName;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.weblyzard.api.model.Lang;
import com.weblyzard.api.model.Span;
import com.weblyzard.api.model.annotation.Annotation;
import com.weblyzard.api.model.document.partition.DocumentPartition;
import com.weblyzard.api.serialize.json.DocumentHeaderDeserializer;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

/**
 * The {@link Document} class used to represent documents.
 *
 * <p>
 * The {@link Document} class also supports arbitrary meta data which is stored in the <code>
 * header</code> instance variable.
 *
 * @author Albert Weichselbraun
 */
@Data
@Accessors(chain = true)
@NoArgsConstructor
@JsonInclude(content = Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class Document implements Serializable {

    private static final long serialVersionUID = 1L;
    public static final String NS_DUBLIN_CORE = "http://purl.org/dc/elements/1.1/";

    /** The Attribute used to encode document keywords */
    public static final QName WL_KEYWORD_ATTR = new QName(NS_DUBLIN_CORE, "subject");

    private String id;
    private String format;
    private Lang lang;
    private String nilsimsa;

    @JsonDeserialize(keyUsing = DocumentHeaderDeserializer.class)
    private Map<QName, String> header = new HashMap<>();

    private String content;

    /** Document {@link DocumentPartition} such as title, body, sentences, lines, etc. */
    private Map<DocumentPartition, List<Span>> partitions;

    /**
     * This field contains all annotations after titleAnnotations and bodyAnnotations have been
     * merged. (i.e. after the document's finalization)
     */
    @JsonProperty("annotations")
    private List<Annotation> annotations;

    public Document(Document d) {
        Document document = new Document();
        document.id = d.id;
        document.format = d.format;
        document.lang = d.lang;
        document.nilsimsa = d.nilsimsa;
        document.header = d.header;
        document.partitions = partitions;
    }

}
