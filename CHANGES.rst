Changes in sphinx-automodapi
============================

0.2 (unreleased)
----------------

- Suppress warning about re-defining autoattribute in recent versions of
  Sphinx. [#8]

- Avoid hard-coding sphinx_automodapi module name in case this extension is
  bundled into another package. [#12]

- Fix use of automodapi when source files are inside a source directory. [#16]

0.1 (2016-12-12)
----------------

- Fixed a bug that caused the automodapi directive to not work properly when
  the main module docstring was not included. [#3]

- Fixed a bug that caused skipped classes in automodapi directives to still
  be included in inheritance diagrams. [#3]

- Original code taken out of astropy-helpers
