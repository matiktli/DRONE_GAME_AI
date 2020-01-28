from abc import ABC

"""
Player's Drone entity
"""


class Drone():

    def __init__(self, player_id, drone_id, energy=255, energy_bandwidth=(0, 255), move_cost=10, duplicate_cost_vector=0.6, recharge_energy=15):
        self.player_id = player_id
        self.drone_id = drone_id
        self.energy = energy
        self.energy_bandwidth = energy_bandwidth
        self.has_attacked = False
        self.move_cost = move_cost
        self.duplicate_cost_vector = duplicate_cost_vector
        self.recharge_energy = recharge_energy

    # Optymise energy to set bandwidth, returns False if drone died in this process
    def __optymise_energy(self) -> bool:
        assert self.energy != None
        if self.energy <= self.energy_bandwidth[0]:
            self.energy = self.energy_bandwidth[0]
            return False
        elif self.energy > self.energy_bandwidth[1]:
            self.energy = self.energy_bandwidth[1]
        return True

    def action_move(self):
        self.energy = self.energy - self.move_cost
        self.__optymise_energy()

    def action_stay(self):
        self.energy = self.energy + self.recharge_energy
        self.__optymise_energy()

    # Add drone stats
    def action_merge(self, drone_to_merge_in):
        self.energy = self.energy + drone_to_merge_in.energy
        self.__optymise_energy()

    def action_duplicate(self):
        energy_loss = int(self.energy * self.duplicate_cost_vector)
        self.energy = self.energy - energy_loss
        self.__optymise_energy()

    def receive_demage(self, energy_damage=15):
        self.energy = self.energy - energy_damage
        self.__optymise_energy()

    def action_env_attack(self) -> int:
        self.has_attacked = True
        self.__optymise_energy()
        return self.energy

    def is_alive(self) -> bool:
        result = self.__optymise_energy()
        return result
