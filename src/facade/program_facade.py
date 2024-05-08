from OpenGL.GL import *
import textwrap


class ProgramFacade:
    # GLSL para Vertex Shader
    VERTEX_CODE: str = textwrap.dedent("""
                attribute vec3 position;
                attribute vec2 texture_coord;
                varying vec2 out_texture;

                uniform mat4 model;
                uniform mat4 view;
                uniform mat4 projection;        

                void main(){
                    gl_Position = projection * view * model * vec4(position,1.0);
                    out_texture = vec2(texture_coord);
                }
            """)

    # GLSL para Fragment Shader
    FRAGMENT_CODE: str = textwrap.dedent("""
                uniform vec4 color;
                varying vec2 out_texture;
                uniform sampler2D samplerTexture;
        
                void main(){
                    vec4 texture = texture2D(samplerTexture, out_texture);
                    gl_FragColor = texture;
                }
        """)

    @staticmethod
    def __compile_shaders(vertex_shader: GLuint, fragment_shader: GLuint) -> None:
        glCompileShader(vertex_shader)
        glCompileShader(fragment_shader)

    @staticmethod
    def __attach_shaders(program, vertex_shader: GLuint, fragment_shader: GLuint) -> None:
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)

    @classmethod
    def __bind_shaders_sources(cls, vertex_shader: GLuint, fragment_shader: GLuint) -> None:
        glShaderSource(vertex_shader, cls.VERTEX_CODE)
        glShaderSource(fragment_shader, cls.FRAGMENT_CODE)

    @staticmethod
    def __enable_depth_test():
        glEnable(GL_DEPTH_TEST)

    @staticmethod
    def __configure_3d_render():
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_TEXTURE_2D)

    @classmethod
    def setup_program(cls):
        program = glCreateProgram()

        vertex = glCreateShader(GL_VERTEX_SHADER)
        fragment = glCreateShader(GL_FRAGMENT_SHADER)

        cls.__bind_shaders_sources(vertex, fragment)
        cls.__compile_shaders(vertex, fragment)
        cls.__attach_shaders(program, vertex, fragment)

        # construção do programa
        glLinkProgram(program)
        glUseProgram(program)

        cls.__enable_depth_test()
        cls.__configure_3d_render()
        return program
