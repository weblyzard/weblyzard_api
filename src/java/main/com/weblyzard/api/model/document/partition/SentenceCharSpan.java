package com.weblyzard.api.model.document.partition;

import java.util.HashMap;
import java.util.Map;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
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
    /**
     * This field provides support for numericSentenceProperties such as semOrient, significance,
     * mediaCriticismScore, veracityScore, etc.
     */
    private Map<String, Double> numericSentenceProperties;

    public SentenceCharSpan(int start, int end) {
        super(start, end);
    }

    @JsonAnyGetter
    public Map<String, Double> getNumericSentenceProperties() {
        return numericSentenceProperties;
    }

    @JsonAnySetter
    public void add(String key, double value) {
        if (numericSentenceProperties == null) {
            numericSentenceProperties = new HashMap<>();
        }
        numericSentenceProperties.put(key, value);
    }

}
