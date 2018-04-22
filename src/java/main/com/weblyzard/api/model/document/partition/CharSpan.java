package com.weblyzard.api.model.document.partition;

import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonSubTypes.Type;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.fasterxml.jackson.annotation.JsonTypeInfo.As;
import com.fasterxml.jackson.annotation.JsonTypeInfo.Id;
import com.weblyzard.api.model.Span;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

/**
 * A string range within a document
 * 
 * @author Albert Weichselbraun
 *
 */
@Data
@Accessors(chain = true)
@AllArgsConstructor
@NoArgsConstructor
@JsonTypeInfo(use = Id.NAME, include = As.PROPERTY)
@JsonSubTypes({@Type(value = TokenCharSpan.class), @Type(value = SentenceCharSpan.class)})
public class CharSpan implements Span {
    private int start;
    private int end;

    /**
     * @return the substring within the given range
     */
    public String getSubstring(String s) {
        return s.substring(start, end);
    }
}
