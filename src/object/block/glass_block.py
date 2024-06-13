from src.object.block import Block
from src.object import ObjectId
from src.texture import TextureId
from src.manager import GPUDataManager


class GlassBlock(Block):

    TEXTURE_ID: TextureId = TextureId.GLASS_TEXTURE

    def __init__(self, program, index_in_chunk, coord: list, obj_ilum_parameters):
        super().__init__(program, coord, self.TEXTURE_ID, index_in_chunk,
                         GPUDataManager().get_initial_index_for_object_id(ObjectId.GLASS),
                         GPUDataManager().get_size_index_for_object_id(ObjectId.GLASS), obj_ilum_parameters)
