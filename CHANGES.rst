Changes in sphinx-automodapi
============================

0.14.1 (2022-01-12)
-------------------

- Fixed issue with ``:skip:`` introduced by ``:include:`` feature. [#142]

0.14.0 (2021-12-22)
-------------------

- Set default value for ``env.intersphinx_named_inventory``. [#136]

- Sphinx 4 compatibility w.r.t. logger warning. [#129]

- Add ``:include:`` option to do the opposite of ``:skip:``. [#127]

- Various infrastructure/packaging updates and code clean-ups.
  Minimum supported Python version is now 3.7 and Sphinx 2.
  [#120, #124, #126, #133, #139]

0.13 (2020-09-24)
-----------------

- Fixed implementation of ``allowed-package-names`` option (which did
  not work at all). [#111]

- Ensure that generated files are always in .rst. [#112]

- Update minimum required Python version to 3.6. [#117]

- Fixed compatibility with Sphinx 3.0 and later. [#100]

0.12 (2019-08-15)
-----------------

- Fixed compatibility with Sphinx 2.0 and later. [#86]

- Updated required version of Sphinx to 1.7 and later. [#88]

0.11 (2019-05-29)
-----------------

- Added a global configuration option ``automodapi_inheritance_diagram`` to
  control whether inheritance diagrams are shown by default. [#75]

- Fix bug with smart_resolver when intersphinx inventory doesn't include
  any py:class entries. [#76]

- Fixed compatibility with Sphinx 2.0 and later. [#79]

0.10 (2019-01-09)
-----------------

- Fixed compatibility with latest developer version of Sphinx. [#61]

0.9 (2018-11-07)
----------------

- Fix issue with ABC-derived classes (``abc`` and ``collections.abc`` modules)
  having their members ignored in Python 3. This was only an issue when
  ``:inherited-members:`` was not in effect. [#53]

0.8 (2018-10-18)
----------------

- Fixed compatibility with Sphinx 1.8.x. [#51]

- Make all extensions parallel-friendly. [#44]

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
