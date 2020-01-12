from Map import GameMap
from utils.config_utils import Config
from Engine import GameEngine, GameFrame, GameAction, Action
from typing import List
from Bot import Bot, RandomBot


class Player():

    def __init__(self, player_id, bot: Bot):
        self.player_id = player_id
        self.bot = bot
        self.drones = []


"""
Player maintainer service
"""


class PlayerService():

    def __init__(self, players_config, env_actions):
        self.players = []
        self.env_actions = env_actions
        for p in players_config:
            self.__add_player(int(p['id']), str(p['type']), p['path'])

    def __add_player(self, player_id: int, type: str, path: str = None):
        bot = None
        if type == 'RAND':
            bot = RandomBot(player_id, self.env_actions)
        p = Player(player_id, bot)
        self.players.append(p)


"""
Environment object used by player(bot) to perform operations on the game
"""


class Environment():

    def __init__(self, config: Config):
        self.map = GameMap(config.map_size)
        self.player_svc = PlayerService(
            config.players_config, len(list(Action)))
        self.engine = GameEngine(self.map, self.player_svc, config.max_turns)
        self.players = []

    # Initialization function - load players to system
    def _init_load_players(self) -> bool:
        pass

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
