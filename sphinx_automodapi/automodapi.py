# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
This directive takes a single argument that must be a module or package. It
will produce a block of documentation that includes the docstring for the
package, an :ref:`automodsumm` directive, and an :ref:`automod-diagram` if
there are any classes in the module. If only the main docstring of the
module/package is desired in the documentation, use `automodule`_ instead of
`automodapi`_.

It accepts the following options:

    * ``:include-all-objects:``
        If present, include not just functions and classes, but all objects.
        This includes variables, for which a possible docstring after the
        variable definition will be shown.

    * ``:inheritance-diagram:`` / ``:no-inheritance-diagram:``
        Specify whether or not to show the inheritance diagram for classes. This
        overrides the default global configuration set in
        ``automodapi_inheritance_diagram``.

    * ``:skip: str``
        This option results in the
        specified object being skipped, that is the object will *not* be
        included in the generated documentation. This option may appear
        any number of times to skip multiple objects.

    * ``:include: str``
        This option is the opposite of :skip: -- if specified, only the object
        names that match any of the names passed to :include: will be included
        in the generated documentation. This option may appear multiple times
        to include multiple objects.

    * ``:no-main-docstr:``
        If present, the docstring for the module/package will not be generated.
        The function and class tables will still be used, however.

    * ``:headings: str``
        Specifies the characters (in one string) used as the heading
        levels used for the generated section. This must have at least 2
        characters (any after 2 will be ignored). This also *must* match
        the rest of the documentation on this page for sphinx to be
        happy. Defaults to "-^", which matches the convention used for
        Python's documentation, assuming the automodapi call is inside a
        top-level section (which usually uses '=').

    * ``:no-heading:``
        If specified do not create a top level heading for the section.
        That is, do not create a title heading with text like "packagename
        Package".  The actual docstring for the package/module will still be
        shown, though, unless ``:no-main-docstr:`` is given.

    * ``:allowed-package-names: str``
        Specifies the packages that functions/classes documented here are
        allowed to be from, as comma-separated list of package names. If not
        given, only objects that are actually in a subpackage of the package
        currently being documented are included.

    * ``:inherited-members:`` / ``:no-inherited-members:``
        The global sphinx configuration option
        ``automodsumm_inherited_members`` decides if members that a class
        inherits from a base class are included in the generated
        documentation. The option ``:inherited-members:`` or ``:no-inherited-members:``
        allows the user to overrride the global setting.

    * ``:noindex:``
        Propagates the ``noindex`` flag to autodoc. Use it to avoid duplicate
        objects warnings.

    * ``:sort:``
        If the module contains ``__all__``, sort the module's objects
        alphabetically (if ``__all__`` is not present, the objects are found
        using `dir`, which always gives a sorted list).


This extension also adds five sphinx configuration options:

* ``automodapi_inheritance_diagram``
    Should be a boolean that indicates whether to show inheritance diagrams
    by default. This can be overriden on a case by case basis with
    ``:inheritance-diagram:`` and ``:no-inheritance-diagram:``. Defaults to
    ``True``.

* ``automodapi_toctreedirnm``
    This must be a string that specifies the name of the directory the
    automodsumm generated documentation ends up in. This directory path should
    be relative to the documentation root (e.g., same place as ``index.rst``).
    Defaults to ``'api'``.

* ``automodapi_writereprocessed``
    Should be a bool, and if `True`, will cause `automodapi`_ to write files
    with any `automodapi`_ sections replaced with the content Sphinx
    processes after `automodapi`_ has run.  The output files are not
    actually used by sphinx, so this option is only for figuring out the
    cause of sphinx warnings or other debugging.  Defaults to `False`.

* ``automodsumm_inherited_members``
    Should be a bool and if ``True`` members that a class inherits from a base
    class are included in the generated documentation. Defaults to ``False``.

* ``automodsumm_included_members``
    A list of strings containing the names of hidden class members that should be
    included in the documentation. This is most commonly used to add special class
    methods like ``__getitem__`` and ``__setitem__``. Defaults to
    ``['__init__', '__call__']``.

