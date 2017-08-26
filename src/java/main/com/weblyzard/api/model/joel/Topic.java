package com.weblyzard.api.model.joel;

import java.io.Serializable;
import java.util.List;
import lombok.Data;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;
import lombok.experimental.Accessors;

/**
 * @author Norman Suesstrunk
 *     <p>A Topic is characterized by its "title" and a list of keywords that frequently occur in
 *     documents covering the topic.
 *     <p>Keywords are represented by their corresponding URLs
 */
@Data
@Accessors(chain = true)
@RequiredArgsConstructor
public class Topic implements Serializable {

    private static final long serialVersionUID = 1L;
    private @NonNull String title;
    /** A list of identifiers (URLs) of the context keywords */
    private List<String> contextKeywords;
}
