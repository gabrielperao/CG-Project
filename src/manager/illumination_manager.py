from src.util.helper import GpuDataHelper


class Light:
    def __init__(self, position: list, color: list):
        self.position = position
        self.color = color


class IlluminationManager:
    def __init__(self, program, dist_light):
        self.fonts = []
        self.program = program

        self.dist_light = dist_light
        GpuDataHelper.send_var_to_gpu(self.program, self.dist_light, "dist_light")

    def get_num_fonts(self):
        return len(self.fonts)

    def __send_light_data_to_gpu(self, index):
        GpuDataHelper.send_array3_to_gpu(self.program, self.fonts[index].position, f"lights[{index}].position")
        GpuDataHelper.send_array3_to_gpu(self.program, self.fonts[index].color, f"lights[{index}].color")

    def add_font(self, position, color):
        self.fonts.append(Light(position, color))
        self.__send_light_data_to_gpu(len(self.fonts) - 1)
        GpuDataHelper.send_integer_to_gpu(self.program, len(self.fonts), "numLights")

    def update_font_position(self, index, new_position):
        if index < 0 or index >= len(self.fonts):
            raise IndexError("Índice inexistente")

        current_light = self.fonts[index]
        new_light = Light(new_position, current_light.color)
        self.fonts[index] = new_light
        self.__send_light_data_to_gpu(index)
