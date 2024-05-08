from OpenGL.GL import *
import numpy as np

from src.matrixes import matrix_model, matrix_view, matrix_projection
from src.util.loader import ModelLoader, TextureLoader
from src.util.path import PathHelper
from src.texture import TextureId


class Cube:
    def __init__(self, program, coord: list, texture_obj_path: str, texture_id: TextureId):
        self.program = program
        self.coord = coord

        self.loc_vertexes = glGetAttribLocation(self.program, "position")
        self.loc_texture = glGetAttribLocation(self.program, "texture_coord")
        self.loc_color = glGetUniformLocation(self.program, "color")

        # TODO: modularize
        # TODO: take model and texture load from Cube class and put somewhere else. Only needs to execute once per object class
        self.model_filename = PathHelper.get_abs_path(texture_obj_path)
        self.model = ModelLoader.load_from_file(self.model_filename)

        self.texture_coord = []
        self.vertexes_coord = []
        self.configure_coord()

        self.texture = np.zeros(len(self.texture_coord), [("position", np.float32, 2)])
        self.texture['position'] = self.texture_coord
        self.texture_id = texture_id

        self.vertexes = np.zeros(len(self.vertexes_coord), [("position", np.float32, 3)])
        self.vertexes['position'] = self.vertexes_coord

    def __send_array_to_gpu(self, array, gpu_var_name, data_dimension):
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glBufferData(GL_ARRAY_BUFFER, array.nbytes, array, GL_DYNAMIC_DRAW)

        stride = array.strides[0]
        offset = ctypes.c_void_p(0)

        loc_vertexes = glGetAttribLocation(self.program, gpu_var_name)
        glEnableVertexAttribArray(loc_vertexes)
        glVertexAttribPointer(loc_vertexes, data_dimension, GL_FLOAT, False, stride, offset)

    def send_data_to_gpu(self):
        self.__send_array_to_gpu(self.vertexes, "position", 3)
        self.__send_array_to_gpu(self.texture, "texture_coord", 2)

    def configure_coord(self):
        for face in self.model['faces']:
            for vertex_id in face[0]:
                self.vertexes_coord.append(self.model['vertices'][vertex_id - 1])
            for texture_id in face[1]:
                self.texture_coord.append(self.model['texture'][texture_id - 1])

    def __send_matrix_to_gpu(self, matrix, gpu_var_name):
        loc_matrix = glGetUniformLocation(self.program, gpu_var_name)
        glUniformMatrix4fv(loc_matrix, 1, GL_TRUE, matrix)

    def render(self, window_height, window_width, camera):
        # cálculo das matrizes do objeto e envio para a gpu
        mat_model = matrix_model(coord=self.coord)
        self.__send_matrix_to_gpu(mat_model, "model")

        mat_view = matrix_view(camera.position, camera.target, camera.up)
        self.__send_matrix_to_gpu(mat_view, "view")

        mat_projection = matrix_projection(window_height, window_width, camera.fov, camera.near, camera.far)
        self.__send_matrix_to_gpu(mat_projection, "projection")

        # renderizando a cada três vértices (triângulos) aplicando texturas
        for i in range(0, len(self.vertexes['position']), 4):
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glDrawArrays(GL_TRIANGLE_STRIP, i, 4)
