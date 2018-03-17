import glfw


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

        # Create a windowed mode window and its OpenGL context
        self.window = glfw.create_window(width, height, title, None, None)

        if not self.window:
            glfw.terminate()
            raise Exception("Couldn't create window")

        if make_current:
            glfw.make_context_current(self.window)
            glfw.swap_interval(1)

        glfw.set_key_callback(self.window, key_callback or self.key_callback)

    def should_close(self):
        return glfw.window_should_close(self.window)

    def swap_buffers(self):
        return glfw.swap_buffers(self.window)

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