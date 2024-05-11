from src.object.block import Block
from src.object import ObjectId
from src.texture import TextureId
from src.manager import GPUDataManager


class GrassBlock(Block):

    TEXTURE_ID: TextureId = TextureId.GRASS_TEXTURE

    def __init__(self, program, coord: list, max_gpu_data_array_index: int):
        super().__init__(program, coord, self.TEXTURE_ID,
                         GPUDataManager().get_initial_index_for_object_id(ObjectId.GRASS),
                         max_gpu_data_array_index)
