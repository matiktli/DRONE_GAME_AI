from Map import GameMap
from utils.config_utils import Config
from Engine import GameEngine, GameFrame, GameAction
from typing import List

"""
Environment object used by player(bot) to perform operations on the game
"""


class Environment():

    def __init__(self, config: Config):
        self.map = GameMap(config.game_initial_size)
        self.engine = GameEngine(config.game_max_turns)

    # Get current frame for environemnt
    def get_frame(self) -> GameFrame:
        return self.engine.get_current_game_frame()

    # Pass decided actions for each of drones
    def pass_actions(self, actions: List[GameAction]):
        for action in actions:
            self.engine.add_action_to_query(action)

    # End turn and perform all after move callculations
    def end_turn(self):
        # Perform bot/s actions
        self.engine.perform_actions_in_query()
        # Add and perform environment actions/outcomes
        self.engine.add_environment_actions_to_query()
        self.engine.perform_actions_in_query()
        return self.engine.get_state()['is_on']
