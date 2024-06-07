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
                // define a estrutura para as propriedades da luz
                struct Light {
                    vec3 position;
                    vec3 color;
                };
                
                // define um array uniforme para múltiplas fontes de luz
                uniform int numLights; // número de fontes de luz
                uniform Light lights[10]; // array de luzes, supondo no máximo 10 luzes
                
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
        
                // parâmetro para definir o quão longe a luz se propaga
                uniform float dist_light;
        
                void main() {
                    vec3 ambient = vec3(0.0);
                    vec3 diffuse = vec3(0.0);
                    vec3 specular = vec3(0.0);
                    
                    // calculando reflexão ambiente
                    ambient += ka * vec3(1.0, 1.0, 1.0);
                
                    vec3 norm = normalize(out_normal); // normaliza vetores perpendiculares
                    vec3 viewDir = normalize(viewPos - out_fragPos); // direção do observador/camera
                    
                    for (int i = 0; i < numLights; i ++) {
                        float distance = length(lights[i].position - out_fragPos);
                        float new_kd = max(kd - distance / dist_light, 0.0);
                        float new_ks = max(ks - distance / dist_light, 0.0);
                    
                        // calculando reflexão difusa
                        vec3 lightDir = normalize(lights[i].position - out_fragPos); // direção da luz
                        float diff = max(dot(norm, lightDir), 0.0); // verifica limite angular (entre 0 e 90)
                        diffuse += new_kd * diff * lights[i].color; // iluminação difusa
                        
                        // calculando reflexão especular
                        vec3 reflectDir = normalize(reflect(-lightDir, norm)); // direção da reflexão
                        float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
                        specular += new_ks * spec * lights[i].color;
                    }
                    
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
