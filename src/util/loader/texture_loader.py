from OpenGL.GL import *
from PIL import Image


class TextureLoader:

    @staticmethod
    def __set_texture_parameters(texture_id: int):
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    @staticmethod
    def load_from_file(texture_id: int, filename: str) -> None:
        TextureLoader.__set_texture_parameters(texture_id)
        img = Image.open(filename)
        img_width = img.size[0]
        img_height = img.size[1]
        image_data = img.convert("RGBA").tobytes("raw", "RGBA", 0, -1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img_width, img_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
