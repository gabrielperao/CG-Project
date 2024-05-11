from src.object import GameObject
from src.texture import TextureId


class Block(GameObject):

    def __init__(self, program, coord: list, texture_id: TextureId,
                 initial_index_for_gpu_data_array: int, max_gpu_data_array_index: int):
        super().__init__(program, coord, texture_id,
                         initial_index_for_gpu_data_array, max_gpu_data_array_index)
