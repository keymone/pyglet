import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *


class Window:
    def __init__(self,
                 width=600,
                 height=400,
                 title='glfw',
                 make_current=True,
                 key_callback=None):
        self.width = width
        self.height = height
        self.title = title

        if not glfw.init():
            raise Exception("Couldn't init glfw")

        # glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        # glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
        # glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        # glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        # Create a windowed mode window and its OpenGL context
        self.window = glfw.create_window(width, height, title, None, None)

        if not self.window:
            glfw.terminate()
            raise Exception("Couldn't create window")

        if make_current:
            glfw.make_context_current(self.window)
            glfw.swap_interval(1)

        glfw.set_key_callback(self.window, key_callback or self.key_callback)

        self.time = self.get_time()

        print("OpenGL: " + str(glGetString(GL_VERSION)))

    def should_close(self):
        return glfw.window_should_close(self.window)

    def swap_buffers(self):
        return glfw.swap_buffers(self.window)

    def clear(self):
        glViewport(0, 0, self.width, self.height)
        glClear(GL_COLOR_BUFFER_BIT)

    @staticmethod
    def key_callback(window, key, _scancode, action, _mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    @staticmethod
    def poll_events():
        glfw.poll_events()

    @staticmethod
    def terminate():
        glfw.terminate()

    @staticmethod
    def get_time():
        return glfw.get_time()

    def get_time_delta(self):
        time = self.get_time()
        delta = time - self.time
        self.time = time
        return delta
