from abc import ABC, abstractmethod
from Engine import GameFrame, GameAction, Action
from Entity import Drone
import random


class Bot(ABC):

    def __init__(self, player_id, possible_actions):
        self.player_id = player_id
        self.possible_actions = possible_actions

    # Make decission for each of player bots, returns list of GameMoves
    @abstractmethod
    def make_decissions(self, game_frame: GameFrame) -> []:
        pass


class RandomBot(Bot):

    def __init__(self, player_id, possible_actions):
        super.__init__(player_id, possible_actions)

    def make_decissions(self, game_frame: GameFrame) -> []:
        actions_to_perform = []
        for cell in game_frame.map.grid:
            if cell.is_occupied(occupied_by=self.player_id):
                for drone in cell.drones:
                    if drone.player_id == self.player_id:
                        decided_action = self.__make_decission(
                            game_frame, drone)
                        actions_to_perform.append(decided_action)
        return actions_to_perform

    # Make random action for single drone
    def __make_decission(self, game_frame: GameFrame, drone: Drone) -> GameAction:
        rand_action = random.choice(game_frame.player_available_actions)
        return GameAction(drone.player_id, drone.drone_id, drone.drone_position, rand_action)
