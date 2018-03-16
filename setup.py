from setuptools import setup

setup(
    name='pyglet',
    version='0.1',
    description='Python game library',
    author='Maksym Melnychok',
    author_email='keymone@gmail.com',
    packages=['pyglet'],
    install_requires=[
        'glfw',
        'PyOpenGL',
    ],
)
