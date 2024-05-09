from src.object.block import Block
from src.texture import TextureId


class CobblestoneBlock(Block):

    TEXTURE_ID: TextureId = TextureId.COBBLESTONE_TEXTURE

    def __init__(self, program, coord: list):
        super().__init__(program, coord, self.TEXTURE_ID)
