package com.weblyzard.api.model.jesaja;

import java.util.Collections;
import java.util.List;
import java.util.Set;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

/**
 * The profile specifying how keywords should be computed
 * 
 * @author Albert Weichselbraun
 *
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Accessors(chain = true)
public class KeywordCalculationProfile {

    @JsonProperty("min_ngram_length")
    private int minNGramLength = 1;

    @JsonProperty("max_ngram_length")
    private int maxNGramLength = 3;

    /** minimum significance of phrases to get included in the analysis */
    @JsonProperty("min_phrase_significance")
    private double minPhraseSignificance;

    /** number of keywords to return */
    @JsonProperty("num_keywords")
    private int numKeywords;

    /** keyword algorithm to use */
    @JsonProperty("keyword_algorithm")
    private String keywordAlgorithm;

    /** skip under-represented keywords */
    @JsonProperty("skip_underrepresented_keywords")
    private boolean skipUnderrepresentedKeywords = true;

    /** minimum number of tokens required */
    @JsonProperty("min_token_count")
    private int minTokenCount = 1;

    /** allowed part-of-speech (POS) tags */
    @JsonProperty("valid_pos_tags")
    private Set<String> validPosTags;

    /** required part-of-speech (POS) tags */
    @JsonProperty("required_pos_tags")
    private Set<String> requiredPosTags;

    /** stoplist to use */
    @JsonProperty("stoplists")
    private List<String> stoplists = Collections.emptyList();

    /** NEKs ground annotation entities as keywords */
    @JsonProperty("ground_annotations")
    private boolean groundAnnotations;


}
