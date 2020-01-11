from abc import ABC

MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, STAY, DUPLICATE = range(0, 6)


class Drone():

    def __init__(self, position=(0, 0), player=None, energy=100):
        self.player = player
        self.energy = energy

    def action_move(self, move_code, move_cost_energy=1):
        assert move_code in range(4)
        self.energy = self.energy - move_cost_energy

    def action_stay(self, stay_recharge_energy=10):
        self.energy = self.energy + stay_recharge_energy

    def action_duplicate(self, duplicate_factor_energy=0.5):
        energy_loss = int(self.energy * duplicate_factor_energy)
        self.energy = self.energy - energy_loss

    def receive_demage(self, energy_damage=10):
        self.energy = self.energy - energy_damage
