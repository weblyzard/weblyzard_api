package com.weblyzard.api.model.document.partition;

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
