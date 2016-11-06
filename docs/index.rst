Documentation for sphinx_automodapi
===================================

The sphinx-automodapi package provides Sphinx directives that help faciliate
the automatic generation of API documentation pages for Python package modules.
It was originally developped for the Astropy project, but is now developed as a
standalone package that can be used for any project.

Installation
------------

This extension requires Sphinx 1.2 or later, and at the moment can be installed
by cloning the repository then running:

    python setup.py install

However, we will soon release a version on PyPI, at which point it will be
possible to do:

    pip install sphinx-automodapi

Usage
-----

To use this extension, you will need to add the following entries to the
``extensions`` list in your Sphinx ``conf.py`` file:

    extensions = ['sphinx_automodapi.automodsumm',
                  'sphinx_automodapi.automodapi']

You can then add an ``automodapi`` block anywhere that you want to generate
documentation for a module:

    .. automodapi:: mypackage.mymodule

This will add a section with a list of objects (functions, classes, etc.),
and for objects like classes, a table of attributes/methods will be shown.
