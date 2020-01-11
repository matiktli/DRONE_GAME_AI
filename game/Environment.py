from Map import GameMap
from utils.config_utils import Config


class Frame():

    def __init__(self):
        pass


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
