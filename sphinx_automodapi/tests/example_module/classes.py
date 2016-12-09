__all__ = ['Spam']


class BaseSpam(object):
    """
    Base class for Spam
    """

    def eat(self, time):
        """
        Eat some spam in the required time.
        """
        pass

    def buy(self, price):
        """
        Buy some MOAR spam.
        """
        pass


class Spam(BaseSpam):
    """
    The main spam
    """
    pass
