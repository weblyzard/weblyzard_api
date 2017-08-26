package com.weblyzard.api.recognyze;

import java.util.Set;
import lombok.Data;

@Data
public class RecognyzeResult {

    private String key;
    private Set<SurfaceForm> surfaceForms;
    private String entityType;
    private double confidence;
}
