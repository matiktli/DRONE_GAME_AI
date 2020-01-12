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
    # When two or more drones are at the same cell
    ATTACK = {'id': 100}

    # When drone is surrounded by at least 3 oponent drones and is only drone in cell
    DETONATE = {'id': 101}


"""
Game state representation dto
"""


class GameFrame():

    def __init__(self, map: GameMap):
        self.map = map


"""
Game action requests to engine dto
"""


class GameAction():

    def __init__(self, player_id, drone_id, drone_position, action: Action | EnvAction):
        self.player_id = player_id
        self.drone_id = drone_id
        self.drone_position = drone_position
        self.action = action

    def is_move(self):
        return self.action in [Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT]

    def is_special(self):
        return self.action in [Action.STAY, Action.DUPLICATE]

    def is_env(self):
        return self.action in [EnvAction.ATTACK, EnvAction.DETONATE]

    # Bad implementation
    def __get_new_position(self):
        assert self.drone_position != None
        assert self.action != None
        assert self.is_move()
        return (self.drone_position[0] + self.action['vector'][0], self.drone_position[1] + self.action['vector'][1])


"""
MAIN Game engine.
"""


class GameEngine():

    def __init__(self, game_map: GameMap, max_turns=100):
        self.cur_turn = 0
        self.max_turns = max_turns
        self.actions_query = []
        self.game_map = game_map
        self.utils = GameEngineUtils()

    # Add single drone action to query (for each drone in each player)
    def add_action_to_query(self, game_action: GameAction):
        self.actions_query.append(game_action)

    # Add all environment decission actions to query (once a turn)
    def add_environment_actions_to_query(self):
        for y in range(0, self.game_map.size[1]):
            for x in range(0, self.game_map.size[0]):
                game_env_action = None
                cell = self.game_map.get_cell((x, y))
                # TODO - decide how to add env actions

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
        return {'is_on': self.cur_turn <= self.max_turns}


"""
Utility class for game engine. 'Physics' maintainer.
"""


class GameEngineUtils():

    def __init__(self):
        pass

    # Calculate new position with RESPECTING game engine, end of maps are connected as default
    def __calculate_new_position(self, initial_position: tuple, action_vector: tuple, map_x_y: tuple) -> tuple:
        # TODO - implement move logic

        return initial_position

    # Obtain drone from cell with verifying player id, drone position and drone id.
    def __obtain_drone_from_cell(self, player_id, drone_id, drone_position, game_map):
        cell = game_map.get_cell(drone_position)
        assert cell.is_occupied(drone_id)
        drone: Drone = next(
            (d for d in cell.drones if d.drone_id == drone_id), None)
        assert drone != None
        assert player_id == drone.player_id
        return drone, cell

    # Logic responsible for valid movement of drone

    def __perform_action_move(self, game_action: GameAction, game_map: GameMap) -> GameMap:
        assert game_action.is_move()
        # Valid new positions
        new_position = self.__calculate_new_position(
            game_action.drone_position, game_action.action['vector'], game_map.size)
        drone, cell = self.__obtain_drone_from_cell(game_action.player_id,
                                                    game_action.drone_id, game_action.drone_position, game_map)
        # Drone perform action - so losses energy
        drone.action_move()
        is_dead = drone.get_state()
        # Map accepts movement besides of drone state, why not
        game_map.change_drone_position(
            drone.drone_id, game_action.drone_position, new_position)

        if is_dead:
            # Remove drone from cell - so kill it
            new_cell = game_map.get_cell(new_position)
            new_cell.remove_drone(drone.drone_id)
        return game_map

    # Logic responsible for valid special actions of drone
    def __perform_action_special(self, game_action: GameAction, game_map: GameMap) -> GameMap:
        assert game_action.is_special()
        drone, cell = self.__obtain_drone_from_cell(
            game_action.player_id, game_action.drone_id, game_action.drone_position, game_map)

        # Duplicate action
        if game_action.action == Action.DUPLICATE:
            drone.action_duplicate()
            # TODO - spawn new drone
        # Stay action
        if game_action.action == Action.STAY:
            drone.action_stay()
        is_dead = drone.get_state()

        if is_dead:
            cell.remove_drone(drone.drone_id)
        return game_map

    # Login responsible for performing env decided actions
    def __perform_env_action(self, game_action: GameAction, game_map: GameMap) -> GameMap:
        # TODO - implement env specific
        return game_map

    # Public function to interact with env (map)
    def perform_action_on_env(self, game_action: GameAction, game_map: GameMap) -> GameMap:
        if game_action.is_move():
            game_map = self.__perform_action_move(game_action, game_map)
        if game_action.is_special():
            game_map = self.__perform_action_special(game_action, game_map)
        if game_action.is_env():
            game_map = self.__perform_env_action(game_action, game_map)
        return game_map
