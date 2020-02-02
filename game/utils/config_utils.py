import json


def load_config(path):
    with open(path, 'r') as config_file:
        data = json.load(config_file)
        return data


def save_config(path, config_json_data):
    with open(path, 'w') as config_file:
        json.dump(config_json_data, config_file)


def config_creation_wizard():
    # Collect main info
    config_file_name = input('- Path of config file: ')
    map_size_x = int(input('- Map initial size X: '))
    map_size_y = int(input('- Map initial size Y: '))
    number_of_players = int(input('- Number of players: '))
    number_of_drones_per_player = int(input('- Number of drones per player: '))
    max_turns = int(input('- Max number of turns: '))
    drones_energy_max = int(input('- Default drones max energy: '))
    drones_energy_starting = int(input('- Default drones starting energy: '))
    drones_energy_cost_move = int(input('- Default drones move energy cost: '))
    drones_energy_cost_vector_duplicate = float(
        input('- Default drones duplicate energy cost vector: '))
    drones_energy_gain_stay = int(input('- Default drones stay energy gain: '))

    # Collect env info
    env_info = {
        'actions': ['KILL', 'ATTACK', 'MERGE', 'DETONATE']
    }

    # Collect players info
    players_info = []
    for i in range(0, number_of_players):
        player_type = input(f'Type of player {i}, in [RAND, BOT]: ')
        path = ''
        if player_type != 'RAND':
            path = input(f'Model path for player {i}: ')
        player_info = {
            'id': i,
            'type': player_type,
            'path': path,
            'drone_no': number_of_drones_per_player,
            'allowed_actions': ['MOVE_LEFT', 'MOVE_RIGHT', 'MOVE_UP', 'MOVE_DOWN', 'STAY', 'DUPLICATE'],
            'drones_energy_max': drones_energy_max,
            'drones_energy_starting': drones_energy_starting,
            'drones_energy_cost_move': drones_energy_cost_move,
            'drones_energy_cost_vector_duplicate': drones_energy_cost_vector_duplicate,
            'drones_energy_gain_stay': drones_energy_gain_stay
        }
        players_info.append(player_info)

    # Create config file
    json_file = {
        'game.map.size_x': map_size_x,
        'game.map.size_y': map_size_y,
        'game.max_turns': max_turns,
        'game.players_no': number_of_players,
        'env': env_info,
        'players': players_info
    }
    save_config(config_file_name, json_file)
    return config_file_name


"""
Class to simplify loading of config data
"""


class Config():

    def __init__(self, path):
        self.raw_data = load_config(path)
        self.map_size = (int(self.raw_data['game.map.size_x']),
                         int(self.raw_data['game.map.size_y']))
        self.max_turns = int(self.raw_data['game.max_turns'])
        self.env_config = self.raw_data['env']
        self.number_of_players = int(self.raw_data['game.players_no'])
        self.players_config = self.raw_data['players']


if __name__ == "__main__":
    config_creation_wizard()
