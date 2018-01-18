Changes in sphinx-automodapi
============================

0.8 (unreleased)
----------------

- No changes yet.

0.7 (2018-01-18)
----------------

- Fix compatibility with Sphinx 1.7.x. [#43]

0.6 (2017-07-05)
----------------

- Fix encoding issues on platforms that default to e.g. ASCII encoding. [#33]

0.5 (2017-05-29)
----------------

- Fix a bug that caused the :inherited-members: option to apply to all subsequent
  automodapi directives. [#25]

0.4 (2017-05-24)
----------------

- Fix compatibility with Sphinx 1.6 and 1.7. [#22, #23]

- Introduce a new ``:include-all-objects:`` option to ``automodapi`` that will
  include not just functions and classes in a module, but also all other
  objects. To help this, introduce a new ``:variables-only:`` option for
  ``automodsumm``. [#24]

0.3 (2017-02-20)
----------------

- Fixed installation on Python 3.4. [#21]

0.2 (2016-12-28)
----------------

- Suppress warning about re-defining autoattribute in recent versions of
  Sphinx. [#8]

- Avoid hard-coding sphinx_automodapi module name in case this extension is
  bundled into another package. [#12]

- Fix use of automodapi when source files are inside a source directory. [#16]

- Make sure generated rst is tidy and doesn't include extraneous whitespace. [#18]

0.1 (2016-12-12)
----------------

- Fixed a bug that caused the automodapi directive to not work properly when
  the main module docstring was not included. [#3]

- Fixed a bug that caused skipped classes in automodapi directives to still
  be included in inheritance diagrams. [#3]

- Original code taken out of astropy-helpers
