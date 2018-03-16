from pyglet.window import Window
from pyglet.math.m4 import M4
import glfw
import numpy
import ctypes

from OpenGL.GL import *


def main():
    window = Window()
    ratio = float(window.width) / window.height

    vertices = numpy.array([
        # x, y, c1, c2, c3
        -0.6, -0.4, 1, 0, 0,
         0.6, -0.4, 0, 1, 0,
           0,  0.6, 0, 0, 1
    ], dtype=numpy.float32)

    vshader_str = """
uniform mat4 MVP;
attribute vec3 vCol;
attribute vec2 vPos;
varying vec3 color;
void main()
{
    gl_Position = MVP * vec4(vPos, 0.0, 1.0);
    color = vCol;
}
    """

    fshader_str = """
varying vec3 color;
void main()
{
    gl_FragColor = vec4(color, 1.0);
}
    """

    vbuf = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbuf)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)

    prog = glCreateProgram()

    vshader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vshader, vshader_str)
    glCompileShader(vshader)
    glAttachShader(prog, vshader)

    fshader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fshader, fshader_str)
    glCompileShader(fshader)
    glAttachShader(prog, fshader)

    glLinkProgram(prog)

    mvp_location = glGetUniformLocation(prog, "MVP")
    vpos_location = glGetAttribLocation(prog, "vPos")
    vcol_location = glGetAttribLocation(prog, "vCol")

    glEnableVertexAttribArray(vpos_location)
    glVertexAttribPointer(vpos_location, 2, GL_FLOAT, GL_FALSE, 4*5, ctypes.c_void_p(0))
    glEnableVertexAttribArray(vcol_location)
    glVertexAttribPointer(vcol_location, 3, GL_FLOAT, GL_FALSE, 4*5, ctypes.c_void_p(2*4))

    while not window.should_close():
        glViewport(0, 0, window.width, window.height)
        glClear(GL_COLOR_BUFFER_BIT)

        m = M4.rotate(glfw.get_time()) # * M4.ortho(-ratio, ratio, -1, 1, 1, -1)

        glUseProgram(prog)
        glUniformMatrix4fv(mvp_location, 1, GL_FALSE, m.m)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        window.swap_buffers()
        Window.poll_events()

    Window.terminate()


if __name__ == "__main__":
    main()
