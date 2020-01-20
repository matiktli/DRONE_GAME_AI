from Map import GameMap
from utils.config_utils import Config
from Engine import GameEngine, GameFrame, GameAction, Action
from typing import List
from Bot import Bot, RandomBot

"""
Player representation object
"""


class Player():

    def __init__(self, player_id, bot: Bot, drone_no, allowed_actions_ids=None):
        self.player_id = player_id
        self.bot = bot
        self.allowed_actions_ids = allowed_actions_ids
        self.drone_no = drone_no


class DroneIdGenerator():

    def __init__(self, players_no):
        self.ids_generator = [0 for num in range(0, players_no)]
        pass

    def get_new_drone_id(self, player_id) -> str:
        curr_id = self.ids_generator[int(player_id)]
        new_id = curr_id + 1
        self.ids_generator[int(player_id)] = new_id
        return str(player_id) + '_' + str(new_id)


"""
Player maintainer service
"""


class PlayerService():

    def __init__(self, players_config, env_actions):
        self.players = []
        self.env_actions = env_actions
        self.drone_id_generator = DroneIdGenerator(len(players_config))
        for p in players_config:
            self.__add_player(int(p['id']), str(
                p['type']), int(p['drone_no']), p['path'], p['allowed_actions'])

    def __add_player(self, player_id: int, p_type: str, drone_no: int, path: str = None, allowed_actions_config=None):
        bot = None
        actions = []
        for act_id in allowed_actions_config:
            for act in Action:
                if str(act.value['id']) == str(act_id):
                    actions.append(act)
        if p_type == 'RAND':
            bot = RandomBot(player_id, actions)
        elif p_type == 'BOT':
            bot = None
        p = Player(player_id, bot, drone_no)
        print(
            f'Added player with id: {player_id} and type: {p_type} [{path}] and actions: {list(map(lambda a: a.value["id"], actions))}')
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
        self.engine.increment_turn_counter()
        self.map.reset_drones_attack()
        return self.engine.get_state()['is_on']
