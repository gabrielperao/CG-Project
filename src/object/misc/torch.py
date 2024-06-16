from src.object import GameObject
from src.object import ObjectId
from src.texture import TextureId
from src.manager import GPUDataManager


class Torch(GameObject):
    TEXTURE_ID: TextureId = TextureId.TORCH_TEXTURE

    def __init__(self, program, index_in_chunk, coord: list, illumination):
        super().__init__(program, coord, self.TEXTURE_ID, index_in_chunk,
                         GPUDataManager().get_initial_index_for_object_id(ObjectId.TORCH),
                         GPUDataManager().get_size_index_for_object_id(ObjectId.TORCH))

        super().set_surface_illumination_proprieties(1.0, 1.0, 1.0, 5)

        # inicializa a iluminação do bloco
        ilum_coord = list(coord.copy())
        ilum_coord[1] += 1
        illumination.add_source(ilum_coord, [1.0, 1.0, 0.65])
