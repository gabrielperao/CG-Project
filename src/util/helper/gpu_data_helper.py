from OpenGL.GL import *


class GpuDataHelper:
    @staticmethod
    def send_var_to_gpu(program, var, gpu_var_name):
        loc = glGetUniformLocation(program, gpu_var_name)
        glUniform1f(loc, var)

    @staticmethod
    def send_array3_to_gpu(program, array, gpu_var_name):
        loc = glGetUniformLocation(program, gpu_var_name)
        glUniform3f(loc, array[0], array[1], array[2])

    @staticmethod
    def send_array_to_gpu(program, array, buffer_slot, dim, gpu_var_name):
        glBindBuffer(GL_ARRAY_BUFFER, buffer_slot)
        glBufferData(GL_ARRAY_BUFFER, array.nbytes, array, GL_DYNAMIC_DRAW)

        stride = array.strides[0]
        offset = ctypes.c_void_p(0)

        loc = glGetAttribLocation(program, gpu_var_name)
        glEnableVertexAttribArray(loc)
        glVertexAttribPointer(loc, dim, GL_FLOAT, False, stride, offset)
