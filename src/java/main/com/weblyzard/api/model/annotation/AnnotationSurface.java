package com.weblyzard.api.model.annotation;

import com.weblyzard.api.datatype.MD5Digest;
import java.io.Serializable;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import lombok.Data;
import lombok.experimental.Accessors;

/**
 * The surfaced annotation
 *
 * @author goebel@weblyzard.com
 */
@Data
@Accessors(chain = true)
@XmlAccessorType(XmlAccessType.FIELD)
public class AnnotationSurface implements Serializable {

    private static final long serialVersionUID = 1L;

    private int sentence = 0;
    private int start;
    private int end;
    private String surfaceForm;
    private MD5Digest md5sum;

    public AnnotationSurface(
            int start, int end, int sentence, MD5Digest md5sum, String surfaceForm) {
        this.start = start;
        this.end = end;
        this.sentence = sentence;
        this.md5sum = md5sum;
        this.surfaceForm = surfaceForm;
    }
}
