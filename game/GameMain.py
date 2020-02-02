from Environment import Environment
from utils.config_utils import *
from data.DataService import DataStore
from data.DataVisualizer import DataVisualizer
import sys
import random
from Container import SingleGameContainer
from RewardGenerator import RewardGenerator


# Configuration part
CONFIG_PATH = sys.argv[1]
IS_DISPLAY = False
IS_SAVE = True
GAME_NAME = random.randint(0, 100)
FOLDER_PREFIX = 'test/'

# Initialise data storage impl
data_store = DataStore()
reward_generator = RewardGenerator()

# --- Single Game Container Start ---
container = SingleGameContainer()\
    .with_config(CONFIG_PATH, IS_DISPLAY, GAME_NAME)\
    .with_data_store(data_store)\
    .with_reward_generator(reward_generator)\
    .simulate()\
    .save_game_outcome(FOLDER_PREFIX)
# --- Single Game Container End ---

# Read data from saved storage
data_store = DataStore().with_data_from_file(
    f'{FOLDER_PREFIX}GAME_{GAME_NAME}/FRAME_DATA.json', f'{FOLDER_PREFIX}GAME_{GAME_NAME}/DECISION_DATA.json')

# Initialise game visualization module
data_visualizer = DataVisualizer(str(GAME_NAME), IS_DISPLAY)

# Replay game and save gif
img_frames = data_visualizer.replay_game(data_store.db_frame,
                                         data_store.db_decission)
data_visualizer.save_gif(
    img_frames, f'{FOLDER_PREFIX}GAME_{GAME_NAME}/GAME_REPLAY.gif')

# Display plot created from data and save it
plt = data_visualizer.plot_from_data(
    data_store.db_frame, max_turns=container.CONFIG.max_turns, init_players=container.CONFIG.number_of_players)
data_visualizer.save_plot(
    plt, f'{FOLDER_PREFIX}GAME_{GAME_NAME}/GAME_GRAPH_1.png')
