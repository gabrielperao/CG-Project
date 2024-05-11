from OpenGL.GL import *

from src.matrixes import matrix_model, matrix_view, matrix_projection


class GameObject:
    def __init__(self, program, coord: list, texture_id,
                 initial_index_for_gpu_data_array: int, max_gpu_data_array_index: int):
        self.program = program
        self.coord = coord
        self.initial_index_for_gpu_data_array = initial_index_for_gpu_data_array
        self.max_gpu_data_array_index = max_gpu_data_array_index

        self.loc_vertexes = glGetAttribLocation(self.program, "position")
        self.loc_texture = glGetAttribLocation(self.program, "texture_coord")
        self.loc_color = glGetUniformLocation(self.program, "color")

        self.texture_id = texture_id

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
        for i in range(self.initial_index_for_gpu_data_array, self.max_gpu_data_array_index, 4):
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glDrawArrays(GL_TRIANGLE_STRIP, i, 4)
