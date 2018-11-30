package com.weblyzard.api.model.joel;

import java.io.Serializable;
import java.util.List;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;
import lombok.experimental.Accessors;

/**
 * A Topic is characterized by its "title" and a list of keywords that frequently occur in documents
 * covering the topic. Keywords are represented by their corresponding URLs.
 * 
 * @author Norman Suesstrunk
 * 
 */
@Data
@Accessors(chain = true)
@RequiredArgsConstructor
@NoArgsConstructor
public class Topic implements Serializable {

    private static final long serialVersionUID = 1L;
    private @NonNull String title;
    /** A list of identifiers (URLs) of the context keywords. */
    private List<String> contextKeywords;
}
