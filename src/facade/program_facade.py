from OpenGL.GL import *
import textwrap


class ProgramFacade:
    # GLSL para Vertex Shader
    VERTEX_CODE: str = textwrap.dedent("""
                attribute vec3 position;

                uniform mat4 model;
                uniform mat4 view;
                uniform mat4 projection;        

                void main(){
                    gl_Position = projection * view * model * vec4(position,1.0);
                }
            """)

    # GLSL para Fragment Shader
    FRAGMENT_CODE: str = textwrap.dedent("""
                uniform vec4 color;
                void main(){
                    gl_FragColor = color;
                }
            """)

    @staticmethod
    def _compile_shaders(vertex_shader: GLuint, fragment_shader: GLuint) -> None:
        glCompileShader(vertex_shader)
        glCompileShader(fragment_shader)

    @staticmethod
    def _attach_shaders(program, vertex_shader: GLuint, fragment_shader: GLuint) -> None:
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)

    @classmethod
    def _bind_shaders_sources(cls, vertex_shader: GLuint, fragment_shader: GLuint) -> None:
        glShaderSource(vertex_shader, cls.VERTEX_CODE)
        glShaderSource(fragment_shader, cls.FRAGMENT_CODE)

    @classmethod
    def setup_program(cls):
        program = glCreateProgram()

        vertex = glCreateShader(GL_VERTEX_SHADER)
        fragment = glCreateShader(GL_FRAGMENT_SHADER)

        cls._bind_shaders_sources(vertex, fragment)
        cls._compile_shaders(vertex, fragment)
        cls._attach_shaders(program, vertex, fragment)

        # construção do programa
        glLinkProgram(program)
        glUseProgram(program)
        return program
