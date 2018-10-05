## Java Examples to be used with the webLyzard api

### Keyword Extractor
Extracts keywords from document corpora. The keyword extractor is trained with a reference corpus that contains documents typical to the chosen domain. 

#### Usage:

```bash
Usage: java -jar example-keyword-extractor OPTIONS
OPTIONS:
  --[no]help [-h] (a boolean; default: "false")
    Print usage info.
  --Profile name [-n] (a string; default: "default")
    Profile name used for the trained keyword extraction model.
  --Reference documents [-r] (a string; default: "")
    Directory with the reference documents used to train the keyword extraction.
  --Target documents [-t] (a string; default: "")
    Directory with the documents to annotate.
  --Web service base URL [-b] (a string; default: "")
    webLyzard API base URL.
  --Web service user name [-u] (a string; default: "")
    webLyzard API user name.
  --Web service password [-p] (a string; default: "")
    webLyzard API password.
```

#### Example:
```bash
java -jar ./target/example-keyword-extractor-0.0.1-jar-with-dependencies.jar  -r ~/corpus/reference-documents/ -t ~/documents/ -b http://localhost -u username -p password -n testrun1
``` 

Trains the keyword extraction model `testrun1` with the documents provided at `~/corpus/reference-documents/` and tags all documents found in `~/documents/` afterwards.