* ``automodsumm_properties_are_attributes``
    Should be a bool and if ``True`` properties are treated as attributes in the
    documentation meaning that no property specific documentation is generated.
    Defaults to ``True``.

.. _automodule: http://sphinx-doc.org/latest/ext/autodoc.html?highlight=automodule#directive-automodule
"""

# Implementation note:
# The 'automodapi' directive is not actually implemented as a docutils
# directive. Instead, this extension searches for the 'automodapi' text in
# all sphinx documents, and replaces it where necessary from a template built
# into this extension. This is necessary because automodsumm (and autosummary)
# use the "builder-inited" event, which comes before the directives are
# actually built.

import inspect
import os
import re
import sys

from sphinx.util import logging

from .utils import find_mod_objs

__all__ = []

automod_templ_modheader = """
{modname} {pkgormod}
{modhds}{pkgormodhds}

{automoduleline}
"""

automod_templ_classes = """
Classes
{clshds}

.. automodsumm:: {modname}
    :classes-only:
    {clsfuncoptions}
"""

automod_templ_funcs = """
Functions
{funchds}

.. automodsumm:: {modname}
    :functions-only:
    {clsfuncoptions}
"""

automod_templ_vars = """
Variables
{otherhds}

.. automodsumm:: {modname}
    :variables-only:
    {clsfuncoptions}
"""

automod_templ_inh = """
Class Inheritance Diagram
{clsinhsechds}

.. automod-diagram:: {modname}
    :private-bases:
    :parts: 1
    {allowedpkgnms}
    {skip}
