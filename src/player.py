from random import choice
from abc import ABCMeta, abstractmethod
from typing import List, Optional, TYPE_CHECKING

from const import NAME_LIST
if TYPE_CHECKING:
    from .card import Card
    from .deck import Deck
    from .game import Game


class Player(metaclass=ABCMeta):
    def __init__(self):
        self._name: Optional[str] = None
        self._point: int = 0
        self._has_used: bool = False
        self.hand: List['Card'] = []
        self._return_exchange_left: int = 0
        self._exchange_player: Optional['Player'] = None

    @property
    def name(self):
        return self._name

    @abstractmethod
    def name_myself(self):
        return NotImplemented

    @property
    def point(self):
        return self._point

    def add_point(self):
        self._point += 1

    def draw_card(self, deck: 'Deck'):
        card = deck.cards.pop()
        card.set_owner(self)
        # print(card, len(deck.cards))
        self.hand.append(card)
        # print(self.hand)

    def show_card_in_hand(self):
        print('These are the cards in your hand:')
        print('\n'.join(f'{i} - {card}' for i, card in enumerate(self.hand, 1)))

    @abstractmethod
    def start_this_turn(self, game: 'Game'):
        return NotImplemented

    def exchange_hand_return_handle(self):
        if self._return_exchange_left > 0:
            self._return_exchange_left -= 1
            if self._return_exchange_left == 0:
                for card in self.hand:
                    card.set_owner(self._exchange_player)
                for card in self._exchange_player.hand:
                    card.set_owner(self)
                self.hand, self._exchange_player.hand = self._exchange_player.hand, self.hand
                print('Return exchange cards on hand')


    def exchange_hand(self, player: 'Player'):
        #exchange
        for card in self.hand:
            card.set_owner(player)
        for card in player.hand:
            card.set_owner(self)
        self.hand, player.hand = player.hand, self.hand
        self._return_exchange_left = 3
        self._exchange_player = player
        print(f'Exchange hand to {player} succeed')

    @abstractmethod
    def show(self, game: 'Game'):
        return NotImplemented


class AIPlayer(Player):
    def name_myself(self):
        self._name = choice(NAME_LIST)

    def start_this_turn(self, game: 'Game'):
        self.show(game)

    def show(self, game: 'Game'):
        card = choice(self.hand)
        self.hand.remove(card)
        game.receive_card(card)


class HumanPlayer(Player):
    def name_myself(self):
        name = input('Please input your name: ')
        self._name = name

    def start_this_turn(self, game: 'Game'):
        if not self._has_used:
            want_to_exchange = input(f'{self._name}, You have a change to exchange cards on hand, want to use it?[y/n]')
            if want_to_exchange == 'y':
                print('Players you can select to exchange: ')
                print('\n'.join(f'P{i} - {player.name}' for i, player in enumerate(game.players, 1) if player != self))
                #TODO: need to validate later
                player_id = input('Please choose the player id above:')
                choosed_player = game.players[int(player_id)-1]
                self.exchange_hand(choosed_player)
                self._has_used = True
        else:
            self.exchange_hand_return_handle()

        self.show(game)

    def show(self, game: 'Game'):
        self.show_card_in_hand()
        input_success = False
        while not input_success:
            card_idx = input('Please select a card from above: ')
            try:
                card_idx = int(card_idx)
                if 1 <= card_idx <= len(self.hand):
                    input_success = True
            except Exception:
                print('Human player number should be an integer')
        card = self.hand.pop(card_idx-1)
        game.receive_card(card)
