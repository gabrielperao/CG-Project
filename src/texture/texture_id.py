from enum import Enum


class TextureId(int, Enum):
    GRASS_TEXTURE = 0

    def __int__(self):
        return self.value
