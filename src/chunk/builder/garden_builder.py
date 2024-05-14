from src.object import ObjectId
from src.chunk import Chunk


class GardenBuilder:
    @staticmethod
    def build(chunk: Chunk, x, y, z) -> None:
        chunk.put_object((x + 10, y + 1, z + 7), ObjectId.FLOWER)
        chunk.put_object((x + 8, y + 1, z + 5), ObjectId.FLOWER)
        chunk.put_object((x + 3, y + 1, z + 10), ObjectId.FLOWER)
        chunk.put_object((x + 0, y + 1, z + 0), ObjectId.FLOWER)
        chunk.put_object((x + 2, y + 1, z + 12), ObjectId.FLOWER)
        chunk.put_object((x + 9, y + 1, z + 8), ObjectId.FLOWER)
        chunk.put_object((x + 11, y + 1, z + 3), ObjectId.FLOWER)
        chunk.put_object((x + 13, y + 1, z + 6), ObjectId.FLOWER)
        chunk.put_object((x + 5, y + 1, z + 11), ObjectId.FLOWER)
        chunk.put_object((x + 3, y + 1, z + 15), ObjectId.FLOWER)
        chunk.put_object((x + 6, y + 1, z + 14), ObjectId.FLOWER)
        chunk.put_object((x + 11, y + 1, z + 10), ObjectId.TORCH)
        chunk.put_object((x + 0, y + 1, z + 15), ObjectId.TORCH)
