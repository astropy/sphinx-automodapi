# The following tests use a plain Python example module that is at
# sphinx_automodapi.tests.example_module.

# We store different cases in the cases sub-directory of the tests directory

import os
import sys
import glob
import shutil

import pytest

from copy import deepcopy, copy
from sphinx import build_main
from docutils.parsers.rst import directives, roles

CASES_ROOT = os.path.join(os.path.dirname(__file__), 'cases')

CASES_DIRS = glob.glob(os.path.join(CASES_ROOT, '*'))


def write_conf(filename, conf):
    with open(filename, 'w') as f:
        for key, value in conf.items():
            f.write("{0} = {1}\n".format(key, repr(conf[key])))



intersphinx_mapping = {
    'python': ('http://docs.python.org/{0}/'.format(sys.version_info[0]), None)
    }

DEFAULT_CONF = {'source_suffix': '.rst',
                'master_doc': 'index',
                'nitpicky': True,
                'extensions': ['sphinx.ext.intersphinx', 'sphinx_automodapi.automodapi'],
                'suppress_warnings': ['app.add_directive', 'app.add_node'],
                'intersphinx_mapping': intersphinx_mapping,
                'nitpick_ignore': [('py:class', 'sphinx_automodapi.tests.example_module.classes.BaseSpam')]}




def setup_function(func):
    # This can be replaced with the docutils_namespace context manager once
    # it is in a stable release of Sphinx
    func._directives = copy(directives._directives)
    func._roles = copy(roles._roles)


def teardown_function(func):
    directives._directives = func._directives
    roles._roles = func._roles


@pytest.mark.parametrize('case_dir', CASES_DIRS)
def test_run_full_case(tmpdir, case_dir):

    input_dir = os.path.join(case_dir, 'input')
    output_dir = os.path.join(case_dir, 'output')

    src_dir = tmpdir.mkdir('src').strpath

    conf = deepcopy(DEFAULT_CONF)
    conf.update({'automodapi_toctreedirnm': 'api',
                 'automodapi_writereprocessed': True,
                 'automodsumm_writereprocessed': True})

    if os.path.basename(case_dir) == 'mixed_toplevel':
        conf['extensions'].append('sphinx_automodapi.smart_resolver')

    write_conf(os.path.join(src_dir, 'conf.py'), conf)

    for input_file in glob.glob(os.path.join(input_dir, '*')):
        shutil.copy(input_file, os.path.join(src_dir, os.path.basename(input_file)))

    start_dir = os.path.abspath('.')

    try:
        os.chdir(src_dir)
        status = build_main(argv=('sphinx-build', '-W', '-b', 'html', '.', 'build/_html'))
    finally:
        os.chdir(start_dir)

    assert status == 0

    # Check that all expected output files are there and match the reference files
    for root, dirnames, filenames in os.walk(output_dir):
        for filename in filenames:
            path_reference = os.path.join(root, filename)
            path_relative = os.path.relpath(path_reference, output_dir)
            path_actual = os.path.join(src_dir, path_relative)
            assert os.path.exists(path_actual)
            actual = open(path_actual).read()
            reference = open(path_reference).read()
            assert actual.strip() == reference.strip()
            # if actual != reference:
            #     raise ValueError("Expected:\n\n{0}\n\nGot:\n\n{1}\n".format(reference, actual))
