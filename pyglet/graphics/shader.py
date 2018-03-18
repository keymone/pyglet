from OpenGL.GL import *
import OpenGL.GL as GL
import ctypes


class Shader:
    def __init__(self, vsrc, fsrc):
        self.uniforms = {}
        self.attribs = {}
        self.prog = glCreateProgram()
        vshader = self.compile(vsrc, GL_VERTEX_SHADER)
        fshader = self.compile(fsrc, GL_FRAGMENT_SHADER)
        glLinkProgram(self.prog)
        glDeleteShader(vshader)
        glDeleteShader(fshader)

    def compile(self, src, kind):
        shader = glCreateShader(kind)
        glShaderSource(shader, src)
        glCompileShader(shader)
        status = ctypes.c_int()
        glGetShaderiv(shader, GL_COMPILE_STATUS, ctypes.byref(status))

        if not status.value:
            print(glGetShaderInfoLog(shader))
            glDeleteShader(shader)
            raise (ValueError, 'Shader compilation failed')

        glAttachShader(self.prog, shader)

        return shader

    def def_uniform(self, uname):
        glUseProgram(self.prog)
        self.uniforms[uname] = glGetUniformLocation(self.prog, uname)

    TYPES = {
        float: GL_FLOAT
    }

    SIZES = {
        float: 4
    }

    FALSE = GL_FALSE
    TRUE = GL_TRUE

    def def_attrib(self, aname, pointer=None):
        self.attribs[aname] = glGetAttribLocation(self.prog, aname)

        if pointer:
            ptype = pointer.get('type', float)
            type_gl = self.TYPES[ptype]
            size_gl = self.SIZES[ptype]

            glEnableVertexAttribArray(self.attribs[aname])
            glVertexAttribPointer(
                self.attribs[aname],
                pointer['size'],
                type_gl,
                GL_FALSE if pointer.get('normalized') else GL_TRUE,
                size_gl * pointer.get('stride', 0),
                ctypes.c_void_p(size_gl * pointer.get('offset', 0))
            )

    def bind(self, ub):
        glUseProgram(self.prog)

        for k, v in ub.items():
            u = self.uniforms[k]
            t = v[0]

            f = getattr(OpenGL.GL, 'glUniform' + t)
            f(u, *v[1:])
