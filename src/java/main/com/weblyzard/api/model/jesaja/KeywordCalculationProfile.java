package com.weblyzard.api.model.jesaja;

import java.util.Collections;
import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

/**
 * The profile specifying how keywords should be computed.
 * 
 * @author Albert Weichselbraun
 *
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Accessors(chain = true)
public class KeywordCalculationProfile {

    /**
     * A mapping of part-of-speech (POS) tags to the corresponding grammar groups.
     * <p>
     * Examples: <code>Map.of("NN", "noun", "NNS", "noun", "VB", "verb");</code>
     */
    @JsonProperty("pos_grammar_group_mapping")
    private Map<String, String> posGrammarGroupMapping;

    /**
     * A {@link Set} of valid grammar group patterns used for the keyword computation process.
     * <p>
     * Examples: <code>List.of("noun", "noun:noun", "noun:noun:noun")</code>
     */
    @JsonProperty("valid_grammar_group_patterns")
    private List<String> validGrammarGroupPatterns;

    /** minimum significance of phrases to get included in the analysis. */
    @JsonProperty("min_phrase_significance")
    private double minPhraseSignificance;

    /** number of keywords to return. */
    @JsonProperty("num_keywords")
    private int numKeywords;

    /** keyword algorithm to use. */
    @JsonProperty("keyword_algorithm")
    private String keywordAlgorithm;

    /** skip under-represented keywords. */
    @JsonProperty("skip_underrepresented_keywords")
    private boolean skipUnderrepresentedKeywords = true;

    /** minimum number of tokens required. */
    @JsonProperty("min_token_count")
    private int minTokenCount = 1;

    /** stoplist to use. */
    @JsonProperty("stoplists")
    private List<String> stoplists = Collections.emptyList();

    /** NEKs ground annotation entities as keywords. */
    @JsonProperty("ground_annotations")
    private boolean groundAnnotations;

    /** Ignore titles. */
    @JsonProperty("ignore_titles")
    private boolean ignoreTitles;

    /** Dynamically rotate reference corpus if true. */
    @JsonProperty("is_online")
    private boolean isOnline;

}
