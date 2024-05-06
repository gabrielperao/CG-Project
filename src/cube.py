from OpenGL.GL import *
import numpy as np

from matrixes import matrix_model, matrix_view, matrix_projection


class Cube:
    def __init__(self, program, coord):
        self.program = program
        self.coord = coord

        self.loc_vertexes = glGetAttribLocation(self.program, "position")
        self.loc_color = glGetUniformLocation(self.program, "color")

        self.vertexes = np.zeros(24, [("position", np.float32, 3)])
        self.vertexes['position'] = [
            # Face 1 do Cubo (vértices do quadrado)
            (-0.2, -0.2, +0.2),
            (+0.2, -0.2, +0.2),
            (-0.2, +0.2, +0.2),
            (+0.2, +0.2, +0.2),

            # Face 2 do Cubo
            (+0.2, -0.2, +0.2),
            (+0.2, -0.2, -0.2),
            (+0.2, +0.2, +0.2),
            (+0.2, +0.2, -0.2),

            # Face 3 do Cubo
            (+0.2, -0.2, -0.2),
            (-0.2, -0.2, -0.2),
            (+0.2, +0.2, -0.2),
            (-0.2, +0.2, -0.2),

            # Face 4 do Cubo
            (-0.2, -0.2, -0.2),
            (-0.2, -0.2, +0.2),
            (-0.2, +0.2, -0.2),
            (-0.2, +0.2, +0.2),

            # Face 5 do Cubo
            (-0.2, -0.2, -0.2),
            (+0.2, -0.2, -0.2),
            (-0.2, -0.2, +0.2),
            (+0.2, -0.2, +0.2),

            # Face 6 do Cubo
            (-0.2, +0.2, +0.2),
            (+0.2, +0.2, +0.2),
            (-0.2, +0.2, -0.2),
            (+0.2, +0.2, -0.2)
        ]

    def send_vertexes_to_gpu(self):
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)

        glBufferData(GL_ARRAY_BUFFER, self.vertexes.nbytes, self.vertexes, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)

        stride = self.vertexes.strides[0]
        offset = ctypes.c_void_p(0)

        glEnableVertexAttribArray(self.loc_vertexes)
        glVertexAttribPointer(self.loc_vertexes, 3, GL_FLOAT, GL_FALSE, stride, offset)

    def render(self, window_height, window_width, camera):
        # cálculo da matriz model e manda para a GPU
        mat_model = matrix_model(self.coord[0], self.coord[1], self.coord[2])
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
            glUniform4f(self.loc_color, cr[i // 4], 1.0, cb[i // 4], 1.0)  # definindo uma cor
            glDrawArrays(GL_TRIANGLE_STRIP, i, 4)
