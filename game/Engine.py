import numpy as np
from Map import Cell, GameMap
from enum import Enum
from Entity import Drone
from abc import ABC


class Action(Enum):
    MOVE_UP = {'id': 0, 'vector': (0, 1)}
    MOVE_DOWN = {'id': 1, 'vector': (0, -1)}
    MOVE_LEFT = {'id': 2, 'vector': (-1, 0)}
    MOVE_RIGHT = {'id': 3, 'vector': (1, 0)}

    STAY = {'id': 4, 'vector': (0, 0)}
    DUPLICATE = {'id': 5, 'vector': (0, 0)}


class EnvAction(Enum):
    # When two or more drones are at the same cell (from not the same player) - they fight
    ATTACK = {'id': 100}

    # When drone is surrounded by at least 3 oponent drones and is only drone in cell
    DETONATE = {'id': 101}

    # When two or more drone are at the cell (from the same player)
    # - they merge into one (there can not be enemy drones in area of `distance` from cell)
    MERGE = {'id': 102, 'distance': 1}

    # Send message to kill drone
    KILL = {'id': 103}


"""
Game state representation dto
"""


class GameFrame():

    def __init__(self, map: GameMap):
        self.player_available_actions = list(Action)
        self.map = map


"""
Game action requests to engine dto
"""


class GameAction():

    def __init__(self, player_id, drone_id, drone_position, action):
        self.player_id = player_id
        self.drone_id = drone_id
        self.drone_position = drone_position
        self.action = action

    def is_move(self):
        return self.action in [Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT]

    def is_special(self):
        return self.action in [Action.STAY, Action.DUPLICATE]

    def is_env(self):
        return self.action in [EnvAction.ATTACK, EnvAction.DETONATE, EnvAction.KILL, EnvAction.MERGE]

    # Bad implementation
    def __get_new_position(self):
        assert self.drone_position != None
        assert self.action != None
        assert self.is_move()
        return (self.drone_position[0] + self.action['vector'][0], self.drone_position[1] + self.action['vector'][1])

    def __str__(self):
        return f'Player_id: {self.player_id}, Drone_id: {self.drone_id}, Drone_pos: {self.drone_position}, Action: {self.action}'


"""
MAIN Game engine.
"""


class GameEngine():

    def __init__(self, game_map: GameMap, player_service, max_turns=100):
        self.cur_turn = 0
        self.max_turns = max_turns
        self.actions_query = []
        self.game_map = game_map
        self.env_utils = EnvActionUtils()
        self.utils = GameEngineUtils(self.env_utils)
        self.player_service = player_service
        self.__initialise_drones()
        print(
            f"""Initialised game engine with stats: 
            -Max Turns: {self.max_turns}
            -No Players: {len(self.player_service.players)}
            -No Moves: {self.player_service.env_actions} """)

    def __initialise_drones(self):
        return self.utils.initialise_drone_positions_for_players(self.game_map, self.player_service.players, self.player_service.drone_id_generator)

    # Add single drone action to query (for each drone in each player)
    def add_action_to_query(self, game_action: GameAction):
        self.actions_query.append(game_action)

    # Add all environment decission actions to query (once a turn)
    def add_environment_actions_to_query(self):
        env_actions_to_perform = []
        env_actions_to_perform.append(
            GameAction('ENV', 'ENV', (-1, -1), EnvAction.KILL)
        )
        env_actions_to_perform.append(
            GameAction('ENV', 'ENV', (-1, -1), EnvAction.ATTACK)
        )
        env_actions_to_perform.append(
            GameAction('ENV', 'ENV', (-1, -1), EnvAction.MERGE)
        )
        env_actions_to_perform.append(
            GameAction('ENV', 'ENV', (-1, -1), EnvAction.DETONATE)
        )
        for env_action in env_actions_to_perform:
            self.add_action_to_query(env_action)

    # For each action in query perform given move with including game logic (end of turn)
    def perform_actions_in_query(self, clean=True):
        for game_action in self.actions_query:
            self.game_map = self.utils.perform_action_on_env(
                game_action, self.game_map)
        if clean:
            self.actions_query.clear()

    def get_current_game_frame(self) -> GameFrame:
        return GameFrame(map=self.game_map)

    # Returns state of engine:
    # {'is_on': bool}
    def get_state(self) -> object:
        is_turn_max_limit = self.cur_turn >= self.max_turns
        is_one_player_left = len(self.game_map.get_drones()) == 1
        return {'is_on': not is_turn_max_limit and not is_one_player_left}

    def increment_turn_counter(self):
        tmp = self.cur_turn
        self.cur_turn = tmp + 1
        return self.cur_turn


