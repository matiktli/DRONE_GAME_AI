from Map import GameMap
from utils.config_utils import Config
from Engine import GameEngine, GameFrame


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
        self.engine = GameEngine(config.game_max_turns)

    # Get current frame for environemnt
    def get_frame(self) -> GameFrame:
        return self.engine.get_current_game_frame()

    # Pass decided actions for each of drones
    def pass_actions(self, actions):
        for action in actions:
            self.engine.add_action_to_query(action)

    # End turn and perform all after move calculations
    def end_turn(self):
        self.engine.perform_actions()
        return False
