from OpenGL.GL import *
import numpy as np

from src.matrixes import matrix_model, matrix_view, matrix_projection
from src.util.loader import ModelLoader
from src.util.path import PathHelper


class GameObject:
    def __init__(self, program, coord: list, texture_id, model_filename: str):
        self.program = program
        self.coord = coord

        self.loc_vertexes = glGetAttribLocation(self.program, "position")
        self.loc_texture = glGetAttribLocation(self.program, "texture_coord")
        self.loc_color = glGetUniformLocation(self.program, "color")

        self.model_filename = model_filename
        self.model = ModelLoader.load_from_file(self.model_filename)

        self.texture_coords = []
        self.vertexes_coords = []
        self.configure_coords()

        self.texture = np.zeros(len(self.texture_coords), [("position", np.float32, 2)])
        self.texture['position'] = self.texture_coords
        self.texture_id = texture_id

        self.vertexes = np.zeros(len(self.vertexes_coords), [("position", np.float32, 3)])
        self.vertexes['position'] = self.vertexes_coords

    def send_data_to_gpu(self):
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

    def configure_coords(self):
        for face in self.model['faces']:
            for vertex_id in face[0]:
                self.vertexes_coords.append(self.model['vertices'][vertex_id - 1])
            for texture_id in face[1]:
                self.texture_coords.append(self.model['texture'][texture_id - 1])

    def render(self, window_height, window_width, camera, scale: list = (1.0, 1.0, 1.0),
               rotate: list = (1.0, 0.0, 0.0), angle: float = 0.0):
        # cálculo da matriz model e manda para a GPU
        mat_model = matrix_model(coord=self.coord, scale=scale, rotate=rotate, angle=angle)
        loc_model = glGetUniformLocation(self.program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)

        # cálculo da matriz view e manda para a GPU
        mat_view = matrix_view(camera.position, camera.target, camera.up)
        loc_view = glGetUniformLocation(self.program, "view")
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

        # cálculo da matriz projection e manda para a GPU
        mat_projection = matrix_projection(window_height, window_width, camera.fov, camera.near, camera.far)
        loc_projection = glGetUniformLocation(self.program, "projection")
        glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)

        # renderizando a cada três vértices (triângulos)
        cr = [0, 0.3, 0.3, 0.6, 0.6, 0.9]
        cb = [0, 0, 0.3, 0.3, 0.6, 0.6]
        for i in range(0, len(self.vertexes['position']), 4):
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glDrawArrays(GL_TRIANGLE_STRIP, i, 4)
