"""
Miscellaneous enhancements to help autodoc along.
"""
import dataclasses

from sphinx.ext.autodoc import AttributeDocumenter

__all__ = []

class_types = (type,)
MethodDescriptorType = type(type.__subclasses__)


# See
# https://github.com/astropy/astropy-helpers/issues/116#issuecomment-71254836
# for further background on this.
def type_object_attrgetter(obj, attr, *defargs):
    """
    This implements an improved attrgetter for type objects (i.e. classes)
    that can handle class attributes that are implemented as properties on
    a metaclass.

    Normally `getattr` on a class with a `property` (say, "foo"), would return
    the `property` object itself.  However, if the class has a metaclass which
    *also* defines a `property` named "foo", ``getattr(cls, 'foo')`` will find
    the "foo" property on the metaclass and resolve it.  For the purposes of
    autodoc we just want to document the "foo" property defined on the class,
    not on the metaclass.

    For example::

        >>> class Meta(type):
        ...     @property
        ...     def foo(cls):
        ...         return 'foo'
        ...
        >>> class MyClass(metaclass=Meta):
        ...     @property
        ...     def foo(self):
        ...         \"\"\"Docstring for MyClass.foo property.\"\"\"
        ...         return 'myfoo'
        ...
        >>> getattr(MyClass, 'foo')
        'foo'
        >>> type_object_attrgetter(MyClass, 'foo')
        <property at 0x...>
        >>> type_object_attrgetter(MyClass, 'foo').__doc__
        'Docstring for MyClass.foo property.'

    The last line of the example shows the desired behavior for the purposes
    of autodoc.
    """

    for base in obj.__mro__:
        if attr in base.__dict__:
            if isinstance(base.__dict__[attr], property):
                # Note, this should only be used for properties--for any other
                # type of descriptor (classmethod, for example) this can mess
                # up existing expectations of what getattr(cls, ...) returns
                return base.__dict__[attr]
            break

    try:
        return getattr(obj, attr, *defargs)
    except AttributeError:
        # for dataclasses, get the attribute from the __dataclass_fields__
        if dataclasses.is_dataclass(obj) and attr in obj.__dataclass_fields__:
            return obj.__dataclass_fields__[attr].default
        else:
            raise


def setup(app):
    # Must have the autodoc extension set up first so we can override it
    app.setup_extension('sphinx.ext.autodoc')

    app.add_autodoc_attrgetter(type, type_object_attrgetter)

    suppress_warnings_orig = app.config.suppress_warnings[:]
    if 'app.add_directive' not in app.config.suppress_warnings:
        app.config.suppress_warnings.append('app.add_directive')
    try:
        app.add_autodocumenter(AttributeDocumenter)
    finally:
        app.config.suppress_warnings = suppress_warnings_orig

    return {'parallel_read_safe': True,
            'parallel_write_safe': True}
