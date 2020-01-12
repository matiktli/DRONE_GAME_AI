from Environment import Environment
from Bot import Bot, RandomBot
from utils.config_utils import *


config_path = config_creation_wizard()
# config_path = 'TEST_CONFIG.json'
config = Config(config_path)
env = Environment(config)
exit()
# Play a game
keep_playing = True
while keep_playing:
    frame = env.get_frame()
    for player in env.player_svc.players:
        players_decissions = player.make_decissions(frame)
        env.pass_actions(players_decissions)

    keep_playing = env.end_turn()
