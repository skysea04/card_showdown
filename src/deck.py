from typing import List
import random

from const import CARD_RANKS, CARD_SUITS
from .card import Card

class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        for rank in CARD_RANKS:
            for suit in CARD_SUITS:
                self.cards.append(Card(rank, suit))

    def __str__(self):
        cards = '\n'.join(f'{card}' for card in self.cards)
        return 'Show Deck:\n'+ cards

    def shuffle(self):
        random.shuffle(self.cards)
