#include <GL/glew.h>  
#define GLFW_INCLUDE_NONE
#include <GLFW/glfw3.h> /* verifique no seu SO onde fica o glfw3.h */
#include <iostream>
#include <utility>
#include <vector>
#include <cmath>

using namespace std;

typedef struct{
    float x, y;
} coords;

// constantes de dimensão da janela
#define WINDOW_W 600
#define WINDOW_H 600

// dados o objeto
typedef struct {
    float posInc = 0.0f;
    float x = 0.0f;
    float y = 0.0f;
    float angle = 0.0f;
    float size = 1.0f;
} object;

object tr;

pair<GLFWwindow*, GLuint> setupWindow(int windowWidth, int windowHeight, char* windowName) {
    // inicicializando o sistema de janelas
    glfwInit();

    // deixando a janela invisivel, por enquanto
    glfwWindowHint(GLFW_VISIBLE, GLFW_FALSE);

    // criando uma janela
    GLFWwindow* window = glfwCreateWindow(windowWidth, windowHeight, windowName, NULL, NULL);

    // tornando a janela como principal 
    glfwMakeContextCurrent(window);

    // inicializando Glew (para lidar com funcoes OpenGL)
    GLint GlewInitResult = glewInit();
    printf("GlewStatus: %s", glewGetErrorString(GlewInitResult));

    // GLSL para Vertex Shader
    char* vertex_code =
        "attribute vec2 position;\n"
        "uniform mat4 mat_transformation;\n" // define a matriz de transformação utilizada no objeto
        "void main()\n"
        "{\n"
        "    gl_Position = mat_transformation*vec4(position, 0.0, 1.0);\n"
        "}\n";

    // GLSL para Fragment Shader
    char* fragment_code =
        "uniform vec4 color;\n"
        "void main()\n"
        "{\n"
        "    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);\n" // define a cor do fragmento desenhado
        "}\n";

    // Requisitando slot para a GPU para nossos programas Vertex e Fragment Shaders
    GLuint program = glCreateProgram();
    GLuint vertex = glCreateShader(GL_VERTEX_SHADER);
    GLuint fragment = glCreateShader(GL_FRAGMENT_SHADER);

    // Associando nosso código-fonte GLSL aos slots solicitados
    glShaderSource(vertex, 1, &vertex_code, NULL);
    glShaderSource(fragment, 1, &fragment_code, NULL);

    // Compilando o Vertex Shader e verificando erros
    glCompileShader(vertex);

    GLint isCompiled = 0;
    glGetShaderiv(vertex, GL_COMPILE_STATUS, &isCompiled);
    if (isCompiled == GL_FALSE) {
        //descobrindo o tamanho do log de erro
        int infoLength = 512;
        glGetShaderiv(vertex, GL_INFO_LOG_LENGTH, &infoLength);

        //recuperando o log de erro e imprimindo na tela
        char info[infoLength];
        glGetShaderInfoLog(vertex, infoLength, NULL, info);

        cout << "Erro de compilacao no Vertex Shader.\n";
        cout << "--> " << info << "\n";
    }

    // Compilando o Fragment Shader e verificando erros
    glCompileShader(fragment);

    isCompiled = 0;
    glGetShaderiv(fragment, GL_COMPILE_STATUS, &isCompiled);
    if (isCompiled == GL_FALSE) {
        //descobrindo o tamanho do log de erro
        int infoLength = 512;
        glGetShaderiv(fragment, GL_INFO_LOG_LENGTH, &infoLength);

        //recuperando o log de erro e imprimindo na tela
        char info[infoLength];
        glGetShaderInfoLog(fragment, infoLength, NULL, info);

        cout << "Erro de compilacao no Fragment Shader.\n";
        cout << "--> " << info << "\n";
    }

    // Associando os programas compilado ao programa principal
    glAttachShader(program, vertex);
    glAttachShader(program, fragment);

    // Linkagem do programa e definindo como default
    glLinkProgram(program);
    glUseProgram(program);

    return make_pair(window, program);
}

// função para processar eventos de teclado
static void key_event(GLFWwindow* window, int key, int scancode, int action, int mods) {
    if (key == 265) tr.posInc += 0.0001; // tecla para cima
    if (key == 264) tr.posInc -= 0.0001; // tecla para baixo

    if (key == 334) tr.size += 0.05; // tecla +
    if (key == 333 && tr.size > 0) tr.size -= 0.05; // tecla -
}

// ajusta o ângulo do objeto de acordo com a posição do mouse na janela
static void cursor_angle(GLFWwindow* window, double xpos, double ypos) {
    // normaliza as coordenadas do cursor
    float xposNorm = 2 * (xpos - (WINDOW_W / 2)) / WINDOW_W;
    float yposNorm = -2 * (ypos - (WINDOW_H / 2)) / WINDOW_H;

    tr.angle = -1 * atan2(xposNorm - tr.x, yposNorm - tr.y);
}

