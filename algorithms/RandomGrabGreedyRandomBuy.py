import random
from algorithms.PlayerAlgorithm import PlayerAlgorithm
import numpy as np
from gameFiles.GameState import GameState


# Randomly draw tokens, but when it's an option, randomly buy a card
class RandomGrabGreedyRandomBuy(PlayerAlgorithm):
    def __init__(self, player_number, verbose=False, generator=None):
        super().__init__(player_number, verbose)
        if generator is None:
            generator = np.random.RandomState()
        self.generator = generator

    def calculate_move(self, game_state: GameState):
        legal_moves = game_state.get_current_player_valid_moves()
        # must account for "buy_available" AND "buy_reserved" moves
        legal_buy_moves = list(filter(lambda x: "buy" in x[0], legal_moves))
        if len(legal_buy_moves) > 0:
            move = legal_buy_moves[random.randrange(len(legal_buy_moves))]
        else:
            move = legal_moves[random.randrange(len(legal_moves))]

        if self.verbose:
            print(f"Player {self.player_number} move: {move}")

        return move
