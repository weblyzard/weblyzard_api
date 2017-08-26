package com.weblyzard.api.model.jairo;

import java.net.URI;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@AllArgsConstructor
public class RDFPrefix {

    private String prefix;
    private URI uri;
}
