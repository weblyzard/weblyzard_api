## The webLyzard API

Provides access to all webLyzard Web services.

Full Documentation in http://weblyzard-api.readthedocs.org/en/latest/

### Configuration

The API needs to know the URL, user and password used for the Web service. These data may be 

1. passed by a client at class initialization, or
2. automatically set by the means of the following environment variables:
  + `WEBLYZARD_API_URL`
  + `WEBLYZARD_API_USER`
  + `WEBLYZARD_API_PASS`

   this is also the preferred way for running unit tests.

The preferred way for setting these variables is using `.bash_profile`.

```sh
export WEBLYZARD_API_URL="https://noah.semanticlab.net/ws"
export WEBLYZARD_API_USER="user"
export WEBLYZARD_API_PASS="pass"
```

Do not set `WEBLYZARD_API_USER` and `WEBLYZARD_API_PASS` if your Web service does not require authentication.

If you have already set the variables using `.bash_profile`, when you run a script from the command line is also recommended to use:

```sh
source ~/.bash_profile
```

### Available interfaces:

The following interfaces are currently available for `weblyzard_api`:

+ domain specificity (document relevance in regard of a particular domain)
+ Jeremia (text pre-processing)
+ Jesaja (keyword server)
+ OpenRDF (access OpenRDF linked open data repositories)
+ POS (part of speech tagging)
+ Recognize (named entity recognition)
+ Sentiment Analysis

### Programming Guidelines

+ Required documentation for public methods
  + docstring explaining what the method does
  + a unit test demonstrating the method's usage in the wild.
+ commits must pass all unit tests

