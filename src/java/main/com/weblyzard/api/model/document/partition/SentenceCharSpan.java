package com.weblyzard.api.model.document.partition;

import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;
import com.weblyzard.api.datatype.MD5Digest;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

/**
 * A {@link CharSpan} used for sentences.
 * 
 * @author Albert Weichselbraun
 *
 */
@Data
@NoArgsConstructor
@Accessors(chain = true)
@EqualsAndHashCode(callSuper = true)
public class SentenceCharSpan extends CharSpan {

    @XmlJavaTypeAdapter(MD5Digest.class)
    private MD5Digest id;
    private double semOrient;
    private double significance;

    public SentenceCharSpan(int start, int end) {
        super(start, end);
    }

}
