package com.weblyzard.api.model.joel;

import java.io.Serializable;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.experimental.Accessors;

/** @author norman.suesstrunk@htwchur.ch */
@Data
@Accessors(chain = true)
@AllArgsConstructor
public class ClusterResult implements Serializable {

    private static final long serialVersionUID = 1L;

    private Topic topic;
    private Cluster cluster;
}
