from src.chunk import Chunk
from src.chunk.builder import HouseBuilder, TreeBuilder, GardenBuilder
from src.object import ObjectId

import random


class ChunkManager:

    @staticmethod
    def __generate_base_chunk(index_x, index_z, illumination, objs_ilum_parameters):
        chunk = Chunk(index_x, index_z, illumination, objs_ilum_parameters)
        scenary_size: int = 16
        for i in range(scenary_size):
            for j in range(scenary_size):
                chunk.put_object((i, 0, j), ObjectId.GRASS)
        number_of_dirt_blocks_overrides: int = 10
        for _ in range(number_of_dirt_blocks_overrides):
            x = random.randint(0, scenary_size-1)
            y = random.randint(0, scenary_size-1)
            chunk.remove_object((x, 0, y))
            chunk.put_object((x, 0, y), ObjectId.DIRT)
        return chunk

    @classmethod
    def generate_chunk(cls, index_x, index_z, illumination, objs_ilum_parameters) -> Chunk:
        base_chunk = cls.__generate_base_chunk(index_x, index_z, illumination, objs_ilum_parameters)
        HouseBuilder.build(base_chunk, 1, 1, 1)
        TreeBuilder.build(base_chunk, 10, 1, 10)
        GardenBuilder.build(base_chunk, 0, 1, 0)
        base_chunk.put_object((1, 1, 11), ObjectId.SLIME)
        return base_chunk
