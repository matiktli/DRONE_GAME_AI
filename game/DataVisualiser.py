import matplotlib.pyplot as plt
from DataService import GameFrameData


class DataVisualiser():

    def __init__(self):
        pass

    def __get_plot_data_from_data_frame(self, data_frame: GameFrameData):
        return None

    def visualise_from_data(self, data_frames: {}, max_turns=None):
        for i in range(0, max_turns):
            if str(i) in data_frames:
                d_frame = data_frames[str(i)]
                plot_data = self.__get_plot_data_from_data_frame(d_frame)
                # TODO plot data after game
        pass
