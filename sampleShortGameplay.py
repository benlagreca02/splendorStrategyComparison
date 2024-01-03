import numpy as np

from gameFiles.GameState import GameState

from gameFiles.Card import Card
from gameFiles.Noble import Noble
from gameFiles.Player import Player

from TrueRandomAlgo import TrueRandomAlgo


def play_game(man, players, verb):
    num_rounds = 0
    while len([k for k in man.get_scores() if k >= 15]) < 1:

        if verb:
            print(f"ROUND: {num_rounds}")
            man.print_state()

        for player in players:
            man.make_move(player.calculate_move(man))
            if verb:
                man.print_state()
        num_rounds += 1

    winner_index = np.argmax(man.get_scores())
    return num_rounds, winner_index


if __name__ == '__main__':

    num_games = 500
    print_freq = 25
    verb = False
    # should always be a list of PlayerAlgorithm objects
    algos = [TrueRandomAlgo(1, verbose=verb), TrueRandomAlgo(2, verbose=verb), TrueRandomAlgo(3, verbose=verb)]

    win_count = [0 for _ in range(len(algos))]
    rounds_to_win = [0 for _ in range(num_games)]

    print(f"Simulating {num_games} games...")
    for i in range(num_games):
        # while someone hasn't won
        manager = GameState(len(algos), init_game=True)
        rounds_to_win[i], winner_number = play_game(manager, algos, verb)
        win_count[winner_number] += 1
        if i % print_freq ==0:
            print(i)
    print(f"Avg rounds to win: {np.average(rounds_to_win)}, {win_count}")
