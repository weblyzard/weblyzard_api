package com.weblyzard.api.example.keyword;

import com.google.devtools.common.options.Option;
import com.google.devtools.common.options.OptionsBase;

public class KeywordExtractorOption extends OptionsBase{

	@Option(name="help", abbrev='h', help="Print usage info.", defaultValue="false")
	public boolean printHelp;

	@Option(name="Profile name", abbrev='n', help="Profile name used for the trained keyword extraction model.", defaultValue="default")
	public String profileName;
	
	@Option(name="Reference documents", abbrev='r', help="Directory with the reference documents used to train the keyword extraction.", defaultValue="")
	public String referenceCorpusDirectory;

	@Option(name="Target documents", abbrev='t', help="Directory with the documents to annotate.", defaultValue="")
	public String targetCorpusDirectory;

	@Option(name="Web service base URL", abbrev='b', help="webLyzard API base URL.", defaultValue="")
	public String webServiceBaseUrl;

	@Option(name="Web service user name", abbrev='u', help="webLyzard API user name.", defaultValue="")
	public String webServiceUserName;
	
	@Option(name="Web service password", abbrev='p', help="webLyzard API password.", defaultValue="")
	public String webServiceUserPassword;
}
