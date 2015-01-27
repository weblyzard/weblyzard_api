from setuptools import setup, find_packages
from setuptools.command import sdist

setup (
    name = 'weblyzard_api',
    version = '0.4.8.3',
    description= ' Web services for weblyzard',
    author = 'Heinz-Peter Lang and Albert Weichselbraun',
    author_email = 'lang@weblyzard.com',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['eWRT>=0.9.1.3', 
                        'nose',
                        'lxml',
                        'requests'],
    dependency_links = ['git+https://github.com/weblyzard/ewrt.git#egg=eWRT-0.9.1.4'],
zip_safe = False,
    scripts = ['src/weblyzard_api/client/openrdf/wl_upload_repository.py',]
)
