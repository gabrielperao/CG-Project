from src.util.helper import GpuDataHelper


class Light:
    def __init__(self, position: list, color: list, index_map: tuple):
        self.position = position
        self.color = color
        self.index_map = index_map


class IlluminationManager:
    MAX_SOURCES: 10

    def __init__(self, program, dist_light):
        self.sources = []
        self.program = program

        self.dist_light = dist_light
        GpuDataHelper.send_var_to_gpu(self.program, self.dist_light, "dist_light")

    def get_num_sources(self):
        return len(self.sources)

    def get_source(self, index_map):
        for source in self.sources:
            if source.index_map == index_map:
                return source

        return None

    def add_source(self, position, color, index_map):
        self.sources.append(Light(position, color, index_map))

    def update_source_position(self, index, new_position):
        if index < 0 or index >= len(self.sources):
            raise IndexError("Índice inexistente")

        current_light = self.sources[index]
        new_light = Light(new_position, current_light.color, current_light.index_map)
        self.sources[index] = new_light

    @staticmethod
    def __send_light_data_to_gpu(program, source: Light, index: int):
        GpuDataHelper.send_array3_to_gpu(program, source.position, f"lights[{index}].position")
        GpuDataHelper.send_array3_to_gpu(program, source.color, f"lights[{index}].color")

    def send_lights_to_gpu(self, sources_indexes):
        GpuDataHelper.send_integer_to_gpu(self.program, len(sources_indexes), "numLights")
        for i, source_index in enumerate(sources_indexes):
            source = self.get_source(source_index)
            IlluminationManager.__send_light_data_to_gpu(self.program, source, i)
