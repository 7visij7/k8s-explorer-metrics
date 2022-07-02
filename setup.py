#!/usr/bin/env python3

from setuptools import find_packages, setup


NAME = 'explorer-metrics'
DESCRIPTION = 'Explorer metrics '
URL = 'https://git.company.com/sre/explorer-metrics'
AUTHOR = 'eilchenko'
EMAIL = 'eilchenko@team.company.com'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = 1.0
REQUIRED = [
    'requests',
    'connexion',
    'tornado',
    'swagger-ui-bundle',
    'kubernetes',
    'company'
]


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    include_package_data=True,
    entry_points={
        'console_scripts':
            [
                'daemon = explorer:daemon',
             ]
    }
)