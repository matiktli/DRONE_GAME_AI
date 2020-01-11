from abc import ABC
import numpy as np

"""
Single Cell on the 2D Grid
"""


class Cell():

    def __init__(self, id=0, position=(0, 0), drones=None):
        self.position = position
        self.drones = drones

    # Returns if there is any ship inside the cell
    def is_occupied(self, occupied_by: int) -> bool:
        # TODO
        return self.drones != None


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

    def for_each_cell_do(self, function, params: []):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                curent_cell = self.get_cell((x, y))
                function(curent_cell, params)
