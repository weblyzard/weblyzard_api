package com.weblyzard.api.document.annotation;

import com.weblyzard.api.datatype.MD5Digest;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import lombok.Data;

/**
 * The surfaced annotation
 *
 * @author goebel@weblyzard.com
 */
@Data
@XmlAccessorType(XmlAccessType.FIELD)
public class AnnotationSurface {

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
