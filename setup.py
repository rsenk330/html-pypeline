import pypeline

from setuptools import setup, find_packages

requires = []

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
