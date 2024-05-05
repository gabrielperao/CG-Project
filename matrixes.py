import glm
import numpy as np
import math


def matrix_model(coord_x, coord_y, coord_z):
    matrix_transform = glm.mat4(1.0)  # instanciando uma matriz identidade
    matrix_transform = glm.rotate(matrix_transform, math.radians(180), glm.vec3(0.0, 0.0, 1.0))
    matrix_transform = glm.translate(matrix_transform, glm.vec3(coord_x, coord_y, coord_z))
    matrix_transform = np.array(matrix_transform)
    return matrix_transform


def matrix_view(camera_position, camera_target, camera_up):
    mat_view = glm.lookAt(camera_position, camera_target, camera_up)
    mat_view = np.array(mat_view)
    return mat_view


def matrix_projection(height, width, fov, near, far):
    mat_projection = glm.perspective(glm.radians(fov), width / height, near, far)
    mat_projection = np.array(mat_projection).T
    mat_projection[2, 2] = mat_projection[2, 2] * -1
    return mat_projection
