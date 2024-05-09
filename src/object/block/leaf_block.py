from src.object.block import Block
from src.texture import TextureId


class LeafBlock(Block):

    TEXTURE_ID: TextureId = TextureId.LEAF_TEXTURE

    def __init__(self, program, coord: list):
        super().__init__(program, coord, self.TEXTURE_ID)
