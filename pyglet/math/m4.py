import numpy
import math

class M4:
    def __init__(self, data=None):
        self.m = numpy.array(data, dtype=numpy.float32).reshape(4, 4)
        self.nbytes = self.m.nbytes

    @staticmethod
    def identity():
        return M4([
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        ])

    @staticmethod
    def translate(x, y, z):
        return M4([
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            x, y, z, 1
        ])

    @staticmethod
    def scale(x, y, z):
        return M4([
            x, 0, 0, 0,
            0, y, 0, 0,
            0, 0, z, 0,
            0, 0, 0, 1
        ])

    @staticmethod
    def rotate(degree):
        ds = math.sin(math.radians(degree))
        dc = math.cos(math.radians(degree))
        return M4([
            dc, ds, 0, 0,
            -ds, dc, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        ])

    @staticmethod
    def ortho(l, r, b, t, n, f):
        return M4([
            2.0/(r-l), 0, 0, 0,
            0, 2.0/(t-b), 0, 0,
            0, 0, -2.0/(f-n), 0,
            -(r+l)/(r-l), -(t+b)/(t-b), -(f+n)/(f-n), 1.0
        ])

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return M4(self.m * other)
        elif isinstance(other, M4):
            return M4(numpy.matmul(self.m, other.m))

    def __repr__(self):
        return "{}".format(self.m)
