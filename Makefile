PROJECT=weblyzard_api

####### PYTHON #######

clear-cov:
	rm coverage.xml
test-unit:
	PYTHONPATH=src/python py.test -x --cov=weblyzard_api --cov-report xml src/python/weblyzard_api/tests --collect-only
