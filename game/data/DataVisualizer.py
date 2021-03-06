from .DataService import GameFrameData, DecissionData
import matplotlib.pyplot as plt
import pandas as pd
import cv2
import numpy as np
import time
import imageio


class DataVisualizer():

    BG_COLOR = (0, 0, 0)
    MATRIX_COLOR = (255, 255, 255)
    PLAYER_COLOR_POOL = [
        [(255, 0, 0), 'red'],
        [(0, 255, 0), 'green'],
        [(0, 0, 255), 'blue'],
        [(255, 255, 0), 'yellow'],
        [(255, 0, 255), 'purple'],
        [(255, 128, 0), 'orange']
    ]

    def __init__(self, game_id, is_display):
        self.is_display = is_display
        self.game_id = game_id

    def __add_matrix_to_img(self, img, cell_size, window_size):
        # Adding vertical lines
        for x in range(0, window_size[0], int(cell_size[0])):
            img = cv2.line(
                img, (x, 0), (x, window_size[1]), DataVisualizer.MATRIX_COLOR, 1)
        # Adding horizontal lines
        for y in range(0, window_size[1], int(cell_size[1])):
            img = cv2.line(
                img, (0, y), (window_size[0], y), DataVisualizer.MATRIX_COLOR, 1)
        return img

    def __add_cell_data_to_img(self, img, cell, cell_size: tuple):
        cell_start_point_on_img = (
            (cell.position[0] * int(cell_size[0])),
            (cell.position[1] * int(cell_size[1]))
        )
        cell_center_on_img = (
            (cell_start_point_on_img[0] + int(cell_size[0]/2)),
            (cell_start_point_on_img[1] + int(cell_size[1]/2))
        )
        drones = cell.get_drones()
        if not drones:
            return img

        for p_id in drones:
            p_drones = drones[p_id]
            img = cv2.circle(img, cell_center_on_img, len(p_drones) * 10,
                             DataVisualizer.PLAYER_COLOR_POOL[int(p_id)][0], len(p_drones) * 4)
            img = cv2.putText(img, str(len(p_drones)), cell_center_on_img,
                              cv2.FONT_HERSHEY_SIMPLEX, 1, DataVisualizer.PLAYER_COLOR_POOL[int(p_id)][0])
        return img

    def get_image_from_game_frame_data(self, game_frame_data: GameFrameData, cell_size: tuple, window_size: tuple):
        # Initialise nee image
        img = np.zeros((window_size[0], window_size[1], 3), np.uint8)
        # Draw skeleton of cells
        self.__add_matrix_to_img(img, cell_size, window_size)
        # Populate each cell
        for cell in game_frame_data.grid.ravel():
            self.__add_cell_data_to_img(img, cell, cell_size)
        return img

    def replay_game(self, game_frames_data, decissions_data, delay_ms=100):
        grid_size = game_frames_data['0'].grid_size
        window_size = (800, 800)
        cell_visual_size = (
            window_size[0] / grid_size[0], window_size[1] / grid_size[1])

        frame_images = []
        for turn_id in game_frames_data:
            game_frame_data = game_frames_data[str(turn_id)]
            img = self.get_image_from_game_frame_data(
                game_frame_data, cell_visual_size, window_size)
            frame_images.append(img)

        if self.is_display:
            for i, img_f in enumerate(frame_images):
                cv2.imshow(f'GAME_REPLAY_{self.game_id}', img_f)
                cv2.waitKey(delay_ms)
            cv2.destroyAllWindows()
        return frame_images

    def save_gif(self, frame_images, path):
        imageio.mimsave(path, frame_images)

    def __plot_data(self, data):
        df = pd.DataFrame(data)
        for i, label in enumerate(data):
            if 'y' in label:
                plt.plot('x', label, data=df,
                         color=DataVisualizer.PLAYER_COLOR_POOL[int(label.replace('y', '')) % (len(DataVisualizer.PLAYER_COLOR_POOL))][1], label=label.replace('y', 'Bot: '), linewidth=2)
        plt.title(
            f'Simulation with: {len(data)-1} bots making random decissions')
        plt.legend()

        if self.is_display:
            plt.show()

        return plt

    def plot_from_data(self, data_frames: {}, max_turns=None, init_players=None):
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
        return self.__plot_data(data)

    def save_plot(self, plt, path):
        plt.savefig(path)
