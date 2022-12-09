__all__ = ['NonAscii']


class NonAscii(object):
    def get_äöü(self):
        """
        Return a string with common umlauts like äöüß
        """
        return 'äöü'

    def get_ß(self):
        """
        Return a string with the eszett symbol
        """
        return 'ß'
