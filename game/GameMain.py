from Environment import Environment
from Bot import Bot, RandomBot
from utils.config_utils import *
from data.DataService import DataStore
import data.DataVisualizer as DV
import sys
import random


# config_path = config_creation_wizard()
CONFIG_PATH = sys.argv[1]
IS_DISPLAY = False
IS_SAVE = True
GAME_NAME = random.randint(0, 100)


config = Config(CONFIG_PATH)
env = Environment(config)
data_store = DataStore()
data_visualizer = DV.DataVisualizer(
    str(GAME_NAME), IS_DISPLAY, IS_SAVE)


if IS_DISPLAY:
    input('To start game press [any] key...')

# Start simulating the game
keep_playing = True
while keep_playing:
    frame = env.get_frame()
    data_store.store_game_frame_data(env.engine.cur_turn, frame)
    print('------------------------------------------------')
    for player in env.player_svc.players:
        players_decissions = player.bot.make_decissions(frame)
        data_store.store_player_decissions_data(env.engine.cur_turn,
                                                player.player_id, players_decissions)
        if IS_DISPLAY:
            print(f"""
            Player making decissions:
                Player_id: {player.player_id}
                Turn: {env.engine.cur_turn}
                Decissions: {list(map( lambda decission: str(decission), players_decissions))}
            """)
        env.pass_actions(players_decissions)

    keep_playing = env.end_turn()

if IS_SAVE:
    data_store.save_data_to_file(
        f'test/FRAME_DATA_{GAME_NAME}.JSON', f'test/DECISION_DATA_{GAME_NAME}.JSON')

    data_store = data_store.with_data_from_file(
        f'test/FRAME_DATA_{GAME_NAME}.JSON', f'test/DECISION_DATA_{GAME_NAME}.JSON')


# After game actions
data_visualizer.replay_game(data_store.db_frame,
                            data_store.db_decission)

data_visualizer.plot_from_data(
    data_store.db_frame, max_turns=config.max_turns, init_players=config.number_of_players)
