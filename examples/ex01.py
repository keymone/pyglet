import random
import time

from pyglet.graphics import Window
from pyglet.graphics.primitive import Triangle
from pyglet.graphics.primitive import VC


def main():
    window = Window()
    ratio = float(window.width) / window.height

    tris = [
        (
            Triangle(
                VC([random.random(), random.random()], [1, 0, 0]),
                VC([random.random(), random.random()], [0, 1, 0]),
                VC([random.random(), random.random()], [0, 0, 1])
            ),
            50*(random.random()-0.5)
        )
        for _ in range(1000)
    ]
    for tri, _ in tris:
        tri.ortho(-ratio, ratio, -1, 1, 1, -1)

    while not window.should_close():
        window.clear()

        delta = window.get_time_delta()

        start = time.time()

        for tri, angle in tris:
            tri.rotate(angle*delta)
            tri.draw()

        print("%.5f" % (time.time() - start))

        window.swap_buffers()
        Window.poll_events()

    Window.terminate()


if __name__ == "__main__":
    main()
