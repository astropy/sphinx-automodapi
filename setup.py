#!/usr/bin/env python

# Licensed under a 3-clause BSD style license - see LICENSE.rst

from setuptools import setup

setup(
    name='sphinx-automodapi',
    version='0.1.dev',
    description='Sphinx extension for auto-generating API documentation for entire modules',
    author='The Astropy Developers',
    author_email='astropy.team@gmail.com',
    license='BSD',
    url='http://astropy.org',
    zip_safe=False,
    packages=['sphinx_automodapi'],
    package_data = {'sphinx_automodapi': ['templates/*/*.rst']})
