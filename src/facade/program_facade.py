from OpenGL.GL import *
import textwrap


class ProgramFacade:
    # GLSL para Vertex Shader
    VERTEX_CODE: str = textwrap.dedent("""
                attribute vec3 position;
                attribute vec2 texture_coord;
                attribute vec3 normals;
                
                varying vec2 out_texture;
                varying vec3 out_fragPos;
                varying vec3 out_normal;

                uniform mat4 model;
                uniform mat4 view;
                uniform mat4 projection;        

                void main() {
                    gl_Position = projection * view * model * vec4(position,1.0);
                    out_texture = vec2(texture_coord);
                    out_fragPos = vec3(model * vec4(position, 1.0));
                    out_normal = vec3(model * vec4(normals, 1.0));
                }
            """)

    # GLSL para Fragment Shader
    FRAGMENT_CODE: str = textwrap.dedent("""
                // parâmetro com a cor da(s) fonte(s) de iluminação
                uniform vec3 lightPos; // define coordenadas de posição da luz
                vec3 lightColor = vec3(1.0, 1.0, 1.0);
                
                // parâmetros da iluminação ambiente e difusa
                uniform float ka; // coeficiente de reflexão ambiente
                uniform float kd; // coeficiente de reflexão difusa
                
                // parâmetros da iluminação especular
                uniform vec3 viewPos; // define coordenadas com a posição da camera/observador
                uniform float ks; // coeficiente de reflexão especular
                uniform float ns; // expoente de reflexão especular
                
                // parâmetros recebidos do vertex shader
                varying vec2 out_texture; // recebido do vertex shader
                varying vec3 out_normal; // recebido do vertex shader
                varying vec3 out_fragPos; // recebido do vertex shader
                uniform sampler2D samplerTexture;
        
                // ajustando kd e ks de acordo com a distância entre a luz e o objeto
                uniform float dist_light;
                float distance = length(lightPos - out_fragPos);
                float new_kd = kd - distance / dist_light;
                float new_ks = ks - distance / dist_light;
        
                void main() {
                    if (new_kd < 0.0f) {
                        new_kd = 0.0f;
                    }     
                    if (new_ks < 0.0f) {
                        new_ks = 0.0f;
                    }
                
                    // calculando reflexão ambiente
                    vec3 ambient = ka * lightColor;
                
                    // calculando reflexão difusa
                    vec3 norm = normalize(out_normal); // normaliza vetores perpendiculares
                    vec3 lightDir = normalize(lightPos - out_fragPos); // direção da luz
                    float diff = max(dot(norm, lightDir), 0.0); // verifica limite angular (entre 0 e 90)
                    vec3 diffuse = new_kd * diff * lightColor; // iluminação difusa
                    
                    // calculando reflexão especular
                    vec3 viewDir = normalize(viewPos - out_fragPos); // direção do observador/camera
                    vec3 reflectDir = normalize(reflect(-lightDir, norm)); // direção da reflexão
                    float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
                    vec3 specular = new_ks * spec * lightColor;
                    
                    // aplicando o modelo de iluminação
                    vec4 texture = texture2D(samplerTexture, out_texture);
                    if (texture.a < 0.3f) {
                        discard;
                    }
                    vec4 result = vec4((ambient + diffuse + specular), 1.0) * texture; // aplica iluminação
                    gl_FragColor = result;
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
