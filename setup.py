#!/usr/bin/env python

# Licensed under a 3-clause BSD style license - see LICENSE.rst

from setuptools import setup

with open('README.rst') as infile:
    long_description = infile.read()

from sphinx_automodapi import __version__

setup(
    name='sphinx-automodapi',
    version=__version__,
    description='Sphinx extension for auto-generating API documentation for entire modules',
    long_description=long_description,
    author='The Astropy Developers',
    author_email='astropy.team@gmail.com',
    license='BSD',
    url='http://astropy.org',
    zip_safe=False,
    packages=['sphinx_automodapi'],
    package_data = {'sphinx_automodapi': ['templates/*/*.rst']})
