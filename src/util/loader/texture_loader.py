from OpenGL.GL import *
from PIL import Image

from src.texture import TextureId
from src.util.path import PathHelper


class TextureLoader:

    BLOCK_TEXTURE_FILENAMES = {
        TextureId.GRASS_TEXTURE: "grass_block_texture.png",
        TextureId.DIRT_TEXTURE: "dirt_block_texture.png",
        TextureId.STONE_TEXTURE: "stone_block_texture.png",
        TextureId.COBBLESTONE_TEXTURE: "cobblestone_block_texture.png",
        TextureId.GLASS_TEXTURE: "glass_block_texture.png",
        TextureId.WOOD_TEXTURE: "wood_block_texture.png",
        TextureId.LEAF_TEXTURE: "leaf_block_texture.png"
    }

    MISC_TEXTURE_FILENAMES = {
        TextureId.CHICKEN_TEXTURE: "chicken_misc_texture.png",
        TextureId.TORCH_TEXTURE: "torch_misc_texture.png",
        TextureId.FLOWER_TEXTURE: "flower_misc_texture.png"
    }

    @classmethod
    def load_all_block_textures(cls):
        for texture_id, filename in cls.BLOCK_TEXTURE_FILENAMES.items():
            path = PathHelper.get_abs_path(f"src\\texture\\block\\{filename}")
            cls.__load_from_file(texture_id, path)

    @classmethod
    def load_all_misc_textures(cls):
        for texture_id, filename in cls.MISC_TEXTURE_FILENAMES.items():
            path = PathHelper.get_abs_path(f"src\\texture\\misc\\{filename}")
            cls.__load_from_file(texture_id, path)

    @classmethod
    def __load_from_file(cls, texture_id: int, path: str) -> None:
        cls.__set_texture_parameters(texture_id)
        img = Image.open(path)
        img_width = img.size[0]
        img_height = img.size[1]
        image_data = img.convert("RGBA").tobytes("raw", "RGBA", 0, -1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img_width, img_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    @staticmethod
    def __set_texture_parameters(texture_id: int):
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
