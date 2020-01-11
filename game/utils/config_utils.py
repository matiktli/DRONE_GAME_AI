import json


def load_config(path):
    with open(path, 'r') as config_file:
        data = json.load(config_file)
        return data


def save_config(path, config_json_data):
    with open(path, 'w') as config_file:
        json.dump(config_json_data, config_file)


def config_creation_wizard():
    config_file_name = input('- Name of config file: ')
    map_size_x = int(input('- Map initial size X: '))
    map_size_y = int(input('- Map initial size Y: '))
    number_of_players = int(input('- Number of players: '))
    number_of_drones_per_player = int(input('- Number of drones per player: '))


"""
Class to simplify loading of config data
"""


class Config():

    def __init__(self, path):
        raw_data = load_config(path)
        self.game_initial_size = (int(raw_data['game']['initial_size']['x']),
                                  int(raw_data['game']['initial_size']['y']))
        self.game_max_turns = int(raw_data['game']['max_turns'])
        self.game_number_of_players = len(raw_data['players'])
        self.players = raw_data['players']


if __name__ == "__main__":
    config_creation_wizard()
