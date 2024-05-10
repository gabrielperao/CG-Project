from OpenGL.GL import *
import glfw
import numpy as np

from src.facade import WindowFacade, ProgramFacade
from src.camera import Camera, CameraMovement
from src.util.loader import TextureLoader
from camera import Camera

from src.object.object_id import ObjectId
from chunk import Chunk

window_width = 700
window_height = 500
old_x_pos = 0
old_y_pos = 0

camera = Camera(sensibility=0.2, step=0.003, fov=45.0, near=0.01, far=1000.0)
render_polygons = False


def key_event(window, key, scancode, action, mods):
    global render_polygons

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
    window = WindowFacade.setup_window(window_width, window_height, "MineTest")
    program = ProgramFacade.setup_program()

    TextureLoader.load_all_block_textures()
    # TextureLoader.load_all_misc_textures()  TODO: adicionar texturas misc (galinha, tocha, flor)

    # inicialização do chunk
    chunk = Chunk(0, 0)
    chunk.put_object((1, 0, 1), ObjectId.GRASS)
    chunk.put_object((0, 0, 0), ObjectId.GRASS)
    chunk.put_object((0, 1, 0), ObjectId.STONE)
    chunk.put_object((0, 0, 1), ObjectId.GRASS)
    chunk.build(program)

    # ouve os eventos do teclado e mouse
    glfw.set_key_callback(window, key_event)
    glfw.set_cursor_pos_callback(window, cursor_event)

    # loop de renderização
    glfw.show_window(window)

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

        # renderização do chunk
        chunk.render(window_height, window_width, camera)

        # atualização da câmera
        camera.update_position()
        camera.update_angle_view()

        glfw.swap_buffers(window)

    glfw.terminate()


main()
