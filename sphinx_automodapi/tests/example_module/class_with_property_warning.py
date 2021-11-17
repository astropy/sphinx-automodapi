import warnings

__all__ = ['Camelot']


class customproperty:
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)



class Camelot(object):
    """
    A class where a property emits a warning
    """

    @customproperty
    def silly(cls):
        warnings.warn("It is VERY silly", UserWarning)

    @property
    def place(self):
        """
        Indeed.
        """
        pass
