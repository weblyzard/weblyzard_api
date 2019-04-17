package com.weblyzard.api.example.keyword;

import com.google.devtools.common.options.Option;
import com.google.devtools.common.options.OptionsBase;

public class KeywordExtractorOption extends OptionsBase {

    @Option(name = "help", abbrev = 'h', help = "Print usage info.", defaultValue = "false")
    public boolean printHelp;

    @Option(name = "profile-name", abbrev = 'n',
            help = "Profile name used for the trained keyword extraction model.",
            defaultValue = "default")
    public String profileName;

    @Option(name = "document-language", abbrev = 'l',
            help = "Force the given document language on all documents.", defaultValue = "")
    public String documentLanguage;

    @Option(name = "reference-documents", abbrev = 'r',
            help = "Directory with the reference documents used to train the keyword extraction.",
            defaultValue = "")
    public String referenceCorpusDirectory;

    @Option(name = "target-documents", abbrev = 't',
            help = "Directory with the target documents to annotate.", defaultValue = "")
    public String targetCorpusDirectory;

    @Option(name = "web-service-url", abbrev = 'b', help = "webLyzard API base URL.",
            defaultValue = "")
    public String webServiceBaseUrl;

    @Option(name = "web-service-user", abbrev = 'u', help = "webLyzard API user name.",
            defaultValue = "")
    public String webServiceUserName;

    @Option(name = "web-service-password", abbrev = 'p', help = "webLyzard API password.",
            defaultValue = "")
    public String webServiceUserPassword;

    @Option(name = "use-compression", abbrev = 'c', help = "Compress requests to the API server.",
            defaultValue = "false")
    public String useCompression;

    @Option(name = "valid-grammar-group-patterns", abbrev = 'v',
            help = "Grammar group patterns used for extracting keywords.",
            defaultValue = "noun,noun:noun,noun:prep:noun,noun:noun,noun:adj:noun,adv:adj:noun,adj:noun:noun")
    public String validGrammarGroupPatterns;

    @Option(name = "num-keywords", abbrev = 'k', help = "Number of keywords to compute.",
            defaultValue = "15")
    public String numKeywords;

    @Option(name = "debug-jeremia-document-file", abbrev = 'j',
            help = "Write Jeremia results into the given file.", defaultValue = "")
    public String debugJeremiaDocumentFile;
}
