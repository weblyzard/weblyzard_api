package com.weblyzard.api.model.document;

import lombok.Value;

/**
 * A string range within a document
 * 
 * @author Albert Weichselbraun
 *
 */
@Value
public class StringRange {
    private final int start;
    private final int end;

    /**
     * @return the substring within the given range
     */
    public String getSubstring(String s) {
        return s.substring(start, end);
    }
}
