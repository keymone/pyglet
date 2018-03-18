from OpenGL.GL import glDrawArrays, GL_TRIANGLES
import numpy

from pyglet.graphics.primitive.shape import Shape


class Triangle(Shape):
    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c
        super().__init__()

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, val):
        if self._a != val:
            self.dirty_data = True
            self._a = val

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, val):
        if self._b != val:
            self.dirty_data = True
            self._b = val

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, val):
        if self._c != val:
            self.dirty_data = True
            self._c = val

    def get_data(self):
        return numpy.array([
            *self._a.pos, *self._a.col,
            *self._b.pos, *self._b.col,
            *self._c.pos, *self._c.col,
        ], dtype=numpy.float32)

    def draw(self):
        super().draw()
        glDrawArrays(GL_TRIANGLES, 0, 3)
