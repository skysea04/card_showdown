from typing import Optional

from const import CARD_RANKS, CARD_SUITS

from .player import Player

class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit
        self.point = 4 * CARD_RANKS[rank] + CARD_SUITS[suit]
        self._owner: Optional[Player] = None

    def __str__(self):
        return f'【{self._rank}】 {self._suit}'

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, rank: str):
        if rank not in CARD_RANKS:
            raise ValueError('Invalid Card Rank')
        self._rank = rank

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, suit: str):
        if suit not in CARD_SUITS:
            raise ValueError('Invalid Card Suit')
        self._suit = suit

    @property
    def owner(self):
        return self._owner

    def set_owner(self, player: Player):
        if not isinstance(player, Player):
            raise TypeError('Owner should be a Player')
        self._owner = player
