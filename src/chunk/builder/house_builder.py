from src.object import ObjectId
from src.chunk import Chunk


class HouseBuilder:

    @staticmethod
    def __build_right_wall(chunk, x, y, z) -> None:
        for i in range(5):
            for j in range(3):
                chunk.put_object((x + i, y + j, z), ObjectId.STONE)

    @staticmethod
    def __build_left_wall(chunk, x, y, z) -> None:
        for i in range(5):
            for j in range(3):
                chunk.put_object((x + i, y + j, z + 4), ObjectId.STONE)

    @staticmethod
    def __build_front_wall(chunk, x, y, z) -> None:
        for i in range(3):
            for j in range(3):
                chunk.put_object((x + 4, y + j, z + 1 + i), ObjectId.STONE)

    @staticmethod
    def __build_back_wall(chunk, x, y, z) -> None:
        for i in range(3):
            for j in range(3):
                chunk.put_object((x, y + j, z + 1 + i), ObjectId.STONE)

    @staticmethod
    def __build_ceiling(chunk, x, y, z) -> None:
        for i in range(3):
            for j in range(3):
                chunk.put_object((x + 1 + i, y + 3, z + 1 + j), ObjectId.COBBLESTONE)

    @staticmethod
    def __build_floor(chunk, x, y, z) -> None:
        for i in range(3):
            for j in range(3):
                chunk.remove_object((x + 1 + i, y - 1, z + 1 + j))
                chunk.put_object((x + 1 + i, y - 1, z + 1 + j), ObjectId.WOOD)
        chunk.remove_object((x + 2, y - 1, z + 4))
        chunk.put_object((x + 2, y - 1, z + 4), ObjectId.WOOD)

    @staticmethod
    def __build_windows(chunk, x, y, z) -> None:
        chunk.remove_object((x, y + 1, z + 2))
        chunk.put_object((x, y + 1, z + 2), ObjectId.GLASS)
        chunk.remove_object((x + 4, y + 1, z + 2))
        chunk.put_object((x + 4, y + 1, z + 2), ObjectId.GLASS)

    @staticmethod
    def __build_door(chunk, x, y, z) -> None:
        chunk.remove_object((x + 2, y, z + 4))
        chunk.remove_object((x + 2, y + 1, z + 4))

    @staticmethod
    def __build_garden(chunk, x, y, z) -> None:
        chunk.put_object((x, y, z + 5), ObjectId.LEAF)
        chunk.put_object((x + 1, y, z + 5), ObjectId.LEAF)
        chunk.put_object((x + 3, y, z + 5), ObjectId.LEAF)
        chunk.put_object((x + 4, y, z + 5), ObjectId.LEAF)

    @staticmethod
    def __build_torches(chunk, x, y, z) -> None:
        chunk.put_object((x + 1, y, z + 1), ObjectId.TORCH)

    @staticmethod
    def __build_bench(chunk, x, y, z) -> None:
        chunk.put_object((x + 3, y, z + 1), ObjectId.COBBLESTONE)
        chunk.put_object((x + 3, y + 1, z + 1), ObjectId.FLOWER)

    @classmethod
    def build(cls, chunk: Chunk, x, y, z) -> None:
        cls.__build_right_wall(chunk, x, y, z)
        cls.__build_left_wall(chunk, x, y, z)
        cls.__build_front_wall(chunk, x, y, z)
        cls.__build_back_wall(chunk, x, y, z)
        cls.__build_ceiling(chunk, x, y, z)
        cls.__build_floor(chunk, x, y, z)
        cls.__build_windows(chunk, x, y, z)
        cls.__build_door(chunk, x, y, z)
        cls.__build_garden(chunk, x, y, z)
        cls.__build_torches(chunk, x, y, z)
        cls.__build_bench(chunk, x, y, z)
