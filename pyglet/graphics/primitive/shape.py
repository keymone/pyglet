from OpenGL.GL import *
import numpy

from pyglet.graphics.shader import Shader
from pyglet.math import M4


class Shape:
    def __init__(self):
        self.va = None
        self.vbuf = None
        self.shader = None
        self.mvp = M4.identity()

        self.ready = False
        self.dirty_data = True
        self.dirty_mvp = True

    def setup(self):
        self.va = glGenVertexArrays(1)
        glBindVertexArray(self.va)

        self.vbuf = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbuf)

        self.shader = Shader.default_shader()

    def mark_dirty_data(self):
        self.dirty_data = True

    def mark_dirty_mvp(self):
        self.dirty_mvp = True

    def get_data(self):
        raise(NotImplemented, "implement in subclass")

    def sync(self):
        if self.dirty_data:
            glBindVertexArray(self.va)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbuf)
            vertices = numpy.array(self.get_data(), dtype=numpy.float32)
            glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
            self.dirty_data = False

        if self.dirty_mvp:
            self.shader.bind({'MVP': ('Matrix4fv', 1, Shader.FALSE, self.mvp.m)})
            self.dirty_mvp = False

    def reset(self):
        self.dirty_mvp = True
        self.mvp = M4.identity()

    def rotate(self, *args):
        self.dirty_mvp = True
        self.mvp.mul(M4.rotate(*args), self.mvp)

    def ortho(self, *args):
        self.dirty_mvp = True
        self.mvp *= M4.ortho(*args)

    def translate(self, *args):
        self.dirty_mvp = True
        self.mvp *= M4.translate(*args)

    def scale(self, *args):
        self.dirty_mvp = True
        self.mvp *= M4.scale(*args)

    def draw(self):
        if not self.ready:
            self.setup()
            self.ready = True

        self.sync()
        glBindVertexArray(self.va)
