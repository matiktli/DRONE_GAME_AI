import numpy as np
from Map import Cell, GameMap

"""
Game state representation
"""


class GameFrame():

    def __init__(self, map: GameMap):
        self.map = map


class GameMove():

    def __init__(self):
        pass


class GameEngine():

    def __init__(self, max_turns=100):
        self.max_turns = max_turns
        self.actions_query = []

    def add_action_to_query(self, action):
        pass

    def perform_actions(self):
        pass

    def get_current_game_frame(self):
        pass
