import matplotlib.pyplot as plt
from DataService import GameFrameData
import pandas as pd


class DataVisualiser():
    COLORS = 'bgrcmykw'

    def __init__(self):
        pass

    def __plot_data(self, data):
        df = pd.DataFrame(data)
        for i, label in enumerate(data):
            if 'y' in label:
                plt.plot('x', label, data=df,
                         color=DataVisualiser.COLORS[int(label.replace('y', '')) % (len(DataVisualiser.COLORS))], label=label.replace('y', 'Bot: '), linewidth=2)
        plt.title(
            f'Simulation with: {len(data)-1} bots making random decissions')
        plt.legend()
        plt.show()

    def visualise_from_data(self, data_frames: {}, max_turns=None, init_players=None):
        data = {
            'x': [i for i in range(0, max_turns)]
        }
        for i in range(0, init_players):
            player_label = 'y' + str(i)
            if player_label not in data:
                data[player_label] = [-1 for _ in range(0, max_turns)]

        for turn_id in range(0, max_turns):
            if str(turn_id) in data_frames:
                d_frame = data_frames[str(turn_id)]
                for player_id in d_frame.drones:
                    p_drones = d_frame.drones[player_id]
                    data['y' + player_id][int(turn_id)] = len(p_drones)
                    # TODO plot data after game
        self.__plot_data(data)
