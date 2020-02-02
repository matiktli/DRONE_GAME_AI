from Environment import Environment
from utils.config_utils import *
from data.DataService import DataStore
import data.DataVisualizer as DV
import sys
import random
from GameContainer import SingleGameContainer

CONFIG_PATH = sys.argv[1]
IS_DISPLAY = False
IS_SAVE = True
GAME_NAME = random.randint(0, 100)

data_store = DataStore()
data_visualizer = DV.DataVisualizer(
    str(GAME_NAME), IS_DISPLAY)

# --- Single Game Container Start ---
container = SingleGameContainer()\
    .with_config(CONFIG_PATH, IS_DISPLAY, GAME_NAME)\
    .with_data_store(data_store)\
    .with_data_visualizer(data_visualizer)

container.simulate()
# --- Single Game Container End ---


data_store.save_data_to_file(
    f'test/FRAME_DATA_{GAME_NAME}.json', f'test/DECISION_DATA_{GAME_NAME}.json')
data_store = data_store.with_data_from_file(
    f'test/FRAME_DATA_{GAME_NAME}.json', f'test/DECISION_DATA_{GAME_NAME}.json')


# After game actions
img_frames = data_visualizer.replay_game(data_store.db_frame,
                                         data_store.db_decission)
data_visualizer.save_gif(img_frames, f'test/GAME_REPLAY_{GAME_NAME}.gif')

plt = data_visualizer.plot_from_data(
    data_store.db_frame, max_turns=container.CONFIG.max_turns, init_players=container.CONFIG.number_of_players)
data_visualizer.save_plot(plt, f'test/GAME_GRAPH_1_{GAME_NAME}.png')