"""

_automodapirex = re.compile(r'^(?:\.\.\s+automodapi::\s*)([A-Za-z0-9_.]+)'
                            r'\s*$((?:\n\s+:[a-zA-Z_\-]+:.*$)*)',
                            flags=re.MULTILINE)
# the last group of the above regex is intended to go into finall with the below
_automodapiargsrex = re.compile(r':([a-zA-Z_\-]+):(.*)$', flags=re.MULTILINE)


def automodapi_replace(sourcestr, app, dotoctree=True, docname=None,
                       warnings=True):
    """
    Replaces `sourcestr`'s entries of ".. automodapi::" with the
    automodapi template form based on provided options.

    This is used with the sphinx event 'source-read' to replace
    `automodapi`_ entries before sphinx actually processes them, as
    automodsumm needs the code to be present to generate stub
    documentation.

    Parameters
    ----------
    sourcestr : str
        The string with sphinx source to be checked for automodapi
        replacement.
    app : `sphinx.application.Application`
        The sphinx application.
    dotoctree : bool
        If `True`, a ":toctree:" option will be added in the "..
        automodsumm::" sections of the template, pointing to the
        appropriate "generated" directory based on the Astropy convention
        (e.g. in ``docs/api``)
    docname : str
        The name of the file for this `sourcestr` (if known - if not, it
        can be `None`). If not provided and `dotoctree` is `True`, the
        generated files may end up in the wrong place.
    warnings : bool
        If `False`, all warnings that would normally be issued are
        silenced.

    Returns
    -------
    newstr :str
        The string with automodapi entries replaced with the correct
        sphinx markup.
    """

    logger = logging.getLogger(__name__)

    spl = _automodapirex.split(sourcestr)
    if len(spl) > 1:  # automodsumm is in this document

        # Use app.srcdir because api folder should be inside source folder not
        # at folder where sphinx is run.

        if dotoctree:
            toctreestr = ':toctree: '
            api_dir = os.path.join(app.srcdir, app.config.automodapi_toctreedirnm)
            if docname is None:
                doc_path = app.srcdir
            else:
                doc_path = os.path.dirname(os.path.join(app.srcdir, docname))
            toctreestr += os.path.relpath(api_dir, doc_path).replace(os.sep, '/')
        else:
            toctreestr = ''

        newstrs = [spl[0]]
        for grp in range(len(spl) // 3):
            modnm = spl[grp * 3 + 1]

            # find where this is in the document for warnings
            if docname is None:
                location = None
            else:
                location = (docname, spl[0].count('\n'))

            # initialize default options
            toskip = []
            includes = []
            inhdiag = app.config.automodapi_inheritance_diagram
            maindocstr = True
            top_head = True
            hds = '-^'
            allowedpkgnms = []
            allowothers = False
            noindex = False
            sort = False

            # look for actual options
            unknownops = []
            inherited_members = None
            for opname, args in _automodapiargsrex.findall(spl[grp * 3 + 2]):
                if opname == 'skip':
                    toskip.append(args.strip())
                elif opname == 'include':
                    includes.append(args.strip())
                elif opname == 'inheritance-diagram':
                    inhdiag = True
                elif opname == 'no-inheritance-diagram':
                    inhdiag = False
                elif opname == 'no-main-docstr':
                    maindocstr = False
                elif opname == 'headings':
                    hds = args
                elif opname == 'no-heading':
                    top_head = False
                elif opname == 'allowed-package-names':
                    allowedpkgnms.extend(arg.strip() for arg in args.split(','))
                elif opname == 'inherited-members':
                    inherited_members = True
                elif opname == 'no-inherited-members':
                    inherited_members = False
                elif opname == 'include-all-objects':
                    allowothers = True
                elif opname == 'noindex':
                    noindex = True
                elif opname == 'sort':
                    sort = True
                else:
                    unknownops.append(opname)

            # join all the allowedpkgnms
            if len(allowedpkgnms) == 0:
                allowedpkgnms = ''
                onlylocals = True
            else:
                onlylocals = allowedpkgnms
                allowedpkgnms = ':allowed-package-names: ' + ','.join(allowedpkgnms)

            # get the two heading chars
            hds = hds.strip()
            if len(hds) < 2:
                msg = 'Not enough headings (got {0}, need 2), using default -^'
                if warnings:
                    logger.warning(msg.format(len(hds)), location)
                hds = '-^'
            h1, h2 = hds[:2]

            # tell sphinx that the remaining args are invalid.
            if len(unknownops) > 0 and app is not None:
                opsstrs = ','.join(unknownops)
                msg = 'Found additional options ' + opsstrs + ' in automodapi.'
                if warnings:
                    logger.warning(msg, location)

            ispkg, hascls, hasfuncs, hasother, toskip = _mod_info(
                modnm, toskip, includes, onlylocals=onlylocals)

            # add automodule directive only if no-main-docstr isn't present
            if maindocstr:
                automodline = f'.. automodule:: {modnm}'
            else:
                automodline = ''
            if top_head:
                newstrs.append(automod_templ_modheader.format(
                        modname=modnm,
                        modhds=h1 * len(modnm),
                        pkgormod='Package' if ispkg else 'Module',
                        pkgormodhds=h1 * (8 if ispkg else 7),
                        automoduleline=automodline))  # noqa
            else:
                newstrs.append(automod_templ_modheader.format(
                    modname='',
                    modhds='',
                    pkgormod='',
                    pkgormodhds='',
                    automoduleline=automodline))

            # construct the options for the class/function sections
            # start out indented at 4 spaces, but need to keep the indentation.
            clsfuncoptions = []
            if toctreestr:
                clsfuncoptions.append(toctreestr)
            if noindex:
                clsfuncoptions.append(':noindex:')
            if sort:
                clsfuncoptions.append(':sort:')
            if toskip:
                clsfuncoptions.append(':skip: ' + ','.join(toskip))
            if allowedpkgnms:
                clsfuncoptions.append(allowedpkgnms)
            if hascls:  # This makes no sense unless there are classes.
                if inherited_members is True:
                    clsfuncoptions.append(':inherited-members:')
                if inherited_members is False:
                    clsfuncoptions.append(':no-inherited-members:')
            clsfuncoptionstr = '\n    '.join(clsfuncoptions)

            if hasfuncs:
                newstrs.append(automod_templ_funcs.format(
                    modname=modnm,
                    funchds=h2 * 9,
                    clsfuncoptions=clsfuncoptionstr))

            if hascls:
                newstrs.append(automod_templ_classes.format(
                    modname=modnm,
                    clshds=h2 * 7,
                    clsfuncoptions=clsfuncoptionstr))

            if allowothers and hasother:
                newstrs.append(automod_templ_vars.format(
                    modname=modnm,
                    otherhds=h2 * 9,
                    clsfuncoptions=clsfuncoptionstr))

            if inhdiag and hascls:
                # add inheritance diagram if any classes are in the module
                if toskip:
                    clsskip = ':skip: ' + ','.join(toskip)
                else:
                    clsskip = ''
                diagram_entry = automod_templ_inh.format(
                    modname=modnm,
                    clsinhsechds=h2 * 25,
                    allowedpkgnms=allowedpkgnms,
                    skip=clsskip)
                diagram_entry = diagram_entry.replace('    \n', '')
                newstrs.append(diagram_entry)

            newstrs.append(spl[grp * 3 + 3])

        newsourcestr = ''.join(newstrs)

        if app.config.automodapi_writereprocessed:
            # sometimes they are unicode, sometimes not, depending on how
            # sphinx has processed things
            if isinstance(newsourcestr, str):
                ustr = newsourcestr
            else:
                ustr = newsourcestr.decode(app.config.source_encoding)

            if docname is None:
                with open(os.path.join(app.srcdir, 'unknown.automodapi'),
                          'a', encoding='utf8') as f:
                    f.write('\n**NEW DOC**\n\n')
                    f.write(ustr)
            else:
                env = app.builder.env
                # Determine the filename associated with this doc (specifically
                # the extension)
                filename = docname + os.path.splitext(env.doc2path(docname))[1]
                filename += '.automodapi'

                with open(os.path.join(app.srcdir, filename), 'w',
                          encoding='utf8') as f:
                    f.write(ustr)

        return newsourcestr
    else:
        return sourcestr


def _mod_info(modname, toskip=[], include=[], onlylocals=True):
    """
    Determines if a module is a module or a package and whether or not
    it has classes or functions.
    """

    hascls = hasfunc = hasother = False

    skips = toskip.copy()
    for localnm, fqnm, obj in zip(*find_mod_objs(modname, onlylocals=onlylocals)):
        if include and localnm not in include and localnm not in skips:
            skips.append(localnm)

        elif localnm not in toskip:
            hascls = hascls or inspect.isclass(obj)
            hasfunc = hasfunc or inspect.isroutine(obj)
            hasother = hasother or (not inspect.isclass(obj) and
                                    not inspect.isroutine(obj))
            if hascls and hasfunc and hasother:
                break

    # find_mod_objs has already imported modname
    # TODO: There is probably a cleaner way to do this, though this is pretty
    # reliable for all Python versions for most cases that we care about.
    pkg = sys.modules[modname]
    ispkg = (hasattr(pkg, '__file__') and isinstance(pkg.__file__, str) and
             os.path.split(pkg.__file__)[1].startswith('__init__.py'))

    return ispkg, hascls, hasfunc, hasother, skips


def process_automodapi(app, docname, source):
    source[0] = automodapi_replace(source[0], app, True, docname)


def setup(app):

    app.setup_extension('sphinx.ext.autosummary')

    # Note: we use __name__ here instead of just writing the module name in
    #       case this extension is bundled into another package
    from . import automodsumm
    app.setup_extension(automodsumm.__name__)

    app.connect('source-read', process_automodapi)

    app.add_config_value('automodapi_inheritance_diagram', True, True)
    app.add_config_value('automodapi_toctreedirnm', 'api', True)
    app.add_config_value('automodapi_writereprocessed', False, True)

    return {'parallel_read_safe': True,
            'parallel_write_safe': True}
