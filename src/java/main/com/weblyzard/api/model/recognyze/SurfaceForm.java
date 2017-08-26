package com.weblyzard.api.model.recognyze;

import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class SurfaceForm {

    private String value;
    private int startIndex;
    private int endIndex;
    private boolean isContext;
    private double confidence;
}
