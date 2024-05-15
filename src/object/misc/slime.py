import numpy as np

from src.object import GameEntity
from src.object import ObjectId
from src.texture import TextureId
from src.manager import GPUDataManager


class Slime(GameEntity):
    TEXTURE_ID: TextureId = TextureId.SLIME_TEXTURE

    def __init__(self, program, coord: list):
        super().__init__(program, coord, [1.0, 1.0, 1.0], [0.0, 1.0, 0.0], 0.0, self.TEXTURE_ID,
                         GPUDataManager().get_initial_index_for_object_id(ObjectId.SLIME),
                         GPUDataManager().get_size_index_for_object_id(ObjectId.SLIME))

    @staticmethod
    def __angle_velocity(time):
        return 1.5

    @staticmethod
    def __movement_velocity(time):
        return 0.05

    @staticmethod
    def __scale_velocity(time, cycle_length):
        return [0.0, 0.05 * np.cos(2 * np.pi * time / cycle_length), 0.0]

    @staticmethod
    def __height_movement_velocity(time, cycle_length):
        return [0.0, 0.5 * np.sin(2 * np.pi * time / cycle_length), 0.0]

    def update(self, time):
        if time < 0:
            raise ValueError('Parâmetro deve ser não negativo')

        self.front_move(Slime.__movement_velocity(time))
        self.update_angle(Slime.__angle_velocity(time))
        self.update_scale(Slime.__scale_velocity(time, 30))
        self.update_position(Slime.__height_movement_velocity(time, 30))
