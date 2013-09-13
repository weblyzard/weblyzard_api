'''
@package weblyzard_api.client
webLyzard web service clients

@author Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''
from os import getenv

WEBLYZARD_API_URL  = getenv("WEBLYZARD_API_URL") or "http://localhost:8080"
WEBLYZARD_API_USER = getenv("WEBLYZARD_API_USER")
WEBLYZARD_API_PASS = getenv("WEBLYZARD_API_PASS")


