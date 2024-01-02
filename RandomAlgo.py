import random

from PlayerAlgorithm import PlayerAlgorithm
import numpy as np
from gameFiles.GameState import GameState


class TrueRandomAlgo(PlayerAlgorithm):
    def __init__(self, player_number, verbose=False, generator=None):
        super().__init__(player_number, verbose)
        if generator is None:
            generator = np.random.RandomState()
        self.generator = generator

    def calculate_move(self, game_state: GameState):
        legal_moves = game_state.get_current_player_valid_moves()
        move = legal_moves[random.randrange(len(legal_moves))]
        if self.verbose:
            print(f"Player {self.player_number} move: {move}")
        return move
