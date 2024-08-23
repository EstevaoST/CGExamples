from OpenGL.GL import *
from Ponto import Ponto

class Triangulo:
    def __init__(self, a: Ponto, b: Ponto, c: Ponto):
        self.a = a
        self.b = b
        self.c = c

    def movef(self, mx: float, my: float):
        self.a.x += mx
        self.b.x += mx
        self.c.x += mx
        self.a.y += my
        self.b.y += my
        self.c.y += my

    def movep(self, m: Ponto):
        self.movef(m.x, m.y)

    def desenha(self):
        glBegin(GL_LINE_LOOP)

        glVertex2f(self.a.x, self.a.y)
        glVertex2f(self.b.x, self.b.y)
        glVertex2f(self.c.x, self.c.y)

        glEnd()