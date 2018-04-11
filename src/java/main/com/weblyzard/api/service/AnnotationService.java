package com.weblyzard.api.service;

import com.weblyzard.api.model.document.LegacyDocument;

public interface AnnotationService {
    
    /**
     * Annotates the given {@link LegacyDocument} by extending the list of Annotations returned by
     * {@link LegacyDocument#getAnnotations()}.
     */
    public LegacyDocument annotateDocument(final LegacyDocument document);

}
