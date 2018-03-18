from OpenGL.GL import *
import numpy

from pyglet.graphics.shader import Shader
from pyglet.math import M4


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

        self.vertices = None

        self.va = glGenVertexArrays(1)
        glBindVertexArray(self.va)

        self.vbuf = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbuf)
        glEnableVertexAttribArray(0)

        self.shader = Shader(
            vsrc="""
                #version 330 core

                uniform mat4 MVP;
                in vec4 vCol;
                in vec4 vPos;

                out vec4 color;

                void main()
                {
                    gl_Position = MVP * vPos;
                    color = vCol;
                }
            """,
            fsrc="""
                #version 330 core

                in vec4 color;
                out vec4 fragColor;

                void main()
                {
                    fragColor = color;
                }
            """
        )

        self.shader.def_uniform("MVP")
        self.shader.def_attrib("vPos", {'size': 4, 'stride': 8})
        self.shader.def_attrib("vCol", {'size': 4, 'stride': 8, 'offset': 4})

        self.mvp = M4.identity()

    def reset(self):
        self.mvp = M4.identity()

    def rotate(self, *args):
        self.mvp *= M4.rotate(*args)

    def ortho(self, *args):
        self.mvp *= M4.ortho(*args)

    def translate(self, *args):
        self.mvp *= M4.translate(*args)

    def scale(self, *args):
        self.mvp *= M4.scale(*args)

    def draw(self):
        self.vertices = numpy.array([
            *self.a.pos, *self.a.col,
            *self.b.pos, *self.b.col,
            *self.c.pos, *self.c.col,
        ], dtype=numpy.float32)

        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        self.shader.bind(
            {'MVP': ('Matrix4fv', 1, Shader.FALSE, self.mvp.m)}
        )

        glDrawArrays(GL_TRIANGLES, 0, 3)