// copia o conteúdo de uma matriz 4x4 em outra
void copyMat(float *mOrigin, float *mDest) {
    for (short int i = 0; i < 16; i ++)
        mDest[i] = mOrigin[i];
}

// faz a multiplicação matricial 4x4 m1.m2 e armazena em mRes
void matMul(float *m1, float *m2, float *mRes) {
    float sum;
    for (short int i = 0; i < 4; i ++) {
        for (short int j = 0; j < 4; j ++) {
            sum = 0;
            for (short int k = 0; k < 4; k ++) {
                sum += m1[(i * 4) + k] * m2[(k * 4) + j];
            }
            mRes[(i * 4) + j] = sum;
        }
    }
}

// faz a multiplicação matricial (em ordem) de uma sequência de matrizes e armazena em mRes
void matMulAll(vector<float*> mats, float *mRes) {
    float mAux[16];
    copyMat(mats[0], mAux);

    for (short int i = 1; i < mats.size(); i ++) {
        matMul(mAux, mats[i], mRes);
        copyMat(mRes, mAux);
    }
}

int main(void) {
    pair<GLFWwindow*, GLuint> vars = setupWindow(WINDOW_W, WINDOW_H, "Janela");
    GLFWwindow* window = vars.first;
    GLuint program = vars.second;

    // Preparando dados para enviar a GPU
    coords vertices[3] = {
        { +0.00f, +0.05f },
        { -0.05f, -0.05f },
        { +0.05f, -0.05f }
    };

    GLuint buffer;
    glGenBuffers(1, &buffer);
    glBindBuffer(GL_ARRAY_BUFFER, buffer);

    // Abaixo, nós enviamos todo o conteúdo da variável vertices.
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_DYNAMIC_DRAW);

    // Associando variáveis do programa GLSL (Vertex Shaders) com nossos dados
    GLint loc = glGetAttribLocation(program, "position");
    glEnableVertexAttribArray(loc);
    glVertexAttribPointer(loc, 2, GL_FLOAT, GL_FALSE, sizeof(vertices[0]), (void*) 0); // https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glVertexAttribPointer.xhtml

    // Associando nossa janela com eventos de teclado e de mouse
    glfwSetKeyCallback(window, key_event);
    glfwSetCursorPosCallback(window, cursor_angle);

    // Exibindo nossa janela
    glfwShowWindow(window);

    // configuração de cores e desenhos com os vértices
    while (!glfwWindowShouldClose(window)) {
        glfwPollEvents();
        glClear(GL_COLOR_BUFFER_BIT);
        glClearColor(1.0, 1.0, 1.0, 1.0); // cor do fundo

        // atualiza os valores da nave
        tr.x += tr.posInc * cos(tr.angle + M_PI / 2);
        tr.y += tr.posInc * sin(tr.angle + M_PI / 2);

        // objeto passa para o outro lado da tela caso chegue ao final
        if (tr.x - tr.size/14 > 1 || tr.x + tr.size/14 < -1) tr.x *= -1;
        if (tr.y - tr.size/14 > 1 || tr.y + tr.size/14 < -1) tr.y *= -1;

        // matriz de translação
        float mat_translation[16] = {
            1.0f, 0.0f, 0.0f, tr.x,
            0.0f, 1.0f, 0.0f, tr.y,
            0.0f, 0.0f, 1.0f, 0.0f,
            0.0f, 0.0f, 0.0f, 1.0f
        };

        // matriz de translação oposta
        float mat_translation_opos[16] = {
            1.0f, 0.0f, 0.0f, -tr.x,
            0.0f, 1.0f, 0.0f, -tr.y,
            0.0f, 0.0f, 1.0f, 0.0f,
            0.0f, 0.0f, 0.0f, 1.0f
        };

        // matriz de escala
        float mat_scale[16] = {
            tr.size, 0.0f, 0.0f, 0.0f,
            0.0f, tr.size, 0.0f, 0.0f,
            0.0f, 0.0f, 1.0f, 0.0f,
            0.0f, 0.0f,  0.0f, 1.0f
        };

        // matriz de rotação
        float c = cos(tr.angle);
        float s = sin(tr.angle);
        float mat_rotation[16] = {
            c   , -s  , 0.0f, 0.0f,
            s   , c   , 0.0f, 0.0f,
            0.0f, 0.0f, 1.0f, 0.0f,
            0.0f, 0.0f, 0.0f, 1.0f
        };

        // calcula a transformação resultante
        float mat_transf[16];
        vector<float*> mats = {
            mat_translation,
            mat_rotation,
            mat_scale,
            mat_translation_opos,
            mat_translation
        };
        matMulAll(mats, mat_transf);

        // enviando a matriz de transformacao para a GPU, vertex shader, variavel mat_transformation
        loc = glGetUniformLocation(program, "mat_transformation");
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transf);

        // renderiza o objeto transformado
        glDrawArrays(GL_TRIANGLES, 0, 3);
        glfwSwapBuffers(window);
    }
 
    // encerra a janela
    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}