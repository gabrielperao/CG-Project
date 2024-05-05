from OpenGL.GL import *
import glfw


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
    program = glCreateProgram()
    vertex = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    # associando nosso código-fonte GLSL aos slots solicitados
    glShaderSource(vertex, vertex_code)
    glShaderSource(fragment, fragment_code)

    # compilando vertex shaders
    glCompileShader(vertex)
    if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
        print(glGetShaderInfoLog(vertex).decode())
        raise RuntimeError("Erro de compilação do Vertex Shader")

    # compilando fragment shaders
    glCompileShader(fragment)
    if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
        print(glGetShaderInfoLog(fragment).decode())
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
