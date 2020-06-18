package com.weblyzard.api.service;

import java.util.List;
import com.weblyzard.api.model.document.Document;

/**
 * Interface to annotate batchwise
 * 
 * @author sandro.hoerler@fhgr.ch
 *
 */
public interface BatchedAnnotationInterface {
    /**
     * Annotate documents batchwise.
     * 
     * @param documents document payload
     * @return annotated documents
     */
    public List<Document> annotateDocumentBatch(List<Document> documents);
}
