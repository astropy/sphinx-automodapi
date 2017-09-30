# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
The classes in the astropy docs are documented by their API location,
which is not necessarily where they are defined in the source.  This
causes a problem when certain automated features of the doc build,
such as the inheritance diagrams or the `Bases` list of a class
reference a class by its canonical location rather than its "user"
location.

In the `autodoc-process-docstring` event, a mapping from the actual
name to the API name is maintained.  Later, in the `missing-reference`
event, unresolved references are looked up in this dictionary and
corrected if possible.
"""

import os
import glob
import uuid
import tempfile
from docutils.nodes import literal, reference

# NOTE: This extension originally used a dictionary stored in app.env to keep
# the mapping - however, when running the builds in parallel, this dictionary
# would get populated separately on each reader worker, and there was no way
# to combine these into a single dictionary for use in missing_reference_handler
# which is run in serial mode at the end of the build. The solution implemented
# below is that each worker write a file with its own dictionary using key:value
# syntax. The prefix for the files is a temporary file MAPPING_PREFIX which is
# shared by all workers. Since the parallel builds use multiprocessing rather
# than multi-threading, we then use the process ID as a suffix to the temporary
# file name to avoid any clashes. In missing_reference_handler we then look for
# all files with the MAPPING_PREFIX and the right extension. Just to make sure
# we avoid any issues on systems that may return a filename which could be
# similar between subsequent builds, we generate a UUID to add to the prefix.

MAPPING_PREFIX = tempfile.mktemp(suffix=str(uuid.uuid4()))


def process_docstring(app, what, name, obj, options, lines):
    if isinstance(obj, type):
        with open("{0}.{1}.ref".format(MAPPING_PREFIX, os.getpid()), 'a') as f:
            f.write("{0}:{1}\n".format(obj.__module__ + '.' + obj.__name__, name))


# NOTE: to avoid re-reading all the files every time there is a missing
# reference, we store this as a global dictionary. At the moment
# missing_reference_handler is run in serial mode but if it is ever run in
# parallel, this should still work since each process will have its own global
# mapping object.

mapping = None


def missing_reference_handler(app, env, node, contnode):

    # Note that this is only global within a process, not across processes,
    # which is ok (see NOTE above).
    global mapping

    if mapping is None:
        # Load in the dictionaries that were stored to files
        mapping = {}
        for filename in glob.glob("{0}.*.ref".format(MAPPING_PREFIX)):
            for line in open(filename):
                key, value = line.strip().split(':')
                mapping[key] = value

    reftype = node['reftype']
    reftarget = node['reftarget']
    if reftype in ('obj', 'class', 'exc', 'meth'):
        reftarget = node['reftarget']
        suffix = ''
        if reftarget not in mapping:
            if '.' in reftarget:
                front, suffix = reftarget.rsplit('.', 1)
            else:
                suffix = reftarget

            if suffix.startswith('_') and not suffix.startswith('__'):
                # If this is a reference to a hidden class or method,
                # we can't link to it, but we don't want to have a
                # nitpick warning.
                return node[0].deepcopy()

            if reftype in ('obj', 'meth') and '.' in reftarget:
                if front in mapping:
                    reftarget = front
                    suffix = '.' + suffix

            if (reftype in ('class', ) and '.' in reftarget and
                    reftarget not in mapping):

                if '.' in front:
                    reftarget, _ = front.rsplit('.', 1)
                    suffix = '.' + suffix
                reftarget = reftarget + suffix
                prefix = reftarget.rsplit('.')[0]
                inventory = env.intersphinx_named_inventory
                if (reftarget not in mapping and
                        prefix in inventory):

                    if reftarget in inventory[prefix]['py:class']:
                        newtarget = inventory[prefix]['py:class'][reftarget][2]
                        if not node['refexplicit'] and \
                                '~' not in node.rawsource:
                            contnode = literal(text=reftarget)
                        newnode = reference('', '', internal=True)
                        newnode['reftitle'] = reftarget
                        newnode['refuri'] = newtarget
                        newnode.append(contnode)

                        return newnode

        if reftarget in mapping:
            newtarget = mapping[reftarget] + suffix
            if not node['refexplicit'] and '~' not in node.rawsource:
                contnode = literal(text=newtarget)
            newnode = env.domains['py'].resolve_xref(
                env, node['refdoc'], app.builder, 'class', newtarget,
                node, contnode)
            if newnode is not None:
                newnode['reftitle'] = reftarget
            return newnode


def setup(app):

    app.connect('autodoc-process-docstring', process_docstring)
    app.connect('missing-reference', missing_reference_handler)

    return {'parallel_read_safe': True,
            'parallel_write_safe': True}
