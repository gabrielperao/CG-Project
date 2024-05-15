from OpenGL.GL import *

from src.util.helper import MatrixHelper


class GameObject:
    def __init__(self, program, coord: list, texture_id, index_in_chunk: tuple,
                 initial_index_for_gpu_data_array: int, gpu_data_array_size: int):
        self.index_in_chunk = index_in_chunk

        self.program = program
        self.coord = coord
        self.initial_index_for_gpu_data_array = initial_index_for_gpu_data_array
        self.max_gpu_data_array_index = gpu_data_array_size + initial_index_for_gpu_data_array

        self.loc_vertexes = glGetAttribLocation(self.program, "position")
        self.loc_texture = glGetAttribLocation(self.program, "texture_coord")
        self.loc_color = glGetUniformLocation(self.program, "color")

        self.texture_id = texture_id

    def __calculate_gpu_matrix(self, gpu_var_name, matrix_function, *args):
        matrix = matrix_function(*args)
        loc = glGetUniformLocation(self.program, gpu_var_name)
        glUniformMatrix4fv(loc, 1, GL_TRUE, matrix)

    def update_coord(self, new_coord: list):
        self.coord = new_coord

    def render(self, window_height, window_width, camera, scale: list = (1.0, 1.0, 1.0),
               rotate: list = (1.0, 0.0, 0.0), angle: float = 0.0, faces: list = (True, True) * 3):
        # cálculo das matrizes do objeto e envio para a GPU
        self.__calculate_gpu_matrix("model", MatrixHelper.matrix_model, self.coord, scale, rotate, angle)
        self.__calculate_gpu_matrix("view", MatrixHelper.matrix_view, camera.position, camera.target, camera.up)
        self.__calculate_gpu_matrix("projection", MatrixHelper.matrix_projection, window_height, window_width,
                                    camera.fov, camera.near, camera.far)

        # renderizando a cada três vértices (triângulos) das faces desejadas
        for i in range(self.initial_index_for_gpu_data_array, self.max_gpu_data_array_index, 4):
            if faces[(i - self.initial_index_for_gpu_data_array) // 4]:
                glBindTexture(GL_TEXTURE_2D, self.texture_id)
                glDrawArrays(GL_TRIANGLE_STRIP, i, 4)
