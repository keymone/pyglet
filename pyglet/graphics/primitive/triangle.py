from OpenGL.GL import *
import numpy

from pyglet.graphics.shader import Shader
from pyglet.math.m4 import M4


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

        self.vertices = numpy.array([
            *a.pos, *a.rgb,
            *b.pos, *b.rgb,
            *c.pos, *c.rgb,
        ], dtype=numpy.float32)

        self.vbuf = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbuf)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)

        self.shader = Shader(
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

        self.shader.def_uniform("MVP")
        self.shader.def_attrib("vPos", {'size': 2, 'stride': 5})
        self.shader.def_attrib("vCol", {'size': 3, 'stride': 5, 'offset': 2})

        self.mvp = M4.identity()

    def reset(self):
        self.mvp = M4.identity()

    def rotate(self, *args):
        self.mvp *= M4.rotate(*args)

    def ortho(self, *args):
        self.mvp *= M4.ortho(*args)

    def draw(self):
        self.shader.bind(
            {'MVP': ('Matrix4fv', 1, Shader.FALSE, self.mvp.m)}
        )

        glDrawArrays(GL_TRIANGLES, 0, 3)
