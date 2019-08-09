# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

import pytest

from . import cython_testpackage  # noqa
from .helpers import run_sphinx_in_tmpdir

pytest.importorskip('sphinx')  # skips these tests if sphinx not present


am_replacer_str = """
This comes before

.. automodapi:: sphinx_automodapi.tests.example_module.mixed
{options}

This comes after
"""

am_replacer_basic_expected = """
This comes before


sphinx_automodapi.tests.example_module.mixed Module
---------------------------------------------------

.. automodule:: sphinx_automodapi.tests.example_module.mixed

Functions
^^^^^^^^^

.. automodsumm:: sphinx_automodapi.tests.example_module.mixed
    :functions-only:
    :toctree: api

Classes
^^^^^^^

.. automodsumm:: sphinx_automodapi.tests.example_module.mixed
    :classes-only:
    :toctree: api

Class Inheritance Diagram
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automod-diagram:: sphinx_automodapi.tests.example_module.mixed
    :private-bases:
    :parts: 1

This comes after
"""


def test_am_replacer_basic(tmpdir):
    """
    Tests replacing an ".. automodapi::" with the automodapi no-option
    template
    """

    with open(tmpdir.join('index.rst').strpath, 'w') as f:
        f.write(am_replacer_str.format(options=''))

    run_sphinx_in_tmpdir(tmpdir)

    with open(tmpdir.join('index.rst.automodapi')) as f:
        result = f.read()

    assert result == am_replacer_basic_expected


am_replacer_repr_str = u"""
This comes before with spéciàl çhars

.. automodapi:: sphinx_automodapi.tests.example_module.mixed
{options}

This comes after
"""


@pytest.mark.parametrize('writereprocessed', [False, True])
def test_am_replacer_writereprocessed(tmpdir, writereprocessed):
    """
    Tests the automodapi_writereprocessed option
    """

    with open(tmpdir.join('index.rst').strpath, 'w') as f:
        f.write(am_replacer_repr_str.format(options=''))

    run_sphinx_in_tmpdir(tmpdir, additional_conf={'automodapi_writereprocessed': writereprocessed})

    assert tmpdir.join('index.rst.automodapi').isfile() is writereprocessed


am_replacer_noinh_expected = """
This comes before


sphinx_automodapi.tests.example_module.mixed Module
---------------------------------------------------

.. automodule:: sphinx_automodapi.tests.example_module.mixed

Functions
^^^^^^^^^

.. automodsumm:: sphinx_automodapi.tests.example_module.mixed
    :functions-only:
    :toctree: api

Classes
^^^^^^^

.. automodsumm:: sphinx_automodapi.tests.example_module.mixed
    :classes-only:
    :toctree: api


This comes after
""".format(empty='')


def test_am_replacer_noinh(tmpdir):
    """
    Tests replacing an ".. automodapi::" with no-inheritance-diagram
    option
    """

    ops = ['', ':no-inheritance-diagram:']
    ostr = '\n    '.join(ops)

    with open(tmpdir.join('index.rst').strpath, 'w') as f:
        f.write(am_replacer_str.format(options=ostr))

    run_sphinx_in_tmpdir(tmpdir)

    with open(tmpdir.join('index.rst.automodapi')) as f:
        result = f.read()

    assert result == am_replacer_noinh_expected


am_replacer_titleandhdrs_expected = """
This comes before


sphinx_automodapi.tests.example_module.mixed Module
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

.. automodule:: sphinx_automodapi.tests.example_module.mixed

Functions
*********

.. automodsumm:: sphinx_automodapi.tests.example_module.mixed
    :functions-only:
    :toctree: api

Classes
*******

.. automodsumm:: sphinx_automodapi.tests.example_module.mixed
    :classes-only:
    :toctree: api

Class Inheritance Diagram
*************************

.. automod-diagram:: sphinx_automodapi.tests.example_module.mixed
    :private-bases:
    :parts: 1


This comes after
"""


def test_am_replacer_titleandhdrs(tmpdir):
    """
    Tests replacing an ".. automodapi::" entry with title-setting and header
    character options.
    """

    ops = ['', ':headings: &*']
    ostr = '\n    '.join(ops)

    with open(tmpdir.join('index.rst').strpath, 'w') as f:
        f.write(am_replacer_str.format(options=ostr))

    run_sphinx_in_tmpdir(tmpdir)

    with open(tmpdir.join('index.rst.automodapi')) as f:
        result = f.read()

    assert result == am_replacer_titleandhdrs_expected


