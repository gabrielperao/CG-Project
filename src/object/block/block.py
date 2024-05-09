from src.object import GameObject
from src.texture import TextureId
from src.util.path import PathHelper


class Block(GameObject):

    BLOCK_MODEL_FILENAME: str = PathHelper.get_abs_path("src\\model\\block\\block.obj")

    def __init__(self, program, coord: list, texture_id: TextureId):
        super().__init__(program, coord, texture_id, self.BLOCK_MODEL_FILENAME)
