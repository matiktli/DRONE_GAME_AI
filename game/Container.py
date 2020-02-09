from Environment import Environment
from utils.config_utils import *
from data.DataService import DataStore
import data.DataVisualizer as DV
import os


"""
This is a container representation of easy to handle game model, with builder structure.
ORDER MATTERS... (yeah, not typical, but i have asserts to enforce)
"""


class SingleGameContainer():

    def __init__(self):
        pass

    def with_config(self, config_path, is_display, game_name):
        self.CONFIG = Config(config_path)
        self.IS_DISPLAY = is_display
        self.GAME_NAME = game_name
        self.ENV = Environment(self.CONFIG)
        return self

    def with_reward_generator(self, reward_generator):
        self.REWARD_GENERATOR = reward_generator
        return self

    def with_data_store(self, data_store):
        self.DATA_STORE = data_store
        return self

    # Start simulating the game
    def simulate(self):
        assert self.CONFIG
        assert self.ENV
        keep_playing = True
        while keep_playing:
            frame = self.ENV.get_frame()
            self.DATA_STORE.store_game_frame_data(
                self.ENV.engine.cur_turn, frame)
            print('------------------------------------------------')
            rewards = [0 for p in self.ENV.player_svc.players]
            for player in self.ENV.player_svc.players:
                players_decissions = player.bot.make_decissions(
                    frame, rewards[player.player_id])
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

            for player in self.ENV.player_svc.players:
                reward = self.REWARD_GENERATOR.generate_reward(
                    self.DATA_STORE.db_frame, player.player_id)
                print(
                    f'Reward for player: {player.player_id} at turn: {self.ENV.engine.cur_turn-1}-> {reward}')
                rewards.append(reward)

        return self

    def save_game_outcome(self, path_prefix):
        assert self.DATA_STORE
        assert self.GAME_NAME
        path = path_prefix + 'GAME_' + str(self.GAME_NAME)
        if not os.path.exists(path):
            os.mkdir(path)
        self.DATA_STORE.save_data_to_file(
            path + '/FRAME_DATA.json', path + '/DECISION_DATA.json')
        config_json = self.CONFIG.raw_data
        save_config(path + '/CONFIG.json', config_json)
        return self


# DO NOT USE, NEED TO GET RETHINKED
class MultipleGameContainer():

    def __init__(self):
        pass

    def with_configs(self, config_paths: [], is_display, game_names: []):
        assert len(config_paths) == len(game_names)
