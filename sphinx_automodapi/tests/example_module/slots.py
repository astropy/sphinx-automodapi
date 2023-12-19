"""Test classes containing slots"""
from __future__ import annotations

__all__ = ['SlotDict', 'DerivedParam', 'DerivedSlotParam',]


class SlotDict(object):
    """
    A class that uses __slots__ and __dict__ for its attribute namespace.
    """
    __slots__ = ('param', '__dict__',)

    def __init__(self, param: str, other_param: str):
        """
        Initializes a SlotDict object.

        Parameters
        ----------
        my_param : str
            My parameter
        """
        self.param = param
        self.other_param = other_param

    def my_method(self):
        """
        Prints the class's parameters.
        """
        print(f"param: {self.param}")
        print(f"other_param: {self.other_param}")


class DerivedParam(SlotDict):
    """
    Extends SlotDict by adding an extra parameter
    """
    def __init__(self, param: str, other_param: str, extra_param: str):
        """
        Initializes a DerivedParam object.

        Parameters
        ----------
        param : str
            A parameter
        other_param : str
            Another parameter
        extra_param : str
            An extra parameter
        """
        super(DerivedParam, self).__init__(param, other_param)
        self.extra_param = extra_param

    def derived_from_slot_class_method(self):
        """
        Prints the DerivedParam parameters.
        """
        print(f"param: {self.param}")
        print(f"other_param: {self.other_param}")
        print(f"dict_param: {self.extra_param}")


class DerivedSlotParam(SlotDict):
    """
    Extends SlotDict by adding a slot parameter
    """

    __slots__ = ('extra_param',)

    def __init__(self, param: str, other_param: str, extra_param: str):
        """
        Initializes a DerivedParam object.

        Parameters
        ----------
        param : str
            A parameter
        other_param : str
            Another parameter
        extra_param : str
            An extra parameter
        """
        super(DerivedSlotParam, self).__init__(param, other_param)
        self.extra_param = extra_param

    def derived_from_slot_class_method(self):
        """
        Prints the DerivedParam parameters.
        """
        print(f"param: {self.param}")
        print(f"other_param: {self.other_param}")
        print(f"extra_param: {self.extra_param}")
