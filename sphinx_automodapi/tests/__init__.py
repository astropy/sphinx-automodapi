import sys

from textwrap import dedent

from setuptools.sandbox import run_setup

import pytest

@pytest.fixture
def cython_testpackage(tmpdir, request):
    """
    Creates a trivial Cython package for use with tests.
    """

    test_pkg = tmpdir.mkdir('test_pkg')
    test_pkg.mkdir('_eva_').ensure('__init__.py')
    test_pkg.join('_eva_').join('unit02.pyx').write(dedent("""\
        def pilot():
            \"\"\"Returns the pilot of Eva Unit-02.\"\"\"

            return True
    """))

    test_pkg.join('setup.py').write(dedent("""\
        from os.path import join
        from setuptools import setup, Extension
        from astropy_helpers.setup_helpers import register_commands

        NAME = '_eva_'
        VERSION = 0.1
        RELEASE = True

        cmdclassd = register_commands(NAME, VERSION, RELEASE)

        setup(
            name=NAME,
            version=VERSION,
            cmdclass=cmdclassd,
            ext_modules=[Extension('_eva_.unit02',
                                   [join('_eva_', 'unit02.pyx')])]
        )
    """))

    test_pkg.chdir()
    run_setup('setup.py', ['build_ext', '--inplace'])

    sys.path.insert(0, str(test_pkg))
    import _eva_.unit02

    def cleanup(test_pkg=test_pkg):
        for modname in ['_eva_', '_eva_.uint02']:
            try:
                del sys.modules[modname]
            except KeyError:
                pass

        sys.path.remove(str(test_pkg))

    request.addfinalizer(cleanup)

    return test_pkg
