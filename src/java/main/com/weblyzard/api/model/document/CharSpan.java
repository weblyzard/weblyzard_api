package com.weblyzard.api.model.document;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * A string range within a document
 * 
 * @author Albert Weichselbraun
 *
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class CharSpan {
    private int start;
    private int end;

    /**
     * @return the substring within the given range
     */
    public String getSubstring(String s) {
        return s.substring(start, end);
    }
}
