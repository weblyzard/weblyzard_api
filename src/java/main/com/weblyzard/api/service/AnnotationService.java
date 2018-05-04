package com.weblyzard.api.service;

import com.weblyzard.api.model.document.Document;

public interface AnnotationService {
    
    /**
     * Annotates the given {@link Document} by extending the list of Annotations returned by
     * {@link Document#getAnnotations()}.
     */
    public Document annotateDocument(final Document document);

}
