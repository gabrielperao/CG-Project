import glm
import numpy as np
import math


def matrix_model(coord=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0), rotate=(1.0, 0.0, 0.0), angle=0.0):
    matrix_transform = glm.mat4(1.0)  # instanciando uma matriz identidade
    matrix_transform = glm.scale(matrix_transform, glm.vec3(scale[0], scale[1], scale[2]))
    matrix_transform = glm.rotate(matrix_transform, math.radians(angle), glm.vec3(rotate[0], rotate[1], rotate[2]))
    matrix_transform = glm.translate(matrix_transform, glm.vec3(coord[0], coord[1], coord[2]))
    matrix_transform = np.array(matrix_transform)
    return matrix_transform


def matrix_view(camera_position, camera_target, camera_up):
    mat_view = glm.lookAt(camera_position, camera_target, camera_up)
    mat_view = np.array(mat_view)
    return mat_view


def matrix_projection(height, width, fov, near, far):
    mat_projection = glm.perspective(glm.radians(fov), width / height, near, far)
    mat_projection = np.array(mat_projection)
    return mat_projection
