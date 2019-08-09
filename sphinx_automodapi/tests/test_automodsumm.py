# Licensed under a 3-clause BSD style license - see LICENSE.rst

# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

import pytest

from . import cython_testpackage  # noqa
from .helpers import run_sphinx_in_tmpdir

pytest.importorskip('sphinx')  # skips these tests if sphinx not present

# nosignatures

ADD_RST = """
:orphan:

add
===

.. currentmodule:: sphinx_automodapi.tests.example_module.mixed

.. autofunction:: add
""".strip()

MIXEDSPAM_RST = """
:orphan:

MixedSpam
=========

.. currentmodule:: sphinx_automodapi.tests.example_module.mixed

.. autoclass:: MixedSpam
   :show-inheritance:
""".strip()


def write_api_files_to_tmpdir(tmpdir):
    apidir = tmpdir.mkdir('api')
    with open(apidir.join('sphinx_automodapi.tests.example_module.mixed.add.rst'), 'w') as f:
        f.write(ADD_RST)
    with open(apidir.join('sphinx_automodapi.tests.example_module.mixed.MixedSpam.rst'), 'w') as f:
        f.write(MIXEDSPAM_RST)



ams_to_asmry_str = """
Before

.. automodsumm:: sphinx_automodapi.tests.example_module.mixed
{options}

And After
"""

ams_to_asmry_expected = """\
.. currentmodule:: sphinx_automodapi.tests.example_module.mixed

.. autosummary::

    add
    MixedSpam

"""


def test_ams_to_asmry(tmpdir):

    with open(tmpdir.join('index.rst').strpath, 'w') as f:
        f.write(ams_to_asmry_str.format(options=''))

    write_api_files_to_tmpdir(tmpdir)

    run_sphinx_in_tmpdir(tmpdir)

    with open(tmpdir.join('index.rst.automodsumm')) as f:
        result = f.read()

    assert result == ams_to_asmry_expected


EXPECTED_OPTIONS_STDERR = """
Warning, treated as error:
[automodsumm] Defined more than one of functions-only, classes-only, and variables-only.  Skipping this directive.
"""

def test_too_many_options(tmpdir, capsys):

    ops = ['', ':classes-only:', ':functions-only:']
    ostr = '\n    '.join(ops)

    with open(tmpdir.join('index.rst').strpath, 'w') as f:
        f.write(ams_to_asmry_str.format(options=ostr))

    write_api_files_to_tmpdir(tmpdir)

    run_sphinx_in_tmpdir(tmpdir, expect_error=True)

    stdout, stderr = capsys.readouterr()
    assert stderr.strip() == EXPECTED_OPTIONS_STDERR.strip()



PILOT_RST = """
:orphan:

pilot
=====

.. currentmodule:: apyhtest_eva.unit02

.. autofunction:: pilot
""".strip()

ams_cython_str = """
Before

.. automodsumm:: apyhtest_eva.unit02
    :functions-only:

And After
"""

ams_cython_expected = """\
.. currentmodule:: apyhtest_eva.unit02

.. autosummary::

    pilot

"""


def test_ams_cython(tmpdir, cython_testpackage):  # noqa

    with open(tmpdir.join('index.rst').strpath, 'w') as f:
        f.write(ams_cython_str)

    apidir = tmpdir.mkdir('api')
    with open(apidir.join('apyhtest_eva.unit02.pilot.rst'), 'w') as f:
        f.write(PILOT_RST)

    run_sphinx_in_tmpdir(tmpdir)

    with open(tmpdir.join('index.rst.automodsumm')) as f:
        result = f.read()

    assert result == ams_cython_expected