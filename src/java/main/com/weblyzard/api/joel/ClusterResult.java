package com.weblyzard.api.joel;

import java.io.Serializable;
import lombok.AllArgsConstructor;
import lombok.Data;

/** @author norman.suesstrunk@htwchur.ch */
@Data
@AllArgsConstructor
public class ClusterResult implements Serializable {

    private static final long serialVersionUID = 1L;

    private Topic topic;
    private Cluster cluster;
}
