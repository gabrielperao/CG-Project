import glm
import numpy as np


class Camera:
    def __init__(self, sensibility, step, fov, near, far):
        self.position = glm.vec3(0.0, 0.0, 4.0)
        self.target = glm.vec3(0.0, 0.0, 0.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)
        self.velocity = np.zeros(3)

        self.sensibility = sensibility
        self.fov = fov
        self.step = step
        self.near = near
        self.far = far

    def direction(self):
        direction = np.array([
            self.target.x - self.position.x,
            self.target.y - self.position.y,
            self.target.z - self.position.z,
        ])
        return direction / np.linalg.norm(direction)

    def perpendicular_direction(self):
        direction_plane = np.array([
            self.up.x,
            self.up.y,
            self.up.z,
        ])
        return np.cross(self.direction(), direction_plane)

    def update_position(self):
        self.position.x += self.step * self.velocity[0]
        self.position.y += self.step * self.velocity[1]
        self.position.z += self.step * self.velocity[2]

    def update_targets(self):
        self.target.x += self.step * self.velocity[0]
        self.target.y += self.step * self.velocity[1]
        self.target.z += self.step * self.velocity[2]
