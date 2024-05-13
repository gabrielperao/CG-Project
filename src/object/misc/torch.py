from src.object import GameObject
from src.object import ObjectId
from src.texture import TextureId
from src.manager import GPUDataManager


class Torch(GameObject):
    TEXTURE_ID: TextureId = TextureId.TORCH_TEXTURE

    def __init__(self, program, coord: list, max_gpu_data_array_index: int):
        super().__init__(program, coord, self.TEXTURE_ID,
                         GPUDataManager().get_initial_index_for_object_id(ObjectId.TORCH),
                         max_gpu_data_array_index)

    # TODO: se a tocha puder ficar grudada na parede e inclinada, então arrumar aqui
    def render_x_rotated(self, window_height, window_width, camera, direction: int = 1, faces: list = (True, True) * 3):
        if direction != 1 and direction != -1:
            raise ValueError("Direção deve ser 1 ou -1 apenas")

        self.coord += direction * [0.2, 0.0, 0.0]
        super().render(window_height, window_width, camera, rotate=[direction, 0, 0], angle=45.0, faces=faces)

    def render_z_rotated(self, window_height, window_width, camera, direction: int = 1, faces: list = (True, True) * 3):
        if direction != 1 and direction != -1:
            raise ValueError("Direção deve ser 1 ou -1 apenas")

        self.coord += direction * [0.0, 0.0, 0.2]
        super().render(window_height, window_width, camera, rotate=[direction, 0, 0], angle=45.0, faces=faces)
