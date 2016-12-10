Generating tables of module objects with automodsumm
====================================================

.. _automodsumm:

Overview
--------

The ``automodsumm`` directive takes all objects in a
module and generates a table of these objects and associated API pages. The
:ref:`automodapi <automodapi>` directive then calls ``automodsumm`` once for
functions and once for classes, and adds the module docstring - but effectively,
the bulk of the work in creating the API tables and pages is done by
``automodsumm``.

Nevertheless, in most cases, users should not need to call ``automodsumm``
directly, except if finer control is desired. The syntax of the directive is::

    .. automodsumm:: mypackage.mymodule
       <options go here>

The automodsumm directive is described in more detail below.

In detail
---------

.. automodule:: sphinx_automodapi.automodsumm
