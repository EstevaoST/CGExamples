import math

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from Ponto import Ponto
from Linha import Linha

translacaoX = 0
translacaoY = 0

left = 0
right = 0
top = 0
bottom = 0
panX = 0
panY = 0

l1 = Linha(Ponto(0.1, 0.9), Ponto(0.9, 0.1))
l2 = Linha(Ponto(0.1, 0.1), Ponto(0.9, 0.9))
l1.collide = CollisionLines(l1.a, l1.b, l2.a, l2.b)
l2.collide = l1.collide

def desenhaEixos():
    global left, right
    glColor3f(1, 1, 1)
    glLineWidth(1)

    glBegin(GL_LINES)
    glVertex2f(left, 0)
    glVertex2f(right, 0)
    glVertex2f(0, bottom)
    glVertex2f(0, top)
    glEnd()

    return
def desenhaLinhas():
    glPushMatrix()
    
    glLineWidth(2)

    glBegin(GL_LINES)

    if l1.collide:
        glColor3f(1, 0, 0)
    else:
        glColor3f(0, 1, 0)
    glVertex2f(l1.a.x, l1.a.y)
    glVertex2f(l1.b.x, l1.b.y)    

    if l2.collide:
        glColor3f(1, 0, 0)
    else:
        glColor3f(0, 1, 0)
    glVertex2f(l2.a.x, l2.a.y)
    glVertex2f(l2.b.x, l2.b.y)    
    
    glEnd()
    glPopMatrix()

def Desenha():
    global translacaoX, translacaoY, left, right, top, bottom, panX, panY

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(left + panX, right + panX, bottom + panY, top + panY)
    glMatrixMode(GL_MODELVIEW)

    # Limpa a janela de visualização com a cor branca
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    
    glPushMatrix()
    glLoadIdentity()
    desenhaEixos()    
    glPopMatrix()

    desenhaLinhas()
    
    # Executa os comandos OpenGl
    glFlush()

    return
def Animate():
    glutPostRedisplay()

# Função callback chamada para gerenciar eventos de teclas
def Teclado(key: chr, x: int, y: int):
    if key == 27:
        exit(0)

    return

def TeclasEspeciais(key: int, x: int, y: int):
    global translacaoX, translacaoY, left, right, top, bottom, panX, panY

    if key == GLUT_KEY_LEFT:
        translacaoX -= 0.1

    if key == GLUT_KEY_RIGHT:
        translacaoX += 0.1

    if key == GLUT_KEY_UP:
        translacaoY += 0.1

    if key == GLUT_KEY_DOWN:
        translacaoY -= 0.1

    if key == GLUT_KEY_END:
        left -= 0.1
        right += 0.1
        top += 0.1
        bottom -= 0.1

    if key == GLUT_KEY_HOME:
        left += 0.1
        right -= 0.1
        top -= 0.1
        bottom += 0.1

    if key == GLUT_KEY_F9:
        panX += 0.1

    if key == GLUT_KEY_F10:
        panX -= 0.1

    if key == GLUT_KEY_F11:
        panY += 0.1

    if key == GLUT_KEY_F12:
        panY -= 0.1

    # Redesenha
    glutPostRedisplay()
    return

def Mouse(mbutton: int, mstate: int, x: int, y: int):
    if (mstate != GLUT_DOWN): 
        return
    if (mbutton != GLUT_LEFT_BUTTON):
        return    

    PontoClicado = ScreenToWorldPoint(x, y)
    print(str(PontoClicado.x) + "," + str(PontoClicado.y))
    l2.b = PontoClicado

    l1.collide = CollisionLines(l1.a, l1.b, l2.a, l2.b)
    l2.collide = l1.collide

    glutPostRedisplay()

# Funções de colisão
def ScreenToWorldPoint(x: int, y: int) -> Ponto:
    # Converte a coordenada de tela para o sistema de coordenadas do glOrtho
    vport = glGetIntegerv(GL_VIEWPORT)
    mvmatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    projmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
    realY = vport[3] - y
    worldCoordinate1 = gluUnProject(x, realY, 0, mvmatrix, projmatrix, vport)

    PontoClicado = Ponto (worldCoordinate1[0], worldCoordinate1[1])
    return PontoClicado
def CollisionLines(a1:Ponto, a2:Ponto, b1:Ponto, b2:Ponto) -> bool:    
    uA = ((b2.x-b1.x)*(a1.y-b1.y) - (b2.y-b1.y)*(a1.x-b1.x)) / ((b2.y-b1.y)*(a2.x-a1.x) - (b2.x-b1.x)*(a2.y-a1.y))
    uB = ((a2.x-a1.x)*(a1.y-b1.y) - (a2.y-a1.y)*(a1.x-b1.x)) / ((b2.y-b1.y)*(a2.x-a1.x) - (b2.x-b1.x)*(a2.y-a1.y))

    #intersectionX = x1 + (uA * (a2.x-a1.x));
    #intersectionY = y1 + (uA * (a2.y-a1.y));

    if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
        return True
    return False

# Inicialização
def Inicializa():
    global left, right, top, bottom, panX, panY

    glMatrixMode(GL_PROJECTION)
    left = -1
    right = 1
    top = 1
    bottom = -1
    gluOrtho2D(left + panX, right + panX, bottom + panY, top + panY)
    glMatrixMode(GL_MODELVIEW)

    return

def main():
    glutInit(sys.argv)

    # Define do modo de operação da GLUT
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)

    # Especifica o tamanho inicial em pixels da janela GLUT
    glutInitWindowSize(800, 800)

    # Cria a janela passando como argumento o título da mesma
    glutCreateWindow("Desenha OpenGL")

    # Registra a função callback de redesenho da janela de visualização
    glutDisplayFunc(Desenha)
    glutIdleFunc(Animate)

    # Registra a função callback para tratamento das teclas ASCII
    glutKeyboardFunc(Teclado)
    glutSpecialFunc(TeclasEspeciais)
    glutMouseFunc(Mouse)

    # Chama a função responsável por fazer as inicializações
    Inicializa()

    try:
        # Inicia o processamento e aguarda interações do usuário
        glutMainLoop()
    except SystemExit:
        pass


if __name__ == '__main__':
    main()
