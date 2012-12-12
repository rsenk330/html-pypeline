import os

import pypeline

from setuptools import setup, find_packages

requires = [
    'misaka',
]

# Only include stuff for "development" by looking for a file
# called ``./script/.devel``
if os.path.exists("./script/.devel"):
    requires.extend([
        'nose>=1.0',
        'coverage>=3.5.3',
    ])

setup(
    name='pypeline',
    version=pypeline.__version__,
    description="HTML filters and utilities (python implementation of html-pipeline)",
    long_description=open('README.md').read(),
    packages=find_packages(),
    scripts=[],
    install_requires=requires,
    include_package_data=True,
    zip_safe=True
)
