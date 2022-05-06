from collections.abc import Sequence

__all__ = ['SequenceSubclass']


class SequenceSubclass(Sequence):
    """
    Inherits from an ABC.
    """

    def __init__(self):
        self._items = []

    def __len__(self):
        """
        Must be defined for the collections.abc.Sequence base class.
        """
        return len(self._items)

    def __getitem__(self, key):
        """
        Must be defined for the collections.abc.Sequence base class.
        """
        return self._items[key]

    def my_method(self, parameter):
        """
        An example method.
        """
        pass

    @property
    def my_property(self):
        """
        An example property.
        """
        return 42
