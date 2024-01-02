import numpy as np

from gameFiles.GameState import GameState

from gameFiles.Card import Card
from gameFiles.Noble import Noble
from gameFiles.Player import Player

from RandomAlgo import TrueRandomAlgo

if __name__ == '__main__':

    # make generator the same every time for testing purposes
    manager = GameState(2, init_game=True, generator=np.random.RandomState(69))

    # should always be a list of PlayerAlgorithm objects
    players = [TrueRandomAlgo(1, verbose=True), TrueRandomAlgo(2, verbose=True)]

    manager.print_state()
    i = 1
    while len([k for k in manager.get_scores() if k >= 15]) < 1:
        print(f"ROUND {i}")
        for player in players:
            manager.make_move(player.calculate_move(manager))
        i += 1
    print(f"Game over, scores: {manager.get_scores()}")
    manager.print_state()