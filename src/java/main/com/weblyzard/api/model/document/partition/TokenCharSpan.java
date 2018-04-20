package com.weblyzard.api.model.document.partition;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * A {@link CharSpan} used for token which contains POS and Dependency information.
 * @author Albert Weichselbraun
 *
 */
@NoArgsConstructor
public class TokenCharSpan extends CharSpan{
    private @Setter @Getter String pos;
    private @Setter @Getter Dependency dependency;
    
    public TokenCharSpan(int start, int end, String pos, Dependency dependency) {
        super(start, end);
        this.pos = pos;
        this.dependency = dependency;
    }
}
