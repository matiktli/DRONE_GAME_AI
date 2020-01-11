from Environment import Environment
from utils.config_utils import Config

config = Config('...')
game_env = Environment(config)
bot = None  # Here we would wrap our model into Bot()

is_run = True
while is_run:
    frame = game_env.get_frame()
    moves = []
    game_env.pass_actions(moves)
    is_run = game_env.end_turn()
