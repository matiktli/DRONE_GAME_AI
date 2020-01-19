

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

    def __init__(self):
        pass


class DataCollector():

    def __init__(self):
        self.db_frame = {}
        self.db_decission = {}

    def store_game_frame_data(self, turn_id, game_frame) -> GameFrameData:
        turn_id = str(turn_id)
        if turn_id not in self.db_frame:
            game_frame_data = GameFrameData(
                turn_id).from_game_frame(game_frame)
            self.db_frame[turn_id] = game_frame_data

    def store_player_decissions_data(self, turn_id, player_id, decissions):
        turn_id = str(turn_id)
        if turn_id not in self.db_decission:
            self.db_decission[turn_id] = {}
        for dec in decissions:
            # TODO store player decission data
            pass
