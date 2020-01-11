from Map import GameMap
from utils.config_utils import Config


"""
Game state representation
"""


class Frame():

    def __init__(self):
        pass


"""
Game action requests for player(bot)
"""


class Actions():

    def __init__(self):
        pass


"""
Environment object used by player(bot) to perform operations on the game
"""


class Environment():

    def __init__(self, config: Config):
        self.config = config
        self.map = GameMap(config.game_initial_size)

    # Get current frame for environemnt
    def get_frame(self) -> Frame:
        pass

    # Pass decided actions for each of drones
    def pass_actions(self, actions):
        pass

    # End turn and perform all after move calculations
    def end_turn(self):
        return True

    def __init_players(self, config: Config):
        pass
