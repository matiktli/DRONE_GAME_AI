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
    def is_occupied(self, occupied_by: int = -1) -> bool:
        result = self.drones != None
        if occupied_by != -1:
            result = result and occupied_by in [
                int(d.drone_id) for d in self.drones]
        return result

    def add_drone(self, drone: Drone):
        assert not self.is_occupied(drone.drone_id)
        self.drones.append(drone)

    def remove_drone(self, drone_id):
        assert self.is_occupied(drone_id)
        for i, drone in enumerate(self.drones):
            if drone.drone_id == drone_id:
                del self.drones[i]
                break


"""
Game map representing 2D Grid
"""


class GameMap():

    def __init__(self, initial_size=(100, 100)):
        self.size = initial_size
        self.grid = np.array(self.__initialise_grid(initial_size))

    def __initialise_grid(self, size) -> []:
        grid = [[None for x in range(size[0])] for y in range(size[1])]
        for y in range(size[1]):
            for x in range(size[0]):
                grid[y][x] = Cell(position=(x, y), drones=None)

        print(f'Initialised grid of size: {size}')
        return grid

    def get_cell(self, location) -> Cell:
        assert self.grid != None
        if isinstance(location, tuple):
            # Get single cell by location: (x,y)
            x, y = location[0], location[1]
            return self.grid[y][x]
        elif isinstance(location, int):
            # Get single cell by int id
            id_int = location
            return self.grid.ravel()[id_int]
        else:
            return None

    def change_drone_position(self, drone_id, current_position: tuple, new_position: tuple):
        assert new_position[0] in range(
            0, self.size[0]) and new_position[1] in range(0, self.size[1])
        cell = self.get_cell(current_position)
        assert cell.is_occupied() == True
        drone = [drone for drone in cell.drones if drone.drone_id == drone_id]
        assert len(drone) == 1 and drone[0] != None
        drone = drone[0]

        new_cell = self.get_cell(new_position)
        new_cell.add_drone(drone)

        cell.remove_drone(drone)

    def for_each_cell_do(self, function, params: []):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                curent_cell = self.get_cell((x, y))
                function(curent_cell, params)
