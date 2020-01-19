

class DataVisualiser():

    def __init__(self):
        pass

    def from_game_frame(self, game_frame):
        pass


class GameFrameData():

    def __init__(self):
        pass

    def from_game_frame(self, game_frame):
        # TODO
        return self


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
            self.db_frame[turn_id] = GameFrameData(
            ).from_game_frame(game_frame)

    def store_player_decissions_data(self, turn_id, player_id, decissions):
        turn_id = str(turn_id)
        if turn_id not in self.db_decission:
            self.db_decission[turn_id] = {}
        for dec in decissions:
            # TODO
            pass
