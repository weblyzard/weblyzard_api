## The webLyzard API

Provides access to all webLyzard Web services.

### Configuration

The API needs to know the URL, user and password used for the Web service. These data may be 
1. passed by a client at class initialization, or
2. automatically set by the means of the following environment variables:
  * `WEBLYZARD_API_URL`
  * `WEBLYZARD_API_USER`
  * `WEBLYZARD_API_PASS`

   this is also the preferred way for running unit tests.

The preferred way for setting these variables is using `.bash_profile`.
```bash
export WEBLYZARD_API_URL="https://noah.semanticlab.net/ws"
export WEBLYZARD_API_USER="user"
export WEBLYZARD_API_PASS="pass"
```

### Available interfaces:

The following interfaces are currently available for `weblyzard_api`:
* domain specificity (document relevance in regard of a particular domain)
* Jeremia (text pre-processing)
* Jesaja (keyword server)
* OpenRDF (access OpenRDF linked open data repositories)
* POS (part of speech tagging)
* Recognize (named entity recognition)
* Sentiment Analysis
