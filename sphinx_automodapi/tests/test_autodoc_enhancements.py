from textwrap import dedent

import pytest

from ..autodoc_enhancements import type_object_attrgetter


# Define test classes outside the class; otherwise there is flakiness with the
# details of how exec works on different Python versions
class Meta(type):
    @property
    def foo(cls):
        return 'foo'


class MyClass(metaclass=Meta):
    @property
    def foo(self):
        """Docstring for MyClass.foo property."""
        return 'myfoo'


def test_type_attrgetter():
    """
    This test essentially reproduces the docstring for
    `type_object_attrgetter`.

    Sphinx itself tests the custom attrgetter feature; see:
    https://bitbucket.org/birkenfeld/sphinx/src/40bd03003ac6fe274ccf3c80d7727509e00a69ea/tests/test_autodoc.py?at=default#cl-502
    so rather than a full end-to-end functional test it's simple enough to just
    test that this function does what it needs to do.
    """

    assert getattr(MyClass, 'foo') == 'foo'
    obj = type_object_attrgetter(MyClass, 'foo')
    assert isinstance(obj, property)
    assert obj.__doc__ == 'Docstring for MyClass.foo property.'

    with pytest.raises(AttributeError):
        type_object_attrgetter(MyClass, 'susy')

    assert type_object_attrgetter(MyClass, 'susy', 'default') == 'default'
    assert type_object_attrgetter(MyClass, '__dict__') == MyClass.__dict__


def test_type_attrgetter_for_dataclass():
    """
    This tests the attribute getter for non-default dataclass fields
    """
    import dataclasses

    @dataclasses.dataclass
    class MyDataclass:
        foo: int
        bar: str = "bar value"

    with pytest.raises(AttributeError):
        getattr(MyDataclass, 'foo')
    assert type_object_attrgetter(MyDataclass, 'foo') == dataclasses.MISSING
    assert getattr(MyDataclass, 'bar') == 'bar value'
