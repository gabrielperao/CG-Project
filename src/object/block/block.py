from src.object import GameObject
from src.texture import TextureId


class Block(GameObject):

    def __init__(self, program, coord: list, texture_id: TextureId, model_filename):
        super().__init__(program, coord, texture_id, model_filename)
