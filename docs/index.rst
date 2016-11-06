Documentation for sphinx-automodapi
===================================

The sphinx-automodapi package provides Sphinx directives that help faciliate
the automatic generation of API documentation pages for Python package modules.
It was originally developped for the Astropy project, but is now developed as a
standalone package that can be used for any project.

Installation
------------

This extension requires Sphinx 1.2 or later, and at the moment can be installed
by cloning the repository then running::

    python setup.py install

However, we will soon release a version on PyPI, at which point it will be
possible to do::

    pip install sphinx-automodapi

Quick start
-----------

To use this extension, you will need to add the following entries to the
``extensions`` list in your Sphinx ``conf.py`` file::

    extensions = ['sphinx.ext.autosummary',
                  'sphinx_automodapi.automodsumm',
                  'sphinx_automodapi.automodapi']

.. TODO: we could make automodsumm be automatically set up when automodapi is set up

You can then add an ``automodapi`` block anywhere that you want to generate
documentation for a module::

    .. automodapi:: mypackage.mymodule

This will add a section with the docstring of the module, followed by a list of
functions, and by a list of classes. For each function and class, a full API
page will be generated.

By default, sphinx_automodapi will try and make a diagram showing an
inheritance graph of all the classes in the module. This requires graphviz to
be installed. To disable the inheritance diagram, you can do::

    .. automodapi:: mypackage.mymodule
       :no-inheritance-diagram:

.. TODO: disable inheritance diagram by default!

.. TODO: mention about api directory being excluded
