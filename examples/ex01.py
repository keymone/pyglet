from pyglet.graphics.window import Window
from pyglet.graphics.shader import Shader
from pyglet.graphics.primitive.triangle import Triangle
from pyglet.graphics.primitive.point import Point2
from pyglet.math.m4 import M4
import numpy

from OpenGL.GL import *


def main():
    window = Window()
    ratio = float(window.width) / window.height
    tri = Triangle(
        Point2((-0.6, -0.4), (1, 0, 0)),
        Point2((0.6, -0.4), (0, 1, 0)),
        Point2((0, 0.6), (0, 0, 1))
    )

    while not window.should_close():
        window.clear()

        tri.reset()
        tri.rotate(window.get_time())
        tri.ortho(-ratio, ratio, -1, 1, 1, -1)
        tri.draw()

        window.swap_buffers()
        Window.poll_events()

    Window.terminate()


if __name__ == "__main__":
    main()
