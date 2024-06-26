from src.util import singleton
from src.object import GameObject, ObjectId
from src.manager import GPUDataManager
from src.texture import TextureId


@singleton
class SkyBox(GameObject):

    TEXTURE_ID: TextureId = TextureId.SKYBOX_TEXTURE
    SCALE = (150.0, 150.0, 150.0)

    def __init__(self, program, coord: list, ka_ilum_parameter: float):
        index_in_chunk = ()
        super().__init__(program, coord, self.TEXTURE_ID, index_in_chunk,
                         GPUDataManager().get_initial_index_for_object_id(ObjectId.SKYBOX),
                         GPUDataManager().get_size_index_for_object_id(ObjectId.SKYBOX), [])

        self.set_surface_illumination_proprieties(ka_ilum_parameter)

    def set_surface_illumination_proprieties(self, ka):
        super().set_surface_illumination_proprieties(ka, 0.0, 0.0, 1.0)

    def dynamic_render(self, window_height, window_width, camera, illumination):
        self.__update_coord(camera.position)
        super().render(window_height, window_width, camera, illumination, list(self.SCALE))

    def __update_coord(self, new_coord: list):
        super().update_coord(new_coord)

