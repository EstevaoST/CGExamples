# ***********************************************************************************
#   Example2.py
#       Autor: Estêvão Smania Testa (baseado no código de Márcio Sarroglia Pinho)
#
#   Este programa exibe polígonos em OpenGL e permite movelos
#
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
#
#   No caso de usar no MacOS, pode ser necessário alterar o arquivo ctypesloader.py,
#   conforme a descrição que está nestes links:
#   https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos
#   https://stackoverflow.com/questions/6819661/python-location-on-mac-osx
#   Veja o arquivo Patch.rtf, armazenado na mesma pasta deste fonte.
# ***********************************************************************************

import os
import time

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def square(x,y, w,h):
    glLoadIdentity()     
    
    glTranslate(x, y, 0)
    
    glBegin(GL_QUADS)    
    glVertex2f(0, 0)
    glVertex2f(w, 0)
    glVertex2f(w, h)
    glVertex2f(0, h)
    glEnd()    

def reshape(w: int, h: int):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()     
    
    for sqr in squares:
        glColor3f(sqr.c[0], sqr.c[1], sqr.c[2])
        square(sqr.x, sqr.y, sqr.w, sqr.h)
        
    glColor3f(1.0, 0.0, 0.0)

    glutSwapBuffers()

# **********************************************************************
# animate()
# Funcao chama enquanto o programa esta ocioso
# Calcula o FPS
#
# **********************************************************************
class Square:
    def __init__(self, w, h):
        self.x = 0
        self.y = 0
        self.w = w
        self.h = h
        self.c = (1,0,0)

# Variaveis Globais
nFrames, TempoTotal, AccumDeltaT = 0, 0, 0
oldTime = time.time()
squares = [Square(100,100)]
nSquare = 0
movement = (0,0)

def animate():
    global nFrames, TempoTotal, AccumDeltaT, oldTime

    nowTime = time.time()
    dt = nowTime - oldTime
    oldTime = nowTime

    AccumDeltaT += dt
    TempoTotal += dt
    nFrames += 1
    
    if AccumDeltaT > 1.0/30:  # fixa a atualizaÃ§Ã£o da tela em 30
        AccumDeltaT = 0
        glutPostRedisplay()


# **********************************************************************
# The function called whenever a key is pressed. 
# # Note the use of Python tuples to pass in: (key, x, y)
# 
# **********************************************************************
ESCAPE = b'\x1b'
def getKey(*args):
    global squares, nSquare
    #print (args)
    # If escape is pressed, kill everything.
    if args[0] == b'q':
        os._exit(0)
    if args[0] == ESCAPE:
        os._exit(0)
    if args[0] == b' ':
        squares.append(Square(100,100))
        nSquare += 1
        squares[nSquare].c = (nSquare / 9 % 3 / 2.0, 
                              nSquare / 3 % 3 / 2.0,
                              nSquare % 3 / 2.0)
        
        print(nSquare)

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************
def arrow_keys(a_keys: int, x: int, y: int):
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP                
        squares[nSquare].y += 10
        pass
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        squares[nSquare].y -= 10
        pass
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        squares[nSquare].x -= 10
        pass
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        squares[nSquare].x += 10
        pass

    glutPostRedisplay()

# ***********************************************************************************
#
# ***********************************************************************************
def mouse(button: int, state: int, x: int, y: int):
    if (state != GLUT_DOWN): 
        return
    if (button != GLUT_RIGHT_BUTTON):
        return
    print ("Mouse:", x, ",", y)

    vport = glGetIntegerv(GL_VIEWPORT)
    mvmatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    projmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
    realY = vport[3] - y
    worldCoordinate1 = gluUnProject(x, realY, 0, mvmatrix, projmatrix, vport)

    print ("Ponto: ", worldCoordinate1)
    
    glutPostRedisplay()

# ***********************************************************************************
#
# ***********************************************************************************
def mouseMove(x: int, y: int):
    glutPostRedisplay()

# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

glutInit(sys.argv)
#glutInit()
glutInitDisplayMode(GLUT_RGBA|GLUT_DEPTH | GLUT_RGB)
# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(500, 500)
# Cria a janela na tela, definindo o nome da
# que aparecera na barra de tÃ­tulo da janela.
glutInitWindowPosition(100, 100)

wind = glutCreateWindow("Titulo da janela")
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutIdleFunc (animate)
glutKeyboardFunc(getKey)
glutMouseFunc(mouse)
#glutMotionFunc(mouseMove)
glutSpecialFunc(arrow_keys)

try:
	glutMainLoop()
except SystemExit:
	pass
