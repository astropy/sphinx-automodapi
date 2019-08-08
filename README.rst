|Travis Status| |AppVeyor status| |Coverage Status| |PyPI|

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

.. |Travis Status| image:: https://travis-ci.org/astropy/sphinx-automodapi.svg?branch=master
   :target: https://travis-ci.org/astropy/sphinx-automodapi
.. |AppVeyor status| image:: https://ci.appveyor.com/api/projects/status/warwyfj06t1rkn5p/branch/master?svg=true
   :target: https://ci.appveyor.com/project/Astropy/sphinx-automodapi/branch/master
.. |Coverage Status| image:: https://codecov.io/gh/astropy/sphinx-automodapi/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/astropy/sphinx-automodapi
.. |PyPI| image:: https://img.shields.io/pypi/v/sphinx-automodapi.svg
   :target: https://pypi.python.org/pypi/sphinx-automodapi
