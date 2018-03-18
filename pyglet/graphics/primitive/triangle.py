from OpenGL.GL import *
import numpy

from pyglet.graphics.shader import Shader
from pyglet.math import M4


class Triangle:
    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c

        self.va = glGenVertexArrays(1)
        glBindVertexArray(self.va)

        self.vbuf = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbuf)

        self.shader = Shader.default_shader()
        self.mvp = M4.identity()

        self.is_dirty = True
        self.write_data()

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, val):
        if self._a != val:
            self.is_dirty = True
            self._a = val

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, val):
        if self._b != val:
            self.is_dirty = True
            self._b = val

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, val):
        if self._c != val:
            self.is_dirty = True
            self._c = val

    def write_data(self):
        glBindVertexArray(self.va)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbuf)

        vertices = numpy.array([
            *self._a.pos, *self._a.col,
            *self._b.pos, *self._b.col,
            *self._c.pos, *self._c.col,
        ], dtype=numpy.float32)

        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

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
        if self.is_dirty:
            self.write_data()

        self.shader.bind({'MVP': ('Matrix4fv', 1, Shader.FALSE, self.mvp.m)})
        glBindVertexArray(self.va)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glBindVertexArray(0)
