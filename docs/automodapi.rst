Automatically generating module documentation with automodapi
=============================================================

.. _automodapi:

Overview
--------

The main Sphinx directive provided by the sphinx-automodapi package is the
``automodapi`` directive. As described in the :ref:`quickstart` guide,
before you use the directive, you will need to make sure the following
extension is included in the ``extensions`` entry of your documentation's
``conf.py`` file::

    extensions = ['sphinx_automodapi.automodapi']

You can then add an ``automodapi`` block anywhere that you want to generate
documentation for a module::

  .. automodapi:: mypackage.mymodule
     <options go here>

This will add a section with the docstring of the module, followed by a list of
functions, and by a list of classes. For each function and class, a full API
page will be generated.

The automodapi directive and allowed options are described in more detail below.

In detail
---------

.. automodule:: sphinx_automodapi.automodapi
