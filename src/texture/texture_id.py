from enum import Enum


class TextureId(int, Enum):
    GRASS_TEXTURE = 0
    DIRT_TEXTURE = 1
    STONE_TEXTURE = 2
    COBBLESTONE_TEXTURE = 3
    GLASS_TEXTURE = 4
    WOOD_TEXTURE = 5
    LEAF_TEXTURE = 6
    SLIME_TEXTURE = 7
    TORCH_TEXTURE = 8
    FLOWER_TEXTURE = 9
    SKYBOX_TEXTURE = 10

    def __int__(self):
        return self.value
