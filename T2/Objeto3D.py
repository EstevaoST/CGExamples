from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from Ponto import *

class Objeto3D:
        
    def __init__(self):
        self.vertices = []
        pass

    def LoadFile(self, file:str):
        f = open(file, "r")

        for line in f:
            values = line.split(' ')
            if values[0] == 'v':
                self.vertices.append(Ponto(float(values[1]),
                                           float(values[2]),
                                           float(values[3])))
                print(self.vertices[-1].x, self.vertices[-1].y, self.vertices[-1].z)
        pass

    def Desenha(self):
        glPushMatrix()
        glColor3f(1, 0, 0)
        glPointSize(5)
        glBegin(GL_POINTS)
        for v in self.vertices:
            glVertex(v.x, v.y, v.z)
        glEnd()
        glPopMatrix()
        pass