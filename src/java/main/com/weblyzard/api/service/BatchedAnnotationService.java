package com.weblyzard.api.service;

import java.util.List;
import com.weblyzard.api.model.document.Document;

/**
 * Interface for batched annotation processing.
 * 
 * @author sandro.hoerler@fhgr.ch
 *
 */
public interface BatchedAnnotationService {

    /**
     * Annotates the given list of {@link Document}s.
     * 
     * @param documents to annotate
     * @return the documents with annotations
     */
    public List<Document> annotateDocumentBatch(final List<Document> documents);

}
