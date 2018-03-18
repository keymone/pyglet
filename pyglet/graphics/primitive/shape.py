from OpenGL.GL import *
import numpy

from pyglet.graphics.shader import Shader
from pyglet.math import M4


class Shape:
    def __init__(self):
        self.va = glGenVertexArrays(1)
        glBindVertexArray(self.va)

        self.vbuf = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbuf)

        self.shader = Shader.default_shader()
        self.mvp = M4.identity()

        self.is_dirty = True
        self.write_data()

    def mark_dirty(self):
        self.is_dirty = True

    def get_data(self):
        raise(NotImplemented, "implement in subclass")

    def write_data(self):
        glBindVertexArray(self.va)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbuf)
        vertices = numpy.array(self.get_data(), dtype=numpy.float32)
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
