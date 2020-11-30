Documentation for sphinx-automodapi
===================================

The sphinx-automodapi package provides Sphinx directives that help faciliate
the automatic generation of API documentation pages for Python package modules.
It was originally developped for the Astropy project, but is now developed as a
standalone package that can be used for any project.

Installation
------------

This extension requires Sphinx 1.7 or later, and can be installed with::

    pip install sphinx-automodapi

The extension is also available through conda package management system. It can be installed with::

    conda install -c conda-forge sphinx-automodapi



.. _quickstart:

Quick start
-----------

To use this extension, you will need to add the following entry to the
``extensions`` list in your Sphinx ``conf.py`` file::

    extensions = ['sphinx_automodapi.automodapi']
    numpydoc_show_class_members = False

You can then add an ``automodapi`` block anywhere that you want to generate
documentation for a module::

    .. automodapi:: mypackage.mymodule

This will add a section with the docstring of the module, followed by a list of
functions, and by a list of classes. For each function and class, a full API
page will be generated. The ``numpydoc_show_class_members=False`` option is needed
to avoid having methods and attributes of classes being shown multiple times.

By default, sphinx_automodapi will try and make a diagram showing an
inheritance graph of all the classes in the module. This requires graphviz to
be installed. To disable the inheritance diagram, you can do::

    .. automodapi:: mypackage.mymodule
       :no-inheritance-diagram:

The ``automodapi`` directive takes other options that are described in more
detail in the `User guide`_ below.

If you are documenting a module which imports classes from other files, and you
want to include an inheritance diagram for the classes, you may run into Sphinx
warnings, because the class may be documented as e.g. ``astropy.table.Table``
but the class really lives at ``astropy.table.core.Table``. To fix this you can
make use of the ``'sphinx_automodapi.smart_resolver'`` Sphinx extension, which
will automatically try and resolve such differences. In this, case, be sure to
include::

    extensions = ['sphinx_automodapi.automodapi',
                  'sphinx_automodapi.smart_resolver']

in your ``conf.py`` file.

User guide
----------

.. toctree::
   :maxdepth: 1

   automodapi.rst
   automodsumm.rst

Dependency Version Guidelines
-----------------------------

As a general guideline, automodapi dependencies (at the time of writing, just
Sphinx) aim to maintain compatibility with versions <= 2 years old. Dependencies
may be newer, however, if specific features become important to help automodapi
work better or be more maintainable.
