from abc import ABC

"""
Player's Drone entity
"""


class Drone():

    def __init__(self, player_id, drone_id, energy=255, energy_bandwidth=(0, 255)):
        self.player_id = player_id
        self.drone_id = drone_id
        self.energy = energy
        self.energy_bandwidth = energy_bandwidth

    # Optymise energy to set bandwidth, returns False if drone died in this process
    def __optymise_energy(self) -> bool:
        assert self.energy != None
        if self.energy <= self.energy_bandwidth[0]:
            self.energy = self.energy_bandwidth[0]
            return False
        elif self.energy > self.energy_bandwidth[1]:
            self.energy = self.energy_bandwidth[1]
        return True

    def action_move(self, move_cost_energy=10):
        self.energy = self.energy - move_cost_energy
        self.__optymise_energy()

    def action_stay(self, stay_recharge_energy=15):
        self.energy = self.energy + stay_recharge_energy
        self.__optymise_energy()

    def action_duplicate(self, duplicate_factor_energy=0.4):
        energy_loss = int(self.energy * duplicate_factor_energy)
        self.energy = self.energy - energy_loss
        self.__optymise_energy()

    def receive_demage(self, energy_damage=15):
        self.energy = self.energy - energy_damage
        self.__optymise_energy()

    def is_alive(self) -> bool:
        result = self.__optymise_energy()
        return result
