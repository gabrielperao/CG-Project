from src.util import singleton
from src.object import GameObject, ObjectId
from src.manager import GPUDataManager
from src.texture import TextureId


@singleton
class SkyBox(GameObject):

    def __init__(self, program, index, coord: list):
        TEXTURE_ID: TextureId = TextureId.SKYBOX_TEXTURE
        index_in_chunk = ()
        super().__init__(program, coord, TEXTURE_ID, index,
                         GPUDataManager().get_initial_index_for_object_id(ObjectId.SKYBOX),
                         GPUDataManager().get_size_index_for_object_id(ObjectId.SKYBOX))