"""
Utility class for game engine. 'Physics' maintainer.
"""


class GameEngineUtils():

    def __init__(self, env_utils):
        self.env_utils = env_utils
        pass

    # Calculate new position with RESPECTING game engine, end of maps are connected as default
    def __calculate_new_position(self, initial_position: tuple, action_vector: tuple, map_x_y: tuple) -> tuple:
        if action_vector[0] == 0 and action_vector[1] == 0:
            return initial_position

        new_raw_x, new_raw_y = initial_position[0] + \
            action_vector[0], initial_position[1] + action_vector[1]

        # If new position is outside right
        if new_raw_x >= map_x_y[0]:
            new_raw_x = int(new_raw_x % map_x_y[0])
        # If new position is outside left
        elif new_raw_x < 0:
            new_raw_x = int(new_raw_x + map_x_y[0])

        # If new position is outside up
        if new_raw_y >= map_x_y[1]:
            new_raw_y = int(new_raw_y % map_x_y[1])
        # If new position is outside down
        elif new_raw_y < 0:
            new_raw_y = int(new_raw_y + map_x_y[1])

        assert new_raw_x in range(0, map_x_y[0])
        assert new_raw_y in range(0, map_x_y[1])
        return (new_raw_x, new_raw_y)

    # Obtain drone from cell with verifying player id, drone position and drone id.
    def __obtain_drone_from_cell(self, player_id, drone_id, drone_position, game_map):
        cell = game_map.get_cell(drone_position)
        assert cell.is_occupied(drone_id)
        drone: Drone = next(
            (d for d in cell.drones if d.drone_id == drone_id), None)
        assert drone != None
        assert int(player_id) == int(
            drone.player_id) or str(player_id) == 'ENV'
        return drone, cell

    # Logic responsible for valid movement of drone

    def __perform_action_move(self, game_action: GameAction, game_map: GameMap) -> GameMap:
        assert game_action.is_move()
        # Valid new positions
        new_position = self.__calculate_new_position(
            game_action.drone_position, game_action.action.value['vector'], game_map.size)
        drone, cell = self.__obtain_drone_from_cell(game_action.player_id,
                                                    game_action.drone_id, game_action.drone_position, game_map)
        # Drone perform action - so losses energy
        drone.action_move()
        # Map accepts movement besides of drone state, why not
        game_map.change_drone_position(
            drone.drone_id, game_action.drone_position, new_position)
        return game_map

    # Logic responsible for valid special actions of drone
    def __perform_action_special(self, game_action: GameAction, game_map: GameMap) -> GameMap:
        assert game_action.is_special()
        pass  # ONLY TMP (!!!)
        drone, cell = self.__obtain_drone_from_cell(
            game_action.player_id, game_action.drone_id, game_action.drone_position, game_map)

        # Duplicate action
        if game_action.action == Action.DUPLICATE:
            drone.action_duplicate()
            # duplicate logic, poor one TMP
            drone_ids = list(map(lambda drone: drone.drone_id.split('_')[1], game_map.get_cell(
                drone.drone_id).get_drones()[str(drone.player_id)]))
            drone_ids = drone_ids.sort()

        # Stay action
        if game_action.action == Action.STAY:
            drone.action_stay()
        return game_map

    # Login responsible for performing env decided actions
    def __perform_env_action(self, game_action: GameAction, game_map: GameMap) -> GameMap:
        assert game_action.is_env()
        if game_action.action == EnvAction.KILL and game_action.drone_id == 'ENV':
            game_map = self.env_utils.perform_env_kill_all(game_map)
        elif game_action == EnvAction.KILL:
            game_map = self.env_utils.perform_env_kill_single(
                game_action.player_id, game_action.drone_id, game_map)

        if game_action.action == EnvAction.ATTACK and game_action.drone_id == 'ENV':
            game_map = self.env_utils.perform_env_attack_all(game_map)
        elif game_action == EnvAction.ATTACK:
            game_map = self.env_utils.perform_env_attack_single(
                game_action.player_id, game_action.drone_id, game_map)

        if game_action.action == EnvAction.MERGE and game_action.drone_id == 'ENV':
            game_map = self.env_utils.perform_env_merge_all(game_map)
        elif game_action == EnvAction.MERGE:
            game_map = self.env_utils.perform_env_merge_single(
                game_action.player_id, game_action.drone_id, game_map)

        if game_action.action == EnvAction.DETONATE and game_action.drone_id == 'ENV':
            game_map = self.env_utils.perform_env_detonate_all(game_map)
        elif game_action == EnvAction.DETONATE:
            game_map = self.env_utils.perform_env_detonate_single(
                game_action.player_id, game_action.drone_id, game_map)

        return game_map

    # Public function to interact with env (map)
    def perform_action_on_env(self, game_action: GameAction, game_map: GameMap) -> GameMap:
        print(
            f'[ENGINE: performing]: Player: {game_action.player_id} | Drone: {game_action.drone_id} | Action: {game_action.action}')
        if game_action.is_move():
            game_map = self.__perform_action_move(
                game_action, game_map)
        elif game_action.is_special():
            game_map = self.__perform_action_special(
                game_action, game_map)
        elif game_action.is_env():
            game_map = self.__perform_env_action(
                game_action, game_map)
        return game_map

    def initialise_drone_positions_for_players(self, game_map: GameMap, players, drone_id_generator):
        for player in players:
            for _ in range(0, player.drone_no):
                new_drone_id = drone_id_generator.get_new_drone_id(
                    player.player_id)
                print(f'--> For player {player.player_id} -- {new_drone_id}')
                new_drone = Drone(player.player_id, new_drone_id)
                init_pos = ((game_map.size[0]/2 + player.player_id),
                            (game_map.size[1]/2 + player.player_id))
                cell = game_map.get_cell(init_pos)
                cell.add_drone(new_drone)


