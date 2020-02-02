import numpy as np
from Map import Cell, GameMap
from enum import Enum
from Entity import Drone
from abc import ABC
import random


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
        self.player_service = player_service
        self.actions_query = []
        self.game_map = game_map
        self.env_utils = EnvActionUtils()
        self.utils = GameEngineUtils(
            self.env_utils, self.player_service.drone_id_generator)
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
    def add_environment_actions_to_query(self, available_actions):
        env_actions_to_perform = []

        for action in available_actions:
            env_actions_to_perform.append(
                GameAction('ENV', 'ENV', (-1, -1), action)
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
        drones = self.game_map.get_drones()
        is_one_player_left = len(drones) == 1
        flat_drones = []
        for owner_id in drones:
            ds = drones[owner_id]
            for d in ds:
                flat_drones.append(d)

        max_drones = self.game_map.size[0] * \
            self.game_map.size[1] * int(self.game_map.size[0] / 2)
        max_drones = 3000
        is_to_much_drones = len(flat_drones) > max_drones
        return {'is_on': not is_turn_max_limit and not is_one_player_left and not is_to_much_drones}

    def increment_turn_counter(self):
        tmp = self.cur_turn
        self.cur_turn = tmp + 1
        return self.cur_turn


"""
Utility class for game engine. 'Physics' maintainer.
"""


class GameEngineUtils():

    def __init__(self, env_utils, drone_id_generator):
        self.env_utils = env_utils
        self.drone_id_generator = drone_id_generator

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
        drone, cell = self.__obtain_drone_from_cell(
            game_action.player_id, game_action.drone_id, game_action.drone_position, game_map)

        # Duplicate action
        if game_action.action == Action.DUPLICATE:
            drone.action_duplicate()
            new_drone_id = self.drone_id_generator.get_new_drone_id(
                game_action.player_id)
            new_drone = Drone(game_action.player_id, new_drone_id,
                              drone.energy, drone.energy_bandwidth)
            spawn_position = cell.position + \
                self.__calculate_new_position(
                    cell.position, (0, -1), game_map.size)
            new_cell = game_map.get_cell(spawn_position)
            assert new_cell
            new_cell.add_drone(new_drone)
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
        buffor_size = int(0.2 * game_map.size[0])
        for player in players:
            init_x = random.randint(
                0 + buffor_size, game_map.size[0] - buffor_size)
            init_y = random.randint(
                0 + buffor_size, game_map.size[1] - buffor_size)

            for _ in range(0, player.drone_no):
                new_drone_id = drone_id_generator.get_new_drone_id(
                    player.player_id)
                new_drone = Drone(
                    player.player_id,
                    new_drone_id,
                    player.drones_energy_starting,
                    player.drones_energy_bandwith,
                    player.drones_energy_cost_move,
                    player.drones_energy_cost_vector_duplicate,
                    player.drones_energy_gain_stay
                )

                init_d_x = random.randint(
                    init_x - buffor_size-1, init_x + buffor_size-1)
                init_d_y = random.randint(
                    init_y - buffor_size-1, init_y + buffor_size-1)
                cell = game_map.get_cell((init_d_x, init_d_y))
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
            print(
                f"""(?)\t- Drone: {drone_id} did NOT attack in cell: {cell.position}""")
            return game_map
        my_drone = cell.get_drone(drone_id)
        assert my_drone
        assert my_drone.has_attacked == False
        enemy_drones_in_cell = [
            d for d in cell.drones if str(d.player_id) != drone_id.split('_')[0]]
        if not enemy_drones_in_cell:
            return game_map
        target_drone = random.choice(enemy_drones_in_cell)
        assert target_drone != None
        damage_to_target = int(my_drone.energy * 0.8)
        damage_to_source = int(target_drone.energy * 0.2)
        target_drone.receive_demage(damage_to_target)
        my_drone.receive_demage(damage_to_source)
        print(
            f"""\t- Drone: {my_drone.drone_id} attacked {target_drone.drone_id} and dealed {damage_to_target} in cell: {cell.position}""")
        if not my_drone.is_alive():
            removed = cell.remove_drone(my_drone.drone_id)
            assert removed
            print(
                f"""\t\t- Drone: {my_drone.drone_id} died after attacking""")
        if not target_drone.is_alive():
            removed = cell.remove_drone(target_drone.drone_id)
            assert removed
            print(
                f"""\t\t- Drone: {target_drone.drone_id} died after BEEING attacking""")
        return game_map

    def perform_env_attack_all(self, game_map: GameMap) -> GameMap:
        for cell in game_map.grid_flatten():
            if cell.is_occupied():
                drones_in_cell = cell.drones
                for d in drones_in_cell:
                    if not d.has_attacked:
                        game_map = self.perform_env_attack_single(
                            'ENV', d.drone_id, game_map)

        return game_map

    def perform_env_merge_single(self, player_id: str, drone_id: str, game_map: GameMap) -> GameMap:
        cell = game_map.get_cell(drone_id)
        if cell == None:
             # If cell is None it means that drone can not anymore perform action, since it does not exist anymore
            print(
                f"""(?)\t- Drone: {drone_id} did NOT merged in cell [NOT_EXISTING]: {cell.position}""")
            return game_map
        my_drone = cell.get_drone(drone_id)
        assert my_drone
        my_other_drones = []
        for d in cell.drones:
            # If there are enemy drones in the cell we can not merge
            if d.player_id != my_drone.player_id:
                print(
                    f"""(?)\t- Drone: {drone_id} did NOT merged in cell [ENEMY_CLOSE]: {cell.position}""")
                return game_map
            elif d.drone_id != my_drone.drone_id:
                my_other_drones.append(d)
        # If that happens that there are no other drones then just do nothing
        if len(my_other_drones) == 0:
            print(
                f"""(?)\t- Drone: {drone_id} did NOT merged in cell [NO_NEIGHBOURS]: {cell.position}""")
            return game_map
        target_drone = random.choice(my_other_drones)
        assert target_drone
        target_drone.action_merge(my_drone)
        cell.remove_drone(my_drone.drone_id)
        print(
            f"""(?)\t- Drone: {drone_id} did merged, into drone: {target_drone.drone_id}, in cell [NO_NEIGHBOURS]: {cell.position}""")
        return game_map

    def perform_env_merge_all(self, game_map: GameMap) -> GameMap:
        drones = game_map.get_drones()
        for owner_id in drones:
            player_drones = drones[owner_id]
            for drone in player_drones:
                game_map = self.perform_env_merge_single(
                    'ENV', drone.drone_id, game_map)
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
