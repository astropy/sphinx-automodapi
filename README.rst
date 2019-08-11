|Azure Status| |Coverage Status| |PyPI|

About
=====

This is a Sphinx extension to automatically generate API pages for whole
modules. It was originally developed for the Astropy project but is now
available as a standalone package since it can be used for any other
package. The documentation can be found on
`ReadTheDocs <http://sphinx-automodapi.readthedocs.io/en/latest/>`_.

Running tests
-------------

To run the tests, you can either do::

    pytest sphinx_automodapi

or if you have `tox <https://tox.readthedocs.io/en/latest/>`_ installed::

    tox -e test

.. |Azure Status| image:: https://dev.azure.com/astropy-project/sphinx-automodapi/_apis/build/status/astropy.sphinx-automodapi?branchName=master
   :target: https://dev.azure.com/astropy-project/sphinx-automodapi/_build/latest?definitionId=2&branchName=master
.. |Coverage Status| image:: https://codecov.io/gh/astropy/sphinx-automodapi/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/astropy/sphinx-automodapi
.. |PyPI| image:: https://img.shields.io/pypi/v/sphinx-automodapi.svg
   :target: https://pypi.python.org/pypi/sphinx-automodapi
