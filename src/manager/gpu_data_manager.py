from OpenGL.GL import *
import numpy as np

from src.util.helper import PathHelper
from src.util.helper import GpuDataHelper
from src.util.loader import ModelLoader
from src.util import singleton
from src.object import ObjectId


@singleton
class GPUDataManager:

    def __init__(self, program):
        self.program = program
        self.texture = []
        self.vertexes = []
        self.normals = []
        self.initial_indexes = {}
        self.size_indexes = {}

    def get_initial_index_for_object_id(self, object_id: ObjectId):
        return self.initial_indexes[object_id]

    def get_size_index_for_object_id(self, object_id: ObjectId):
        return self.size_indexes[object_id]

    def __get_data_array_len(self) -> int:
        return len(self.vertexes)

    def __add_vertex_coord(self, coord):
        self.vertexes.append(coord)

    def __add_texture_coord(self, coord):
        self.texture.append(coord)

    def __add_normal_coord(self, coord):
        self.normals.append(coord)

    def __configure_coords(self):
        filenames = {
            ObjectId.GRASS: PathHelper.get_abs_path("src\\model\\block\\grass_block.obj"),
            ObjectId.STONE: PathHelper.get_abs_path("src\\model\\block\\simple_block.obj"),
            ObjectId.COBBLESTONE: PathHelper.get_abs_path("src\\model\\block\\simple_block.obj"),
            ObjectId.DIRT: PathHelper.get_abs_path("src\\model\\block\\simple_block.obj"),
            ObjectId.GLASS: PathHelper.get_abs_path("src\\model\\block\\simple_block.obj"),
            ObjectId.LEAF: PathHelper.get_abs_path("src\\model\\block\\simple_block.obj"),
            ObjectId.WOOD: PathHelper.get_abs_path("src\\model\\block\\wood_block.obj"),
            ObjectId.TORCH: PathHelper.get_abs_path("src\\model\\misc\\torch.obj"),
            ObjectId.FLOWER: PathHelper.get_abs_path("src\\model\\misc\\flower.obj"),
            ObjectId.SLIME: PathHelper.get_abs_path("src\\model\\block\\simple_block.obj"),
            ObjectId.SKYBOX: PathHelper.get_abs_path("src\\model\\misc\\skybox.obj")
        }

        for object_id in filenames.keys():
            model = ModelLoader.load_from_file(filenames[object_id])
            self.initial_indexes[object_id] = self.__get_data_array_len()
            for face in model['faces']:
                for vertex_id in face[0]:
                    self.__add_vertex_coord(model['vertices'][vertex_id - 1])
                for texture_id in face[1]:
                    self.__add_texture_coord(model['texture'][texture_id - 1])
                for normal_id in face[2]:
                    self.__add_normal_coord(model['normals'][normal_id - 1])

            self.size_indexes[object_id] = self.__get_data_array_len() - self.initial_indexes[object_id]

    @staticmethod
    def __setup_coords(array, dim):
        modified_array = np.zeros(len(array), [("position", np.float32, dim)])
        modified_array['position'] = array.copy()
        return modified_array

    def __send_data_to_gpu(self):
        buffer = glGenBuffers(3)
        GpuDataHelper.send_array_to_gpu(self.program, self.vertexes, buffer[0], 3, "position")
        GpuDataHelper.send_array_to_gpu(self.program, self.texture, buffer[1], 2, "texture_coord")
        GpuDataHelper.send_array_to_gpu(self.program, self.normals, buffer[2], 3, "normals")

    def configure(self):
        self.__configure_coords()
        self.vertexes = self.__setup_coords(self.vertexes, 3)
        self.texture = self.__setup_coords(self.texture, 2)
        self.normals = self.__setup_coords(self.normals, 3)
        self.__send_data_to_gpu()
