from src.object import GameObject
from src.texture import TextureId


class Block(GameObject):

    def __init__(self, program, coord: list, texture_id: TextureId, index_in_chunk,
                 initial_index_for_gpu_data_array: int, max_gpu_data_array_index: int, obj_ilum_parameters: dict):
        super().__init__(program, coord, texture_id, index_in_chunk,
                         initial_index_for_gpu_data_array, max_gpu_data_array_index)

        super().set_surface_illumination_proprieties(obj_ilum_parameters['ka'], obj_ilum_parameters['kd'],
                                                     obj_ilum_parameters['ks'], obj_ilum_parameters['ns'])
