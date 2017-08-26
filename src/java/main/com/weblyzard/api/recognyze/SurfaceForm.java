package com.weblyzard.api.recognyze;

import lombok.Data;

@Data
public class SurfaceForm {

    private String value;
    private int startIndex;
    private int endIndex;
    private boolean isContext;
    private double confidence;
}
