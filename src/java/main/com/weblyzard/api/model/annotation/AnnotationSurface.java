package com.weblyzard.api.model.annotation;

import com.weblyzard.api.datatype.MD5Digest;
import java.io.Serializable;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

/**
 * A mention of one entity (i.e. its position and surface form)
 *
 * @author goebel@weblyzard.com
 */
@Data
@Accessors(chain = true)
@NoArgsConstructor
@AllArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
public class AnnotationSurface implements Serializable {

    private static final long serialVersionUID = 1L;

    private int start;
    private int end;
    private int sentence;
    private MD5Digest md5sum;
    private String surfaceForm;
    private double confidence;
}
