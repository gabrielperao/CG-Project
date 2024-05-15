from src.object import GameObject
from src.object import ObjectId
from src.texture import TextureId
from src.manager import GPUDataManager


class Flower(GameObject):
    TEXTURE_ID: TextureId = TextureId.FLOWER_TEXTURE

    def __init__(self, program, index_in_chunk, coord: list):
        super().__init__(program, coord, self.TEXTURE_ID, index_in_chunk,
                         GPUDataManager().get_initial_index_for_object_id(ObjectId.FLOWER),
                         GPUDataManager().get_size_index_for_object_id(ObjectId.FLOWER))
