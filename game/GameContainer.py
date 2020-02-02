from Environment import Environment
from utils.config_utils import *
from data.DataService import DataStore
import data.DataVisualizer as DV


class SingleGameContainer():

    def __init__(self):
        pass

    def with_config(self, config_path, is_display, game_name):
        self.CONFIG = Config(config_path)
        self.IS_DISPLAY = is_display
        self.GAME_NAME = game_name
        self.ENV = Environment(self.CONFIG)
        return self

    def with_data_store(self, data_store):
        self.DATA_STORE = data_store
        return self

    def with_data_visualizer(self, data_visualizer):
        self.DATA_VLISUALIZER = data_visualizer
        return self

    # Start simulating the game
    def simulate(self):
        keep_playing = True
        while keep_playing:
            frame = self.ENV.get_frame()
            self.DATA_STORE.store_game_frame_data(
                self.ENV.engine.cur_turn, frame)
            print('------------------------------------------------')
            for player in self.ENV.player_svc.players:
                players_decissions = player.bot.make_decissions(frame)
                self.DATA_STORE.store_player_decissions_data(self.ENV.engine.cur_turn,
                                                             player.player_id, players_decissions)
                if self.IS_DISPLAY:
                    print(f"""
                    Player making decissions:
                        Player_id: {player.player_id}
                        Turn: {self.ENV.engine.cur_turn}
                        Decissions: {list(map( lambda decission: str(decission), players_decissions))}
                    """)
                self.ENV.pass_actions(players_decissions)

            keep_playing = self.ENV.end_turn()
        return self
