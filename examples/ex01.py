from pyglet.graphics.window import Window
from pyglet.graphics.primitive.triangle import Triangle
from pyglet.graphics.primitive.point import Point


def main():
    window = Window()
    ratio = float(window.width) / window.height

    tri = Triangle(
        Point((-0.6, -0.4), (1, 0, 0)),
        Point((0.6, -0.4), (0, 1, 0)),
        Point((0, 0.6), (0, 0, 1))
    )
    tri.ortho(-ratio, ratio, -1, 1, 1, -1)

    tri2 = Triangle(
        Point((0, 0), (1, 0, 0)),
        Point((0, 1), (0, 1, 0)),
        Point((1, 0), (0, 0, 1))
    )
    tri2.ortho(-ratio, ratio, -1, 1, 1, -1)

    while not window.should_close():
        window.clear()

        tri.rotate(window.get_time_delta()*10)
        tri.draw()
        tri2.draw()

        window.swap_buffers()
        Window.poll_events()

    Window.terminate()


if __name__ == "__main__":
    main()
