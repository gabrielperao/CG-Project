from enum import Enum


class ObjectId(int, Enum):
    EMPTY = 0
    GRASS = 1
    DIRT = 2
    STONE = 3
    COBBLESTONE = 4
    WOOD = 5
    LEAF = 6
    GLASS = 7

    def __int__(self):
        return self.value
