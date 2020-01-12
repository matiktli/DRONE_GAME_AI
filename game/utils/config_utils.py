import json


def load_config(path):
    with open(path, 'r') as config_file:
        data = json.load(config_file)
        return data


def save_config(path, config_json_data):
    with open(path, 'w') as config_file:
        json.dump(config_json_data, config_file)


def config_creation_wizard():
    config_file_name = input('- Path of config file: ')
    map_size_x = int(input('- Map initial size X: '))
    map_size_y = int(input('- Map initial size Y: '))
    number_of_players = int(input('- Number of players: '))
    number_of_drones_per_player = int(input('- Number of drones per player: '))
    max_turns = int(input('- Max number of turns: '))

    players_info = []
    for i in range(0, number_of_players):
        player_type = input(f'Type of player {i}: [RAND, BOT]')
        path = ''
        if player_type != 'RAND':
            path = input(f'Model path for player {i}: ')
        player_info = {
            'id': i,
            'type': player_type,
            'path': path
        }
        players_info.append(player_info)

    json_file = {
        'game.map.size_x': map_size_x,
        'game.map.size_y': map_size_y,
        'game.max_turns': max_turns,
        'game.players_no': number_of_players,
        'game.drones_per_player_no': number_of_drones_per_player,
        'players': players_info
    }
    save_config(config_file_name, json_file)
    return config_file_name


"""
Class to simplify loading of config data
"""


class Config():

    def __init__(self, path):
        raw_data = load_config(path)
        self.map_size = (int(raw_data['game.map.size_x']),
                         int(raw_data['game.map.size_y']))
        self.max_turns = int(raw_data['game.max_turns'])
        self.number_of_players = int(raw_data['game.players_no'])
        self.drones_per_player = int(raw_data['game.drones_per_player_no'])
        self.players_config = raw_data['players']


if __name__ == "__main__":
    config_creation_wizard()
