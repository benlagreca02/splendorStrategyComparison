import numpy as np

from gameFiles.data import colours


class Player(object):
    def __init__(self):
        self.cards_in_hand = []
        self.cards_played = []
        self.nobles = []

        self._gold = 0
        self._white = 0
        self._blue = 0
        self._green = 0
        self._red = 0
        self._black = 0

    def copy(self):
        copy = Player()
        for colour in colours + ['gold']:
            copy.set_gems(colour, self.num_gems(colour))
        copy.nobles = self.nobles[:]
        copy.cards_in_hand = self.cards_in_hand[:]
        copy.cards_played = self.cards_played[:]
        return copy

    def num_gems(self, colour):
        return getattr(self, '_' + colour)

    def set_gems(self, colour, number):
        setattr(self, '_' + colour, number)

    @property
    def total_num_gems(self):
        return (self._gold + self._white + self._blue + self._green +
                self._red + self._black)

    @property
    def gems(self):
        return {'white': self._white,
                'blue': self._blue,
                'green': self._green,
                'red': self._red,
                'black': self._black,
                'gold': self._gold}

    # def gems_list(self):
    #     return (['white' for _ in range(self.white)] +
    #             ['blue' for _ in range(self.blue)] +
    #             ['green' for _ in range(self.green)] +
    #             ['red' for _ in range(self.red)] +
    #             ['black' for _ in range(self.black)] +
    #             ['gold' for _ in range(self.gold)])

    def add_gems(self, **kwargs):
        for colour, change in kwargs.items():
            assert colour in colours or colour == 'gold'
            self.set_gems(colour, self.num_gems(colour) + change)

    @property
    def num_reserved(self):
        return len(self.cards_in_hand)

    @property
    def score(self):
        score = 0
        num_zero = 0
        for card in self.cards_played:
            points = card.points
            if points > 0:
                score += card.points
            else:
                num_zero += 1

        # score -= num_zero# // 3

        for noble in self.nobles:
            score += noble.points

        return score

    def num_cards_of_colour(self, colour):
        number = 0
        for card in self.cards_played:
            if card.colour == colour:
                number += 1
        return number

    def can_afford(self, card):
        missing_colours = [max(card.num_required(colour) -
                               self.num_gems(colour) -
                               self.num_cards_of_colour(colour), 0)
                           for colour in colours]

        if sum(missing_colours) > self.num_gems('gold'):
            return False, sum(missing_colours) - self.num_gems('gold')

        cost = {colour: max(min(self.num_gems(colour),
                                card.num_required(colour) -
                                self.num_cards_of_colour(colour)),
                            0) for colour in colours}
        cost['gold'] = sum(missing_colours)

        # TODO: Allow gold to be used instead of coloured gems, if available
        # however, why would you ever want to use gold if you don't have to....

        return True, cost

    def verify_state(self):
        assert 0 <= self.total_num_gems <= 10
        assert len(self.cards_in_hand) <= 3
        assert len(set(self.nobles)) == len(self.nobles)

        for colour in colours + ['gold']:
            assert self.num_gems(colour) >= 0

    @property
    def num_cards_each_tier(self):
        results = np.zeros(3)
        for card in self.cards_played:
            results[card.tier - 1] += 1
        return results
