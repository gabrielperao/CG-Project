from enum import Enum


class CameraMovement(int, Enum):
    STOP = 0
    FRONT = 1
    BACK = 2
    LEFT = 3
    RIGHT = 4
    UP = 5
    DOWN = 6

    def __int__(self):
        return self.value
