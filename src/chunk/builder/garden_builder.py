from src.object import ObjectId
from src.chunk import Chunk


class GardenBuilder:
    @staticmethod
    def build(chunk: Chunk) -> None:
        chunk.put_object((10, 1, 7), ObjectId.FLOWER)
        chunk.put_object((8, 1, 5), ObjectId.FLOWER)
        chunk.put_object((3, 1, 10), ObjectId.FLOWER)
        chunk.put_object((0, 1, 0), ObjectId.FLOWER)
        chunk.put_object((2, 1, 12), ObjectId.FLOWER)
        chunk.put_object((9, 1, 8), ObjectId.FLOWER)
        chunk.put_object((11, 1, 3), ObjectId.FLOWER)
        chunk.put_object((13, 1, 6), ObjectId.FLOWER)
        chunk.put_object((5, 1, 11), ObjectId.FLOWER)
        chunk.put_object((3, 1, 15), ObjectId.FLOWER)
        chunk.put_object((6, 1, 14), ObjectId.FLOWER)
        chunk.put_object((11, 1, 10), ObjectId.TORCH)
        chunk.put_object((0, 1, 15), ObjectId.TORCH)
