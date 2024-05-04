import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm
import math

def setup_window(window_width, window_height, window_name):
    # inicializa o GLFW
    if not glfw.init():
        raise RuntimeError("Erro ao inicializar o GLFW")

    # inicializa o sistema de janela
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(window_width, window_height, window_name, None, None)
    glfw.make_context_current(window)

    # GLSL para Vertex Shader
    vertex_code = """
        attribute vec3 position;
                
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;        
        
        void main(){
            gl_Position = projection * view * model * vec4(position,1.0);
        }
    """

    # GLSL para Fragment Shader
    fragment_code = """
        uniform vec4 color;
        void main(){
            gl_FragColor = color;
        }
    """

    # requisitando slot para a GPU para nossos programas
    program  = glCreateProgram()
    vertex   = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    # associando nosso código-fonte GLSL aos slots solicitados
    glShaderSource(vertex, vertex_code)
    glShaderSource(fragment, fragment_code)

    # compilando vertex shaders
    glCompileShader(vertex)
    if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(vertex).decode()
        print(error)
        raise RuntimeError("Erro de compilação do Vertex Shader")

    # compilando fragment shaders
    glCompileShader(fragment)
    if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(fragment).decode()
        print(error)
        raise RuntimeError("Erro de compilação do Fragment Shader")

    # associando os programas compilado ao programa principal
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)

    # construção do programa
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')
        
    # definindo como default
    glUseProgram(program)
    return window, program

def matrix_projection(height, width, fov, near, far):
    mat_projection = glm.perspective(glm.radians(fov), width/height, near, far)
    mat_projection = np.array(mat_projection).T
    mat_projection[2,2] = mat_projection[2,2]*-1
    return mat_projection

def matrix_model():
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade   
    matrix_transform = glm.rotate(matrix_transform, math.radians(180), glm.vec3(0.0,0.0,1.0))
    matrix_transform = glm.translate(matrix_transform, glm.vec3(0.0, 0.5, -2))
    matrix_transform = np.array(matrix_transform).T 
    return matrix_transform

def matrix_view(camera_pos, camera_target, camera_up):
    mat_view = glm.lookAt(camera_pos, camera_target, camera_up)
    mat_view = np.array(mat_view).T
    return mat_view

def key_event(window, key, scancode, action, mods):
    global z_camera_pos, camera_pos, near, far

    if key == 265: z_camera_pos-=0.3
    if key == 264: z_camera_pos+=0.3       
    camera_pos = glm.vec3(0.0, 0.0, z_camera_pos)

    if key == 87: far-=0.3
    if key == 83: far+=0.3

def main():
    window_width = 700
    window_height = 500
    window, program = setup_window(window_width, window_height, "teste")

    # define os vértices do objeto
    vertexes = np.zeros(24, [("position", np.float32, 3)])
    vertexes['position'] = [
        # Face 1 do Cubo (vértices do quadrado)
        (-0.2, -0.2, +0.2),
        (+0.2, -0.2, +0.2),
        (-0.2, +0.2, +0.2),
        (+0.2, +0.2, +0.2),

        # Face 2 do Cubo
        (+0.2, -0.2, +0.2),
        (+0.2, -0.2, -0.2),         
        (+0.2, +0.2, +0.2),
        (+0.2, +0.2, -0.2),
        
        # Face 3 do Cubo
        (+0.2, -0.2, -0.2),
        (-0.2, -0.2, -0.2),            
        (+0.2, +0.2, -0.2),
        (-0.2, +0.2, -0.2),

        # Face 4 do Cubo
        (-0.2, -0.2, -0.2),
        (-0.2, -0.2, +0.2),         
        (-0.2, +0.2, -0.2),
        (-0.2, +0.2, +0.2),

        # Face 5 do Cubo
        (-0.2, -0.2, -0.2),
        (+0.2, -0.2, -0.2),         
        (-0.2, -0.2, +0.2),
        (+0.2, -0.2, +0.2),
        
        # Face 6 do Cubo
        (-0.2, +0.2, +0.2),
        (+0.2, +0.2, +0.2),           
        (-0.2, +0.2, -0.2),
        (+0.2, +0.2, -0.2)
    ]

    # envio de dados para a GPU
    buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)

    glBufferData(GL_ARRAY_BUFFER, vertexes.nbytes, vertexes, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)

    # localizamos as variáveis de posição e cor na GPU
    stride = vertexes.strides[0]
    offset = ctypes.c_void_p(0)

    loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc)
    glVertexAttribPointer(loc, 3, GL_FLOAT, GL_FALSE, stride, offset)
    loc_color = glGetUniformLocation(program, "color")

    z_camera_pos = 5.0
    camera_pos = glm.vec3(0.0, 0.0, z_camera_pos)
    camera_target = glm.vec3(0.0, 0.0, 0.0)
    camera_up = glm.vec3(0.0, 1.0, 0.0)
    fov = 45.0
    near = 1
    far = 10

    # ouve os eventos do teclado
    glfw.set_key_callback(window, key_event)

    # loop de renderização
    glfw.show_window(window)
    glEnable(GL_DEPTH_TEST) ### importante para 3D
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        # limpa a cor de fundo da janela e preenche com outra no sistema RGBA
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        
        # glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        
        # cálculo da matriz model e manda para a GPU
        mat_model = matrix_model()
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)    
        
        # cálculo da matriz view e manda para a GPU
        mat_view = matrix_view(camera_pos, camera_target, camera_up)
        loc_view = glGetUniformLocation(program, "view")
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

        # cálculo da matriz projection e manda para a GPU
        mat_projection = matrix_projection(window_height, window_width, fov, near, far)
        loc_projection = glGetUniformLocation(program, "projection")
        glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)    
        
        # renderizando a cada três vértices (triangulos)
        for i in range(0, len(vertexes['position']),3):
            glUniform4f(loc_color, 0.3, 1.0, 0.2, 1.0) ### definindo uma cor
            glDrawArrays(GL_TRIANGLES, i, 3)
        
        glfw.swap_buffers(window)

    glfw.terminate()

main()