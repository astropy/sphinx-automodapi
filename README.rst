|Azure Status| |Coverage Status| |PyPI|

About
=====

This is a Sphinx extension to automatically generate API pages for whole
modules. It was originally developed for the Astropy project but is now
available as a standalone package since it can be used for any other
package. The documentation can be found on
`ReadTheDocs <http://sphinx-automodapi.readthedocs.io/en/latest/>`_.

Proplot modifications
---------------------
This extension was forked from the Astropy project for use with the `proplot <https://github.com/lukelbd/proplot>`__ project in order to add some features. The following changes were made:

* Adds ``__getitem__``, ``__getattr__``, ``__setitem__``, and ``__setattr__`` to the list of builtin methods that are *not* ignored by the documentation generator.
* Skips over class methods that are public, but do *not* have their own ``__doc__`` attributes, to prevent inheriting and displaying documentation from external projects.
* Gives class methods and attributes their own stub pages, instead of putting all class methods and attributes on a single page. This also requires adding the new files to ``env.found_docs`` and reordering the event hooks so ``sphinx_automodapi`` is called before ``autosummary``. This way ``autosummary`` will read the automatically generated class pages and generate the corresponding stubs.


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
