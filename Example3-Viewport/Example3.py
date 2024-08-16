# ***********************************************************************************
#   ExibePoligonos.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa exibe um polígono em OpenGL
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
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
    glPushMatrix()
    glTranslate(x, y, 0)
    
    glBegin(GL_QUADS)    
    glVertex2f(0, 0)
    glVertex2f(w, 0)
    glVertex2f(w, h)
    glVertex2f(0, h)
    glEnd()    
    glPopMatrix()

def reshape(w: int, h: int):
    global vpX, vpY
    glViewport(vpX, vpY, 200, 200)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def display():    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode (GL_MODELVIEW)    
        
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
    def __init__(self,x, y,  w, h,  c = (1,0,0)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c

# Variaveis Globais
nFrames, TempoTotal, AccumDeltaT = 0, 0, 0
oldTime = time.time()
squares = [Square(  0,  0, 30,30, (1,0,0)), Square(60 , 30 , 30,30, (1,0,1)),
           Square( 40, 80, 30,30, (0,1,0)), Square(90 , 70 , 30,30, (0,1,1)),
           Square( 20,120, 30,30, (0,0,1)), Square(225, 30 , 30,30, (1,0,1)),
           Square(115,210, 30,30, (1,0,0)), Square(312, 112, 30,30, (1,0,1)),
           Square( 50,260, 30,30, (0,1,0)), Square(444, 444, 30,30, (0,1,1)),
           Square( 30,330, 30,30, (0,0,1)), Square(447, 301, 30,30, (1,0,1))]
nSquare = 0
movement = (0,0)
vpX = 0
vpY = 0


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
        vpX = 0
        vpY = 0
        reshape(500,500)

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************
def arrow_keys(a_keys: int, x: int, y: int):
    global vpX, vpY
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP                
        vpY += 10        
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        vpY -= 10
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        vpX -= 10    
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        vpX += 10        
    reshape(500, 500)

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