EXPECTED_HEADINGS_STDERR = """
Warning, treated as error:
Not enough headings (got 1, need 2), using default -^
"""


def test_am_replacer_titleandhdrs_invalid(tmpdir, capsys):
    """
    Tests replacing an ".. automodapi::" entry with title-setting and header
    character options.
    """

    ops = ['', ':headings: &']
    ostr = '\n    '.join(ops)

    with open(tmpdir.join('index.rst').strpath, 'w') as f:
        f.write(am_replacer_str.format(options=ostr))

    run_sphinx_in_tmpdir(tmpdir, expect_error=True)

    stdout, stderr = capsys.readouterr()
    assert stderr.strip() == EXPECTED_HEADINGS_STDERR.strip()


am_replacer_nomain_str = """
This comes before

.. automodapi:: sphinx_automodapi.tests.example_module.functions
    :no-main-docstr:

This comes after
"""

am_replacer_nomain_expected = """
This comes before


sphinx_automodapi.tests.example_module.functions Module
-------------------------------------------------------



Functions
^^^^^^^^^

.. automodsumm:: sphinx_automodapi.tests.example_module.functions
    :functions-only:
    :toctree: api


This comes after
""".format(empty='')


def test_am_replacer_nomain(tmpdir):
    """
    Tests replacing an ".. automodapi::" with "no-main-docstring" .
    """

    with open(tmpdir.join('index.rst').strpath, 'w') as f:
        f.write(am_replacer_nomain_str.format(options=''))

    run_sphinx_in_tmpdir(tmpdir)

    with open(tmpdir.join('index.rst.automodapi')) as f:
        result = f.read()

    assert result == am_replacer_nomain_expected


am_replacer_skip_str = """
This comes before

.. automodapi:: sphinx_automodapi.tests.example_module.functions
    :skip: add
    :skip: subtract

This comes after
"""

am_replacer_skip_expected = """
This comes before


sphinx_automodapi.tests.example_module.functions Module
-------------------------------------------------------

.. automodule:: sphinx_automodapi.tests.example_module.functions

Functions
^^^^^^^^^

.. automodsumm:: sphinx_automodapi.tests.example_module.functions
    :functions-only:
    :toctree: api
    :skip: add,subtract


This comes after
""".format(empty='')


def test_am_replacer_skip(tmpdir):
    """
    Tests using the ":skip: option in an ".. automodapi::" .
    """

    with open(tmpdir.join('index.rst').strpath, 'w') as f:
        f.write(am_replacer_skip_str.format(options=''))

    run_sphinx_in_tmpdir(tmpdir)

    with open(tmpdir.join('index.rst.automodapi')) as f:
        result = f.read()

    assert result == am_replacer_skip_expected


am_replacer_invalidop_str = """
This comes before

.. automodapi:: sphinx_automodapi.tests.example_module.functions
    :invalid-option:

This comes after
"""

EXPECTED_INVALID_STDERR = """
Warning, treated as error:
Found additional options invalid-option in automodapi.
"""


def test_am_replacer_invalidop(tmpdir, capsys):
    """
    Tests that a sphinx warning is produced with an invalid option.
    """

    with open(tmpdir.join('index.rst').strpath, 'w') as f:
        f.write(am_replacer_invalidop_str.format(options=''))

    run_sphinx_in_tmpdir(tmpdir, expect_error=True)

    stdout, stderr = capsys.readouterr()
    assert stderr.strip() == EXPECTED_INVALID_STDERR.strip()


am_replacer_cython_str = """
This comes before

.. automodapi:: apyhtest_eva.unit02
{options}

This comes after
"""

am_replacer_cython_expected = """
This comes before


apyhtest_eva.unit02 Module
--------------------------

.. automodule:: apyhtest_eva.unit02

Functions
^^^^^^^^^

.. automodsumm:: apyhtest_eva.unit02
    :functions-only:
    :toctree: api

This comes after
""".format(empty='')


def test_am_replacer_cython(tmpdir, cython_testpackage):  # noqa
    """
    Tests replacing an ".. automodapi::" for a Cython module.
    """

    with open(tmpdir.join('index.rst').strpath, 'w') as f:
        f.write(am_replacer_cython_str.format(options=''))

    run_sphinx_in_tmpdir(tmpdir)

    with open(tmpdir.join('index.rst.automodapi')) as f:
        result = f.read()

    assert result == am_replacer_cython_expected
