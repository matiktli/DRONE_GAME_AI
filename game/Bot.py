from abc import ABC, abstractmethod
from Engine import GameFrame, GameAction, Action
from Entity import Drone
import random


class Bot(ABC):

    def __init__(self, player_id, allowed_actions):
        self.player_id = player_id
        self.allowed_actions = allowed_actions

    # Make decission for each of player bots, returns list of GameMoves
    @abstractmethod
    def make_decissions(self, game_frame: GameFrame) -> []:
        pass


class RandomBot(Bot):

    def __init__(self, player_id, allowed_actions):
        super().__init__(player_id, allowed_actions)

    def make_decissions(self, game_frame: GameFrame, rewards) -> []:
        drones_c = 0
        actions_to_perform = []
        for cell in game_frame.map.grid_flatten():
            if cell.is_occupied():
                for drone in cell.drones:
                    if drone.player_id == self.player_id:
                        drones_c = drones_c + 1
                        decided_action = self.__make_decission(
                            game_frame, drone, self.allowed_actions)
                        actions_to_perform.append(decided_action)
        print(
            f'\n\tPlayer: {self.player_id} has made decision for: {drones_c} drones that were left')
        return actions_to_perform

    # Make random action for single drone
    def __make_decission(self, game_frame: GameFrame, drone: Drone, allowed_actions) -> GameAction:
        rand_action = random.choice(allowed_actions)
        drone_pos = game_frame.map.get_cell(drone.drone_id).position
        return GameAction(drone.player_id, drone.drone_id, drone_pos, rand_action)
