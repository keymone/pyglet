from OpenGL.GL import *
from OpenGL.GL import shaders
import ctypes


class Shader:
    def __init__(self, vsrc, fsrc):
        self.uniforms = {}
        self.attribs = {}
        self.prog = shaders.compileProgram(
            shaders.compileShader(vsrc, GL_VERTEX_SHADER),
            shaders.compileShader(fsrc, GL_FRAGMENT_SHADER),
        )
        glLinkProgram(self.prog)

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

            f = globals()['glUniform' + t]
            f(u, *v[1:])

    @staticmethod
    def default_shader():
        shader = Shader(
            vsrc="""
                #version 330 core

                uniform mat4 MVP;
                in vec4 vCol;
                in vec4 vPos;

                out vec4 color;

                void main()
                {
                    gl_Position = MVP * vPos;
                    color = vCol;
                }
            """,
            fsrc="""
                #version 330 core

                in vec4 color;
                out vec4 fragColor;

                void main()
                {
                    fragColor = color;
                }
            """
        )

        shader.def_uniform("MVP")
        shader.def_attrib("vPos", {'size': 4, 'stride': 8})
        shader.def_attrib("vCol", {'size': 4, 'stride': 8, 'offset': 4})

        return shader
