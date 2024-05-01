from PIL import Image, ImageDraw
from IPython.display import display
import random


class Triangle:

    def __init__(self, vv: list):
        self.v1: tuple = vv[0],
        self.v2: tuple = vv[1],
        self.v3: tuple = vv[2]

    def draw(self):
        image = Image.new('RGB', (500, 500))
        draw = ImageDraw.Draw(image)
        draw.polygon([self.v1, self.v2, self.v3], fill=(0, 0, 0))
        display(image)


if __name__ == "__main__":
    triangle = Triangle([
        (random.randint(0, 500), random.randint(0, 500)),
        (random.randint(0, 500), random.randint(0, 500)),
        (random.randint(0, 500), random.randint(0, 500))
    ])
    triangle.draw()
