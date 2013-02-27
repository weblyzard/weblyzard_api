from setuptools import setup, find_packages
from setuptools.command import sdist

setup (
    name = 'weblyzardServices',
    version = '0.1',
    description= ' Web services for weblyzard',
    author = 'Heinz-Peter Lang',
    author_email = 'lang@weblyzard.com',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['wl_core', 'twisted', ],
    scripts = ['src/weblyzardServices/scripts/start_wl_services.py' ],
    
)
