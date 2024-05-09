from src.object.block import Block
from src.texture import TextureId


class GrassBlock(Block):

    TEXTURE_ID: TextureId = TextureId.GRASS_TEXTURE

    def __init__(self, program, coord: list):
        print(self.TEXTURE_ID)
        super().__init__(program, coord, self.TEXTURE_ID)
