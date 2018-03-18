import random
import time

from threading import Thread, RLock
from IPython import embed
from pyglet.graphics.window import Window
from pyglet.graphics.primitive.triangle import Triangle
from pyglet.graphics.primitive.vc import VC


def main():
    window = Window()
    ratio = float(window.width) / window.height

    lock = RLock()
    entities = []

    def append_entity(e, ortho=True):
        if ortho:
            e.ortho(-ratio, ratio, -1, 1, 1, -1)

        with lock:
            entities.append(e)

    def pop_entity(i=0):
        with lock:
            return entities.pop(i)

    append_entity(
        Triangle(
            VC([0, 0], [1, 0, 0]),
            VC([0, 1], [0, 1, 0]),
            VC([1, 0], [0, 0, 1])
        ),
    )

    repl_t = Thread(
        target=embed,
        kwargs=dict(user_ns=locals())
    )
    repl_t.daemon = True
    repl_t.start()

    while not window.should_close():
        window.clear()

        # delta = window.get_time_delta()

        with lock:
            for ent in entities:
                ent.draw()

        window.swap_buffers()
        Window.poll_events()

    Window.terminate()


if __name__ == "__main__":
    main()
