from .DataService import GameFrameData, DecissionData
import matplotlib.pyplot as plt
import pandas as pd


class DataVisualizer():

    def __init__(self):
        pass

    def __visualize_single_game_frame_data(self, game_frame_data: GameFrameData):
        pass

    def replay_game(self, game_frames_data, decissions_data):
        for turn_id in game_frames_data:
            game_frame_data = game_frames_data[turn_id]
            self.__visualize_single_game_frame_data(game_frame_data)
