from src.object import ObjectId
from src.chunk import Chunk


class TreeBuilder:

    @staticmethod
    def __build_trunk(chunk: Chunk, x, y, z):
        for i in range(4):
            chunk.put_object((x, y + i, z), ObjectId.WOOD)

    @classmethod
    def __build_crown(cls, chunk: Chunk, x, y, z):
        cls.__build_crown_base(chunk, x, y, z)
        cls.__build_crown_middle(chunk, x, y, z)
        cls.__build_crown_top(chunk, x, y, z)
        cls.__smoothen_crown_base(chunk, x, y, z)

    @staticmethod
    def __build_crown_base(chunk: Chunk, x, y, z):
        for i in range(5):
            for j in range(5):
                try:
                    chunk.put_object((x - 2 + i, y + 2, z - 2 + j), ObjectId.LEAF)
                except ValueError:
                    continue

    @staticmethod
    def __build_crown_middle(chunk: Chunk, x, y, z):
        for i in range(3):
            for j in range(3):
                try:
                    chunk.put_object((x - 1 + i, y + 3, z - 1 + j), ObjectId.LEAF)
                except ValueError:
                    continue

    @staticmethod
    def __build_crown_top(chunk: Chunk, x, y, z):
        chunk.put_object((x, y + 4, z), ObjectId.LEAF)

    @staticmethod
    def __smoothen_crown_base(chunk: Chunk, x, y, z):
        chunk.remove_object((x - 2, y + 2, z - 2))
        chunk.remove_object((x - 2, y + 2, z + 2))
        chunk.remove_object((x + 2, y + 2, z - 2))
        chunk.remove_object((x + 2, y + 2, z + 2))

    @classmethod
    def build(cls, chunk: Chunk, x, y, z) -> None:
        cls.__build_trunk(chunk, x, y, z)
        cls.__build_crown(chunk, x, y, z)
