__all__ = ['Fruit', 'Banana', 'Orange']


class Fruit(object):
    """
    An fruit
    """
    def eat(self, time):
        """
        Eat apple.
        """
        pass

    def buy(self, price):
        """
        Buy apple.
        """
        pass

    @property
    def weight(self):
        """
        The weight of the apple.
        """
        return 0

    @property
    def _age(self):
        """
        The age of the fruit.
        """
        return 0

    def __len__(self):
        """
        The length the fruit.
        """
        return 0

    def _out_of_date(self, date):
        """
        Is it out of date?
        """
        pass


class Banana(Fruit):
    """
    A banana
    """
    def eat(self, time):
        """
        Eat banana.
        """
        pass

    def _energy(self, units='kcal'):
        """
        The energy in the banana.
        """
        pass

    def __add__(self, other):
        """
        How to add the banana to something.
        """
        pass


class Orange(Fruit):
    """
    An orange
    """
    def eat(self, time):
        """
        Eat orange.
        """
        pass

    def _energy(self, units='kcal'):
        """
        The energy in the orange.
        """
        pass

    def __add__(self, other):
        """
        How to add the orange to something.
        """
        pass
