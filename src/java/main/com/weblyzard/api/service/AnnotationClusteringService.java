package com.weblyzard.api.service;

import java.util.List;
import java.util.Map;
import com.weblyzard.api.model.annotation.Annotation;

public interface AnnotationClusteringService {

    /**
     * Transforms a list of annotations into a map of annotation clusters.
     * 
     * @param annotationList the annotations to cluster
     * @return a map of clusters with the corresponding list of annotations belonging to these
     *         clusters
     */
    public Map<String, List<Annotation>> clusterAnnotations(final List<Annotation> annotationList);

}
