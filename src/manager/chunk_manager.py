from src.chunk import Chunk
from src.chunk.builder import HouseBuilder, TreeBuilder, GardenBuilder
from src.object import ObjectId


class ChunkManager:

    @staticmethod
    def __generate_base_chunk(index_x, index_z, max_gpu_data_array_index):
        chunk = Chunk(index_x, index_z, max_gpu_data_array_index)
        for i in range(16):
            for j in range(16):
                chunk.put_object((i, 0, j), ObjectId.GRASS)
        return chunk

    @classmethod
    def generate_chunk(cls, index_x, index_z, max_gpu_data_array_index) -> Chunk:
        base_chunk = cls.__generate_base_chunk(index_x, index_z, max_gpu_data_array_index)
        HouseBuilder.build(base_chunk, 1, 1, 1)
        TreeBuilder.build(base_chunk, 10, 1, 10)
        GardenBuilder.build(base_chunk)
        base_chunk.put_object((1, 1, 11), ObjectId.SLIME)
        return base_chunk
