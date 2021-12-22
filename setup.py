#!/usr/bin/env python

import os
from setuptools import setup

setup(use_scm_version={'write_to': os.path.join('sphinx_automodapi', 'version.py')})
