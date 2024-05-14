import numpy as np
from OpenGL.GL import *
import glfw

from src.facade import WindowFacade, ProgramFacade
from src.camera import CameraMovement
from src.camera import Camera
from src.util.loader import TextureLoader
from src.manager import GPUDataManager
from src.manager import ChunkManager

window_width = 700
window_height = 400

old_x_pos = 0
old_y_pos = 0

camera = Camera(sensibility=0.15, step=0.2, fov=45.0, near=0.01, far=1000.0)
render_polygons = False
movement_camera = True


def key_event(window, key, scancode, action, mods):
    global render_polygons, movement_camera

    # tecla pressionada
    if action == glfw.PRESS:
        if key == 87:  # W
            camera.movement = CameraMovement.FRONT
        if key == 83:  # S
            camera.movement = CameraMovement.BACK
        if key == 65:  # A
            camera.movement = CameraMovement.LEFT
        if key == 68:  # D
            camera.movement = CameraMovement.RIGHT
        if key == 90:  # Z
            camera.movement = CameraMovement.DOWN
        if key == 32:  # space
            camera.movement = CameraMovement.UP

        # alterar o modo de visualização dos polígonos
        if key == 80:  # P
            render_polygons = False if render_polygons else True

        # altera o modo de congelar o movimento da câmera
        if key == 256:  # ESC
            movement_camera = False if movement_camera else True

    # tecla liberada
    if action == glfw.RELEASE:
        camera.movement = CameraMovement.STOP


def cursor_event(window, x_pos, y_pos):
    global old_x_pos, old_y_pos

    # calcula a variação de movimento do mouse, não permitindo variações muito grandes
    dx_pos = x_pos - old_x_pos if np.abs(x_pos - old_x_pos) < window_width / 4 else 0
    dy_pos = y_pos - old_y_pos if np.abs(y_pos - old_y_pos) < window_height / 4 else 0
    old_x_pos = x_pos
    old_y_pos = y_pos

    # converte a variação de movimento do mouse para a variação de angulação da câmera
    angle_precision = 1e-4  # limita o quão perpendicular ao chão a câmera pode olhar
    camera.horizontal_angle -= camera.sensibility * camera.fov * dx_pos / window_width
    camera.vertical_angle -= camera.sensibility * camera.fov * dy_pos / window_height
    camera.vertical_angle = np.clip(camera.vertical_angle, -np.pi / 2 + angle_precision, np.pi / 2 - angle_precision)


def main():
    global old_x_pos, old_y_pos

    # inicialização da janela e programa
    window = WindowFacade.setup_window(window_width, window_height, "MineTest")
    program = ProgramFacade.setup_program()

    # carregamento das texturas
    TextureLoader.load_all_block_textures()
    TextureLoader.load_all_misc_textures()

    # envio de dados apara gpu
    gpu_manager = GPUDataManager(program)
    gpu_manager.configure()

    # inicialização do chunk
    chunk = ChunkManager.generate_chunk(0, 0, gpu_manager)
    chunk.build(program)

    # ouve os eventos do teclado e mouse
    glfw.set_key_callback(window, key_event)
    glfw.set_cursor_pos_callback(window, cursor_event)

    # loop de renderização
    glfw.show_window(window)

    count = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()

        # limpa a cor de fundo da janela e preenche com outra no sistema RGBA
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(1.0, 1.0, 1.0, 1.0)

        # verifica o modo de renderização (se é apenas as arestas ou tudo)
        if render_polygons:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # renderização e atualização do chunk
        chunk.render(window_height, window_width, camera)
        chunk.update_entities(count)

        # atualização da câmera
        camera.update_position()
        camera.update_angle_view()

        # retorna o cursor para o centro da tela e deixa-o invisível
        if movement_camera:
            old_x_pos = window_width // 2
            old_y_pos = window_height // 2
            glfw.set_cursor_pos(window, window_width // 2, window_height // 2)
            glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
        else:
            glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)

        glfw.swap_buffers(window)
        count = (count + 1) % 30

    glfw.terminate()


main()
