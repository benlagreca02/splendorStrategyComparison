from gameFiles.StateVector import StateVector
from abc import ABC, abstractmethod


# abstract base class
class PlayerAlgorithm(ABC):

    def __init__(self, player_number, verbose=False):
        self.player_number = player_number
        self.verbose = verbose

    # every algorithm will implement this differently
    @abstractmethod
    def calculate_move(self, state_vec: StateVector):
        pass
