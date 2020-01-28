from abc import ABC
import numpy as np
from Entity import Drone

"""
Single Cell on the 2D Grid
"""


class Cell():

    def __init__(self, id=0, position=(0, 0), drones=[]):
        self.position = position
        self.drones = drones

    # Returns if there is any ship inside the cell
    def is_occupied(self, drone_id=None, player_id=None) -> bool:
        result = self.drones != None and len(self.drones) > 0
        if drone_id != None and result:
            result = result and drone_id in [d.drone_id for d in self.drones]
        if player_id != None and result:
            result = result and player_id in [d.player_id for d in self.drones]
        return result

    def get_drone(self, drone_id: str) -> Drone:
        for d in self.drones:
            if d.drone_id == drone_id:
                return d
        return None

    def add_drone(self, drone: Drone):
        assert not self.is_occupied(drone.drone_id)
        if self.drones == None:
            self.drones = []
        self.drones.append(drone)

    def remove_drone(self, drone_id) -> bool:
        assert self.is_occupied(drone_id=drone_id)
        for i, drone in enumerate(self.drones):
            if drone.drone_id == drone_id:
                del self.drones[i]
                return True
        return False

    def get_drones(self):
        drones = {}
        if not self.is_occupied():
            return drones
        for drone in self.drones:
            if str(drone.player_id) not in drones:
                drones[str(drone.player_id)] = []
            drones[str(drone.player_id)].append(drone)
        return drones


"""
Game map representing 2D Grid
"""


class GameMap():

    def __init__(self, initial_size=(100, 100)):
        self.size = initial_size
        self.grid = np.asarray(self.__initialise_grid(initial_size))

    def __initialise_grid(self, size) -> []:
        grid = [[None for x in range(size[0])] for y in range(size[1])]
        for y in range(size[1]):
            for x in range(size[0]):
                grid[y][x] = Cell(position=(x, y), drones=None)

        print(f'Initialised grid of size: {size}')
        return grid

    # Get cell by search that is either: tuple - position(x,y) or int - drone_id
    def get_cell(self, search) -> Cell:
        assert self.grid.any()
        if isinstance(search, tuple):
            # Get single cell by search: (x,y)
            x, y = int(search[0]), int(search[1])
            return self.grid[y][x]
        elif isinstance(search, str):
            # Get single cell by drone_id id
            for cell in self.grid.ravel():
                if cell.is_occupied():
                    for drone in cell.drones:
                        if drone.drone_id == search:
                            return cell
        elif isinstance(search, int):
            for cell in self.grid.ravel():
                if cell.is_occupied():
                    for drone in cell.drones:
                        if drone.player_id == search:
                            return cell
        else:
            return None

    # With assumption that move is valid it changes the position of drone
    def change_drone_position(self, drone_id, current_position: tuple, new_position: tuple):
        assert new_position != current_position

        cell = self.get_cell(current_position)
        assert cell.is_occupied() == True
        drone = [drone for drone in cell.drones if drone.drone_id == drone_id]
        assert len(drone) == 1 and drone[0] != None
        drone = drone[0]

        new_cell = self.get_cell(new_position)
        new_cell.add_drone(drone)

        cell.remove_drone(drone.drone_id)
        assert self.get_cell(drone.drone_id) == self.get_cell(new_position)

    def grid_flatten(self):
        return self.grid.flatten()

    # Return drones wrapper for callculation purposes {'<player_id>': Drones[]}
    def get_drones(self) -> object:
        drones = {}
        for cell in self.grid_flatten():
            drones_in_cell = cell.get_drones()
            for owner_id in drones_in_cell:
                if owner_id not in drones:
                    drones[owner_id] = []
                for d in drones_in_cell[owner_id]:
                    drones[owner_id].append(d)
        return drones

    def reset_drones_attack(self):
        drones = self.get_drones()
        for p_id in drones:
            for d in drones[str(p_id)]:
                d.has_attacked = False
