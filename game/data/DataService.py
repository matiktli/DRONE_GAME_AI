import copy
import json
import pickle


# Entity representation of GameFrameData
class GameFrameData():

    def __init__(self, turn_id):
        self.turn_id = turn_id
        self.grid = None
        self.grid_size = None
        self.drones = None
        self.drones_flatten = None
        self.players_no_total = None
        self.players_no_alive = None
        self.drones_no_alive = None

    def __get_alive_players_to_drones(self, drones):
        result = {}
        for (player_id, p_drones) in drones.items():
            if len(p_drones) > 0:
                result[player_id] = p_drones
        return result

    def from_game_frame(self, game_frame):
        self.grid = copy.deepcopy(game_frame.map.grid)
        self.grid_size = game_frame.map.size
        self.drones = game_frame.map.get_drones()

        self.drones_flatten = []
        for owner_id in self.drones:
            p_drones = self.drones[owner_id]
            self.drones_flatten.extend(p_drones)

        self.players_no_total = len(self.drones)
        self.players_no_alive = len(
            self.__get_alive_players_to_drones(self.drones))
        self.drones_no_alive = len(self.drones_flatten)
        print(f"""
        Players no TOTAL: {self.players_no_total}
        Players no ALIVE: {self.players_no_alive}
        Drones no ALIVE: {self.drones_no_alive}
        """)
        return self

    # def __str__(self):
    #     pass


# Entity representation of DecissionData
class DecissionData():

    def __init__(self, turn_id):
        self.turn_id = turn_id
        self.drone_id = None
        self.player_id = None
        self.action = None

    def from_game_action(self, game_action):
        self.drone_id = game_action.drone_id
        assert self.drone_id
        self.player_id = self.drone_id[0]
        self.action = game_action.action
        return self


# Database representation, for now in-mem
class DataStore():

    def __init__(self):
        self.db_frame = {}
        self.db_decission = {}

    # Initialise database from file
    def with_data_from_file(self, path_to_db_frame_store=None, path_to_db_decission_store=None):
        def load_from_file(file_path):
            with open(file_path, 'rb') as json_file:
                #data = json.load(json_file)
                data = pickle.load(json_file)
                return data
        if path_to_db_frame_store:
            self.db_frame = load_from_file(path_to_db_frame_store)
        if path_to_db_decission_store:
            self.db_decission = load_from_file(path_to_db_decission_store)
        return self

    # Save database to file
    def save_data_to_file(self, path_to_db_frame_store=None, path_to_db_decission_store=None):
        def save_to_file(file_path, db_data):
            with open(file_path, 'wb') as outfile:
                # json.dump(db_data, outfile)
                pickle.dump(db_data, outfile)
                return True
        if path_to_db_frame_store:
            saved = save_to_file(path_to_db_frame_store, self.db_frame)
            assert saved

        if path_to_db_decission_store:
            saved = save_to_file(path_to_db_decission_store, self.db_decission)
            assert saved
        return saved

    def store_game_frame_data(self, turn_id, game_frame):
        turn_id = str(turn_id)
        if turn_id not in self.db_frame:
            game_frame_data = GameFrameData(
                turn_id).from_game_frame(game_frame)
            self.db_frame[turn_id] = game_frame_data

    def store_player_decissions_data(self, turn_id, player_id, game_actions):
        turn_id = str(turn_id)
        if turn_id not in self.db_decission:
            self.db_decission[turn_id] = []
        for game_action in game_actions:
            decission_data = DecissionData(
                turn_id).from_game_action(game_action)
            self.db_decission[turn_id].append(decission_data)

    def stats(self):
        for turn_id in self.db_frame:
            counter = 0
            fr = self.db_frame[turn_id]
            for cell in fr.grid.ravel():
                if cell.is_occupied():
                    counter = counter + len(cell.drones)
            print(f'{turn_id} -> Alive: {counter}')
