from src.object.block import Block
from src.texture import TextureId
from src.util.path import PathHelper


class StoneBlock(Block):

    TEXTURE_ID: TextureId = TextureId.STONE_TEXTURE
    MODEL_FILENAME: str = PathHelper.get_abs_path("src\\model\\block\\simple_block.obj")

    def __init__(self, program, coord: list):
        super().__init__(program, coord, self.TEXTURE_ID, self.MODEL_FILENAME)
