from Environment import Environment
from Bot import Bot, RandomBot
from utils.config_utils import *


# config_path = config_creation_wizard()
config_path = 'config-test.JSON'
is_print = True

config = Config(config_path)
env = Environment(config)
# TODO_5 - data logger/collector
# Play a game
input('To start game press [any] key...')
keep_playing = True
while keep_playing:
    frame = env.get_frame()
    print('------------------------------------------------')
    for player in env.player_svc.players:
        players_decissions = player.bot.make_decissions(frame)
        if is_print:
            print(f"""
            Player making decissions:
                Player_id: {player.player_id}
                Turn: {env.engine.cur_turn}
                Decissions: {list(map( lambda decission: str(decission), players_decissions))}
            """)
        env.pass_actions(players_decissions)

    keep_playing = env.end_turn()
