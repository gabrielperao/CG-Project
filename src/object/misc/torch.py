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
