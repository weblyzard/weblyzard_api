package com.weblyzard.api.jairo;

import java.net.URI;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class RDFPrefix {

    private String prefix;
    private URI uri;
}