class EnvActionUtils():

    def __init__(self):
        pass

    def perform_env_kill_single(self, player_id: str, drone_id: str, game_map: GameMap) -> GameMap:
        assert '_' in drone_id
        cell = game_map.get_cell(drone_id)
        if cell == None:
            # If cell is None it means that drone can not anymore perform action, since it does not exist anymore
            print(
                f"""(?)\t- Drone: {drone_id} was NOT killed in cell: {cell.position}""")
            return game_map
        for drone in cell.drones:
            d_id = drone.drone_id
            if d_id == drone_id:
                if not drone.is_alive():
                    removed = cell.remove_drone(d_id)
                    assert removed
                    print(
                        f"""\t- Drone: {drone_id} was killed in cell: {cell.position}""")
                    return game_map
        return game_map

    def perform_env_kill_all(self, game_map: GameMap) -> GameMap:
        drones = game_map.get_drones()
        for owner_id in drones:
            player_drones = drones[owner_id]
            for drone in player_drones:
                game_map = self.perform_env_kill_single(
                    'ENV', drone.drone_id, game_map)
        return game_map

    def perform_env_attack_single(self, player_id: str, drone_id: str, game_map: GameMap) -> GameMap:
        cell = game_map.get_cell(drone_id)
        if cell == None:
            # If cell is None it means that drone can not anymore perform action, since it does not exist anymore
            return game_map
        # TODO attack single
        return game_map

    def perform_env_attack_all(self, game_map: GameMap) -> GameMap:
        # TODO attack all
        return game_map

    def perform_env_merge_single(self, player_id: str, drone_id: str, game_map: GameMap) -> GameMap:
        cell = game_map.get_cell(drone_id)
        if cell == None:
            # If cell is None it means that drone can not anymore perform action, since it does not exist anymore
            return game_map
        # TODO merge single
        return game_map

    def perform_env_merge_all(self, game_map: GameMap) -> GameMap:
        # TODO merge all
        return game_map

    def perform_env_detonate_single(self, player_id: str, drone_id: str, game_map: GameMap) -> GameMap:
        cell = game_map.get_cell(drone_id)
        if cell == None:
            # If cell is None it means that drone can not anymore perform action, since it does not exist anymore
            return game_map
        # TODO detonate all
        return game_map

    def perform_env_detonate_all(self, game_map: GameMap) -> GameMap:
        # TODO detonate all
        return game_map
