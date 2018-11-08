package com.weblyzard.api.model;

import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonSubTypes.Type;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.fasterxml.jackson.annotation.JsonTypeInfo.As;
import com.fasterxml.jackson.annotation.JsonTypeInfo.Id;
import com.weblyzard.api.model.document.partition.CharSpan;
import com.weblyzard.api.model.document.partition.SentenceCharSpan;
import com.weblyzard.api.model.document.partition.TokenCharSpan;

/**
 * A position within a document or sentence that is marked by a start and end index.
 * 
 * @author Albert Weichselbraun
 *
 */
@JsonTypeInfo(use = Id.NAME, include = As.PROPERTY)
@JsonSubTypes({@Type(value = CharSpan.class), @Type(value = TokenCharSpan.class),
        @Type(value = SentenceCharSpan.class)})
public interface Span {

    /**
     * Returns the {@link Span}s start position.
     */
    public int getStart();

    /**
     * Returns the {@link Span}s end position.
     */
    public int getEnd();

    public Span setStart(int start);

    public Span setEnd(int end);
}
