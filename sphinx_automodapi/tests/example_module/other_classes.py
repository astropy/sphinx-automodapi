__all__ = ['Foo']


class BaseFoo:
    """
    Base class for Foo
    """

    def bar(self, time):
        """
        Eat some spam in the required time.
        """
        pass


class Foo(BaseFoo):
    """
    The main foo
    """
    def hmm(self):
        pass
