package com.weblyzard.api.model;

/**
 * A position within a document or sentence that is marked by a start and end index.
 * 
 * @author Albert Weichselbraun
 *
 */
public interface Span {

    /**
     * @return the {@link Span}s start position
     */
    public int getStart();

    /**
     * @return the {@link Span}s end position
     */
    public int getEnd();
}
