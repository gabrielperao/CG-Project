import glfw


class WindowFacade:
    @staticmethod
    def _create_window(window_width: int, window_height: int, window_name: str):
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        window = glfw.create_window(window_width, window_height, window_name, None, None)
        glfw.make_context_current(window)
        return window

    @classmethod
    def setup_window(cls, window_width: int, window_height: int, window_name: str) -> tuple:
        if not glfw.init():
            raise RuntimeError("Erro ao inicializar o GLFW")

        window = cls._create_window(window_width, window_height, window_name)
        return window
