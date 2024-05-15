from OpenGL.GL import *
import numpy as np

from src.util.helper import PathHelper
from src.util.loader import ModelLoader
from src.util import singleton
from src.object import ObjectId


@singleton
class GPUDataManager:

    def __init__(self, program):
        self.program = program
        self.texture_coords = []
        self.vertexes_coords = []
        self.vertexes = None
        self.texture = None
        self.initial_indexes = {}
        self.size_indexes = {}

    def get_initial_index_for_object_id(self, object_id: ObjectId):
        return self.initial_indexes[object_id]

    def get_size_index_for_object_id(self, object_id: ObjectId):
        return self.size_indexes[object_id]

    def __get_data_array_len(self) -> int:
        return len(self.vertexes_coords)

    def __add_vertex_coord(self, coord):
        self.vertexes_coords.append(coord)

    def __add_texture_coord(self, coord):
        self.texture_coords.append(coord)

    def configure(self):
        self.__configure_coords()
        self.__setup_vertexes_and_texture()
        self.__send_data_to_gpu()

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

            self.size_indexes[object_id] = self.__get_data_array_len() - self.initial_indexes[object_id]

    def __setup_vertexes_and_texture(self):
        self.vertexes = np.zeros(len(self.vertexes_coords), [("position", np.float32, 3)])
        self.vertexes['position'] = self.vertexes_coords
        self.texture = np.zeros(len(self.texture_coords), [("position", np.float32, 2)])
        self.texture['position'] = self.texture_coords

    def __send_data_to_gpu(self):
        buffer = glGenBuffers(2)
        self.__send_vertexes_to_gpu(buffer)
        self.__send_texture_to_gpu(buffer)

    def __send_vertexes_to_gpu(self, buffer):
        glBindBuffer(GL_ARRAY_BUFFER, buffer[0])
        glBufferData(GL_ARRAY_BUFFER, self.vertexes.nbytes, self.vertexes, GL_DYNAMIC_DRAW)

        stride = self.vertexes.strides[0]
        offset = ctypes.c_void_p(0)

        loc_vertexes = glGetAttribLocation(self.program, "position")
        glEnableVertexAttribArray(loc_vertexes)
        glVertexAttribPointer(loc_vertexes, 3, GL_FLOAT, False, stride, offset)

    def __send_texture_to_gpu(self, buffer):
        glBindBuffer(GL_ARRAY_BUFFER, buffer[1])
        glBufferData(GL_ARRAY_BUFFER, self.texture.nbytes, self.texture, GL_DYNAMIC_DRAW)

        stride = self.texture.strides[0]
        offset = ctypes.c_void_p(0)

        loc_texture = glGetAttribLocation(self.program, "texture_coord")
        glEnableVertexAttribArray(loc_texture)
        glVertexAttribPointer(loc_texture, 2, GL_FLOAT, False, stride, offset)
