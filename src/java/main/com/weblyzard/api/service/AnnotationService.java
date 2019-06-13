package com.weblyzard.api.service;

import com.weblyzard.api.model.annotation.Annotation;
import com.weblyzard.api.model.document.Document;

public interface AnnotationService {

    /**
     * Annotates the given {@link Document} by extending the list of {@link Annotation}s in the document.
     * 
     * @param document to annotate
     * @return the document with extended annotations
     */
    public Document annotateDocument(final Document document);

}
