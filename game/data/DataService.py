

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
        self.grid = game_frame.map.grid
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

    def __str__(self):
        pass


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


class DataCollector():

    def __init__(self):
        self.db_frame = {}
        self.db_decission = {}

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
        print(f'Turns: {len(self.db_frame)}')
        print(f'Decissions: {len(self.db_decission)}')
