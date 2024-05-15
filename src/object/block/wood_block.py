from src.object.block import Block
from src.object import ObjectId
from src.texture import TextureId
from src.manager import GPUDataManager


class WoodBlock(Block):

    TEXTURE_ID: TextureId = TextureId.WOOD_TEXTURE

    def __init__(self, program, index_in_chunk, coord: list):
        super().__init__(program, coord, self.TEXTURE_ID, index_in_chunk,
                         GPUDataManager().get_initial_index_for_object_id(ObjectId.WOOD),
                         GPUDataManager().get_size_index_for_object_id(ObjectId.WOOD))
