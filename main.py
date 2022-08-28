from src.game import Game

game = Game()
game.generate_players()
game.deck.shuffle()
game.let_players_draw_card()
game.run_the_game()
