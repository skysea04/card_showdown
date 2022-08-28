from typing import List

from const import PLAYER_NUM

from .card import Card
from .deck import Deck
from .player import Player, HumanPlayer, AIPlayer

class Game:
    def __init__(self):
        self._turn = 0
        self.deck = Deck()
        self._card_in_this_turn: List[Card] = []
        self._players: List[Player] = []

    @property
    def players(self):
        return self._players

    def generate_players(self):
        human_num_success = False
        human_player_num = 0
        while not human_num_success:
            human_player_num = input('Please input the human player number(1~4): ')
            try:
                human_player_num = int(human_player_num)
                if 1 <= human_player_num <= PLAYER_NUM:
                    human_num_success = True
            except Exception:
                print('Human player number should be an integer')

        for _ in range(PLAYER_NUM):
            if human_player_num > 0:
                player = HumanPlayer()
                human_player_num -= 1
            else:
                player = AIPlayer()
            player.name_myself()
            self._players.append(player)

    def let_players_draw_card(self):
        print('Players start to draw cards ...')
        for _ in range(13):
            for player in self._players:
                player.draw_card(self.deck)

        print('Players\' draws finished')

    def take_a_turn(self):
        for player in self._players:
            player.start_this_turn(self)

        max_point = 0
        max_card_idx = 0
        for i, card in enumerate(self._card_in_this_turn):
            if card.point > max_point:
                max_point = card.point
                max_card_idx = i

        print('\n'.join(
            f'P{i} - {card.owner.name} {card}' for i, card in enumerate(self._card_in_this_turn, 1)
        ))
        player = self._card_in_this_turn[max_card_idx].owner
        player.add_point()
        print(f'{player.name} win this turn, point: {player.point}')
        self._card_in_this_turn = []

    def receive_card(self, card: Card):
        self._card_in_this_turn.append(card)

    def show_winner(self):
        max_point = 0
        max_point_idx = 0
        for i, player in enumerate(self._players):
            if player.point > max_point:
                max_point = player.point
                max_point_idx = i
        print(f'P{max_point_idx} - {self._players[max_point_idx].name} is winner!!')

    def run_the_game(self):
        while self._turn < 13:
            self.take_a_turn()
            self._turn += 1
            print()

        self.show_winner()