from OpenGL.GL import *
import glm
import numpy as np
from .camera_movement import CameraMovement
from src.util.helper import GpuDataHelper


class Camera:
    FLOOR_HEIGHT = 1

    def __init__(self, sensibility, step, fov, near, far):
        self.position = glm.vec3(8.0, 4.0, 8.0)
        self.target = glm.vec3(0.0, 0.0, 0.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)

        self.movement = CameraMovement.STOP
        self.vertical_angle = 0
        self.horizontal_angle = np.pi

        self.sensibility = sensibility
        self.fov = fov
        self.step = step
        self.near = near
        self.far = far

    def update_angle_view(self):
        # converte os ângulos para coordenadas esféricas
        self.target.x = self.position.x + np.cos(self.vertical_angle) * np.sin(self.horizontal_angle)
        self.target.y = self.position.y + np.sin(self.vertical_angle)
        self.target.z = self.position.z + np.cos(self.vertical_angle) * np.cos(self.horizontal_angle)

    def __calculate_direction(self):
        direction = np.array([
            self.target.x - self.position.x,
            self.target.y - self.position.y,
            self.target.z - self.position.z,
        ])
        return direction / np.linalg.norm(direction)

    def __calculate_perpendicular_direction(self):
        perpendicular_angle = self.horizontal_angle + np.pi / 2
        return np.array([np.sin(perpendicular_angle), 0.0, np.cos(perpendicular_angle)])

    def __update_position(self, direction):
        self.position.x += self.step * direction[0]
        self.position.y += self.step * direction[1]
        self.position.z += self.step * direction[2]

        # não permite chegar debaixo da terra
        if self.position.y < self.FLOOR_HEIGHT:
            self.position.y = self.FLOOR_HEIGHT

    def __update_target(self, direction):
        self.target.x += self.step * direction[0]
        self.target.y += self.step * direction[1]
        self.target.z += self.step * direction[2]

    def update_position(self):
        direction = np.zeros(3)

        if self.movement == CameraMovement.FRONT:
            direction = self.__calculate_direction()
        elif self.movement == CameraMovement.BACK:
            direction = -1 * self.__calculate_direction()
        elif self.movement == CameraMovement.LEFT:
            direction = self.__calculate_perpendicular_direction()
        elif self.movement == CameraMovement.RIGHT:
            direction = -1 * self.__calculate_perpendicular_direction()
        elif self.movement == CameraMovement.UP:
            direction = np.array([0.0, 1.0, 0.0])
        elif self.movement == CameraMovement.DOWN:
            direction = np.array([0.0, -1.0, 0.0])

        self.__update_position(direction)
        self.__update_target(direction)

    def send_position_gpu(self, program):
        pos = list(self.position)
        GpuDataHelper.send_array3_to_gpu(program, pos, "viewPos")
