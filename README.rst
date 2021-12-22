|CI Status| |Coverage Status| |PyPI|

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

.. |CI Status| image:: https://github.com/astropy/sphinx-automodapi/workflows/CI/badge.svg
  :target: https://github.com/astropy/sphinx-automodapi/actions
.. |Coverage Status| image:: https://codecov.io/gh/astropy/sphinx-automodapi/branch/main/graph/badge.svg
  :target: https://codecov.io/gh/astropy/sphinx-automodapi
.. |PyPI| image:: https://img.shields.io/pypi/v/sphinx-automodapi.svg
  :target: https://pypi.python.org/pypi/sphinx-automodapi

Development status
------------------

Due to the limitations of FOSS development model, the Astropy Project
does not have enough bandwidth to add new features or fixes to this
package beyond what is necessary for the project itself. Therefore,
we apologize for any inconvenience caused by unresolved open issues
and unmerged stale pull requests. If you have any questions or concerns,
please contact the project via https://www.astropy.org/help .
Thank you for your interest in this package!
