from Environment import Environment
from Bot import Bot, RandomBot
from utils.config_utils import *
from DataService import DataCollector
from DataVisualiser import DataVisualiser


# config_path = config_creation_wizard()
config_path = 'config-test.JSON'
is_print = True

config = Config(config_path)
env = Environment(config)
data_collector = DataCollector()
data_visualiser = DataVisualiser()


# Play a game
input('To start game press [any] key...')
keep_playing = True
while keep_playing:
    frame = env.get_frame()
    data_collector.store_game_frame_data(env.engine.cur_turn, frame)
    print('------------------------------------------------')
    for player in env.player_svc.players:
        players_decissions = player.bot.make_decissions(frame)
        data_collector.store_player_decissions_data(env.engine.cur_turn,
                                                    player.player_id, players_decissions)
        if is_print:
            print(f"""
            Player making decissions:
                Player_id: {player.player_id}
                Turn: {env.engine.cur_turn}
                Decissions: {list(map( lambda decission: str(decission), players_decissions))}
            """)
        env.pass_actions(players_decissions)

    keep_playing = env.end_turn()
data_visualiser.visualise_from_data(
    data_collector.db_frame, max_turns=config.max_turns, init_players=config.number_of_players)
