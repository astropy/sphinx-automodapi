# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

import os
import sys
from copy import deepcopy

from .test_cases import write_conf, SPHINX_LT_17, build_main
from . import cython_testpackage  # noqa

__all__ = ['run_sphinx_in_tmpdir']

intersphinx_mapping = {
    'python': ('https://docs.python.org/{0}/'.format(sys.version_info[0]), None)
    }


DEFAULT_CONF = {'source_suffix': '.rst',
                'master_doc': 'index',
                'nitpicky': True,
                'extensions': ['sphinx.ext.intersphinx', 'sphinx_automodapi.automodapi'],
                'suppress_warnings': ['app.add_directive', 'app.add_node'],
                'intersphinx_mapping': intersphinx_mapping,
                'automodapi_toctreedirnm': 'api',
                'automodapi_writereprocessed': True,
                'automodapi_inheritance_diagram': True,
                'automodsumm_writereprocessed': True}


def run_sphinx_in_tmpdir(tmpdir, additional_conf={}, expect_error=False):

    start_dir = os.path.abspath('.')

    conf = deepcopy(DEFAULT_CONF)
    conf.update(additional_conf)

    write_conf(tmpdir.join('conf.py').strpath, conf)

    argv = ['-W', '-b', 'html', '.', '_build/html']
    if SPHINX_LT_17:
        # As of Sphinx 1.7, the first argument is now no longer ignored
        argv.insert(0, 'sphinx-build')

    try:
        os.chdir(tmpdir.strpath)
        status = build_main(argv=argv)
    finally:
        os.chdir(start_dir)

    if expect_error:
        assert status != 0
    else:
        assert status == 0