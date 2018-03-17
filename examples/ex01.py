from pyglet.graphics.window import Window
from pyglet.graphics.shader import Shader
from pyglet.math.m4 import M4
import numpy

from OpenGL.GL import *


def main():
    window = Window()
    ratio = float(window.width) / window.height

    vertices = numpy.array([
        # x, y, c1, c2, c3
        -0.6, -0.4, 1, 0, 0,
        0.6, -0.4, 0, 1, 0,
        0, 0.6, 0, 0, 1
    ], dtype=numpy.float32)

    vbuf = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbuf)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)

    shader = Shader(
        vsrc="""
uniform mat4 MVP;
attribute vec3 vCol;
attribute vec2 vPos;
varying vec3 color;
void main()
{
    gl_Position = MVP * vec4(vPos, 0.0, 1.0);
    color = vCol;
}
""",
        fsrc="""
varying vec3 color;
void main()
{
    gl_FragColor = vec4(color, 1.0);
}
"""
    )

    shader.def_uniform("MVP")
    shader.def_attrib("vPos", {'size': 2, 'stride': 5})
    shader.def_attrib("vCol", {'size': 3, 'stride': 5, 'offset': 2})

    while not window.should_close():
        glViewport(0, 0, window.width, window.height)
        glClear(GL_COLOR_BUFFER_BIT)

        m = M4.rotate(Window.get_time()) * M4.ortho(-ratio, ratio, -1, 1, 1, -1)

        shader.bind(
            {'MVP': ('Matrix4fv', 1, Shader.FALSE, m.m)}
        )

        glDrawArrays(GL_TRIANGLES, 0, 3)

        window.swap_buffers()
        Window.poll_events()

    Window.terminate()


if __name__ == "__main__":
    main()
