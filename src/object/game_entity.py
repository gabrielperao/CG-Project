import numpy as np
import math
from .game_object import GameObject


class GameEntity(GameObject):
    def __init__(self, program, coord: list, scale: list, rotate: list, angle: float,
                 texture_id, initial_index_for_gpu_data_array: int, gpu_data_array_size: int):
        self.scale = np.array(scale)
        self.rotate = rotate
        self.angle = angle
        super().__init__(program, coord, texture_id, (0, 0, 0), initial_index_for_gpu_data_array, gpu_data_array_size)

    def update_position(self, velocity: list):
        self.coord += velocity

    def front_move(self, velocity: float):
        self.coord[0] += np.sin(math.radians(self.angle)) * velocity
        self.coord[2] += np.cos(math.radians(self.angle)) * velocity

    def update_angle(self, velocity: float):
        self.angle = (self.angle + velocity) % 360

    def update_scale(self, rate: list):
        self.scale += rate

    def render(self, window_height, window_width, camera, scale: list = (1.0, 1.0, 1.0),
               rotate: list = (1.0, 0.0, 0.0), angle: float = 0.0, faces: list = (True, True) * 3):
        raise NotImplementedError("Entidades devem utilizar o método 'dynamic_render'")

    def dynamic_render(self, window_height, window_width, camera):
        super().render(window_height, window_width, camera, list(self.scale), self.rotate, self.angle)
