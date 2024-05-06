from OpenGL.GL import *
import glfw
import numpy as np

from src.facade import WindowFacade, ProgramFacade
from cube import Cube
from camera import Camera

window_width = 700
window_height = 500
old_x_pos = 0
old_y_pos = 0

camera = Camera(sensibility=0.2, step=0.001, fov=45.0, near=1, far=10)
render_polygons = False


def key_event(window, key, scancode, action, mods):
    global render_polygons

    # tecla pressionada
    if action == glfw.PRESS:
        if key == 87:
            camera.velocity = camera.direction()
        if key == 83:
            camera.velocity = -1 * camera.direction()
        if key == 65:
            camera.velocity = -1 * camera.perpendicular_direction()
        if key == 68:
            camera.velocity = camera.perpendicular_direction()
        if key == 90:
            camera.velocity = np.array([0.0, -1.0, 0.0])
        if key == 32:
            camera.velocity = np.array([0.0, 1.0, 0.0])

        # alterar o modo de visualização dos polígonos
        if key == 80:
            render_polygons = False if render_polygons else True

    # tecla liberada
    if action == glfw.RELEASE:
        camera.velocity = np.zeros(3)


def cursor_event(window, x_pos, y_pos):
    global old_x_pos, old_y_pos

    dx_pos = 0
    if np.abs(x_pos - old_x_pos) < window_width / 4:
        dx_pos = x_pos - old_x_pos

    dy_pos = 0
    if np.abs(y_pos - old_y_pos) < window_height / 4:
        dy_pos = y_pos - old_y_pos

    dx_angle = camera.fov * dx_pos / window_width
    dy_angle = camera.fov * dy_pos / window_height

    camera.target.x += camera.sensibility * np.sin(dx_angle)
    camera.target.y -= camera.sensibility * np.sin(dy_angle)
    camera.target.z -= camera.sensibility * np.sin(dx_angle) * np.cos(dy_angle)
    old_x_pos = x_pos
    old_y_pos = y_pos


def main():
    window = WindowFacade.setup_window(window_width, window_height, "MineTest")
    program = ProgramFacade.setup_program()

    # inicialização do objeto em cena
    obj = Cube(program, [0.0, 0.0, 0.0])
    obj.send_vertexes_to_gpu()

    # ouve os eventos do teclado e mouse
    glfw.set_key_callback(window, key_event)
    glfw.set_cursor_pos_callback(window, cursor_event)

    # loop de renderização
    glfw.show_window(window)
    glEnable(GL_DEPTH_TEST)  # importante para 3D!

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

        # renderização e atualização do objeto
        obj.render(window_height, window_width, camera)
        camera.update_position()
        camera.update_targets()

        glfw.swap_buffers(window)

    glfw.terminate()


main()
