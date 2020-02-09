from abc import ABC, abstractmethod
from collections import namedtuple, defaultdict

# Abstrac reward generator


class Generator(ABC):

    def __init__(self):
        pass

    # Return reward foloat from -1, 1
    @abstractmethod
    def generate_reward(self, game_frames_data, for_player):
        return None

    def extract_extra_data_from_frame(self, game_frame_data):
        # Extract player_id to drone number alive
        players_to_drones_no = defaultdict(int)
        for p_id in game_frame_data.drones:
            players_to_drones_no[p_id] = len(game_frame_data.drones[p_id])

        # Extract player_id to cell number occupied
        players_to_cells_no = defaultdict(int)
        for cell in game_frame_data.grid.ravel():
            if cell.is_occupied():
                drones = cell.get_drones()
                for player_id in drones:
                    # We only count one drone paer player in one cell
                    drone = drones[player_id][0]
                    if drone.player_id not in players_to_cells_no:
                        players_to_cells_no[drone.player_id] = 1
                    else:
                        players_to_cells_no[drone.player_id] = players_to_cells_no[drone.player_id] + 1

        return players_to_drones_no, players_to_cells_no


# Simple drone number base reward generator
# Last frame based
class SimpleRewardGenerator(Generator):

    def __init__(self):
        super().__init__()

    # This one is not capable of generating <-1,0) rewards due to no respecting previous frames
    def generate_reward(self, game_frames_data, for_player):
        for_player = str(for_player)
        current_frame = game_frames_data[str(len(game_frames_data)-1)]
        grid_size = current_frame.grid_size
        players_to_drones_no, players_to_cells_no = self.extract_extra_data_from_frame(
            current_frame)

        current_player_drones_no = players_to_drones_no[for_player]
        drones_alive_vector = (current_player_drones_no /
                               current_frame.drones_no_alive)

        current_player_cells_no = players_to_cells_no[for_player]
        cells_owned_vector = (current_player_cells_no /
                              (grid_size[0] * grid_size[1]))

        reward = 0
        if players_to_drones_no[for_player] > 0:
            reward = current_player_drones_no + current_player_cells_no
            reward = reward + int(current_frame.turn_id)
        return reward
