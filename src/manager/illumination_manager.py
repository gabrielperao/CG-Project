from src.util.helper import GpuDataHelper


class Light:
    def __init__(self, position: list, color: list):
        self.position = position
        self.color = color


class IlluminationManager:
    def __init__(self, program, dist_light):
        self.sources = []
        self.program = program

        self.dist_light = dist_light
        GpuDataHelper.send_var_to_gpu(self.program, self.dist_light, "dist_light")

    def get_num_sources(self):
        return len(self.sources)

    def __send_light_data_to_gpu(self, index):
        GpuDataHelper.send_array3_to_gpu(self.program, self.sources[index].position, f"lights[{index}].position")
        GpuDataHelper.send_array3_to_gpu(self.program, self.sources[index].color, f"lights[{index}].color")

    def add_source(self, position, color):
        self.sources.append(Light(position, color))
        self.__send_light_data_to_gpu(len(self.sources) - 1)
        GpuDataHelper.send_integer_to_gpu(self.program, len(self.sources), "numLights")

    def update_source_position(self, index, new_position):
        if index < 0 or index >= len(self.sources):
            raise IndexError("Índice inexistente")

        current_light = self.sources[index]
        new_light = Light(new_position, current_light.color)
        self.sources[index] = new_light
        self.__send_light_data_to_gpu(index)
