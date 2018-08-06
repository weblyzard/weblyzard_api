package com.weblyzard.api.model.joel;

import com.weblyzard.api.model.document.LegacyDocument;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import lombok.experimental.Accessors;

/**
 * @author norman.suesstrunk@htwchur.ch
 * @author albert.weichselbraun@htwchur.ch
 */
@Data
@Accessors(chain = true)
@NoArgsConstructor
public class KeywordDocument implements Serializable {

    private static final long serialVersionUID = 1L;

    public static final String FIELD_KEYWORDS = "tokens";
    public static final String FIELD_SENTENCES = "sentences";

    private @NonNull LegacyDocument document;
    private List<String> keywords;

    public KeywordDocument(LegacyDocument document) {
        this.document = document;
        initKeywordsFromDocument();
    }

    private void initKeywordsFromDocument() {
        if (document.getHeader() != null) {
            this.keywords =
                    Arrays.asList(document.getHeader().get(LegacyDocument.WL_KEYWORD_ATTR).split(";"))
                            .stream()
                            .map(String::trim)
                            .collect(Collectors.toList());

        } else {
            this.keywords = new ArrayList<>();
        }
    }
}
