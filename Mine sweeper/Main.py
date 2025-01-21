import pygame
import math
import random

# Clases
class Celda:
    def __init__(self, i, j, dimCelda):
        self.i = i  # Fila
        self.j = j  # Columna
        self.y = i*dimCelda
        self.x = j*dimCelda
        self.bomba = False
        self.visible = False
        self.bandera = False
        self.cantidadVecinos = -1
        self.textCantidadVecinos = fuente.render(str(self.cantidadVecinos), True, negro)

    def plantarBomba(self):
        self.bomba = True

    def contarVecinos(self):
        total = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                i = self.i + dx
                j = self.j + dy
                if enRango(i) and enRango(j):
                    if cuadricula[i][j].bomba:
                        total += 1
        self.cantidadVecinos = total
        self.textCantidadVecinos = fuente.render(str(self.cantidadVecinos), True, negro)

    def mostrar(self):
        self.visible = True
        if self.cantidadVecinos == 0:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    i = self.i + dx
                    j = self.j + dy
                    if enRango(i) and enRango(j):
                        vecino = cuadricula[i][j]
                        if not(vecino.bomba) and not(vecino.visible):
                            vecino.mostrar()
    
    def dibujar(self):
        if self.visible:
            if self.bomba:
                pantalla.blit(CeldaVisibleBomba, (self.x, self.y))
            elif self.cantidadVecinos == 0:
                pantalla.blit(CeldaVisible, (self.x, self.y))
            else:
                pantalla.blit(CeldaVisible, (self.x, self.y))
                pantalla.blit(self.textCantidadVecinos, (self.x + fontsize-1, self.y + fontsize-1))
        else:
            pantalla.blit(CeldaNoVisible, (self.x, self.y))

# Funciones
def crearCuadricula():
    cuadricula = []
    for i in range(n):
        fila = []
        for j in range(n):
            nuevaCelda = Celda(i, j, dimCelda)
            fila.append(nuevaCelda)
        cuadricula.append(fila)
    return cuadricula

def plantarBombasEnCuadricula():
    bombasPorPlantar = cantidadBombas
    while bombasPorPlantar > 0:
        j = random.randint(0, n-1)
        i = random.randint(0, n-1)
        if not(cuadricula[i][j].bomba):
            cuadricula[i][j].plantarBomba()
            bombasPorPlantar -= 1
            
def dibujarCuadricula():
    pantalla.fill(gris)
    for i in range(n):
        for j in range(n):
            celda = cuadricula[i][j]
            celda.dibujar()

def enRango(numero):
    return -1 < numero and numero < n

def manejarClick(mouse_pos):
    global cuadricula
    x, y = mouse_pos
    i = int(y // dimCelda)
    j = int(x // dimCelda)
    if enRango(i) and enRango(j):
        celda = cuadricula[i][j]
        if celda.bomba:
            finJuego()
        celda.mostrar()

def finJuego():
    for i in range(n):
        for j in range(n):
            cuadricula[i][j].mostrar()

def contarTodosVecinos():
    for i in range(n):
        for j in range(n):
            celda = cuadricula[i][j]
            celda.contarVecinos()

def tecleado(keys):
    if keys[pygame.K_r]:
        reiniciar()

def reiniciar():
    global cuadricula
    cuadricula = crearCuadricula()
    plantarBombasEnCuadricula()
    contarTodosVecinos()

# Variables Global
pygame.font.init()

# Pantalla
altoPantalla = 800
anchoPantalla = 800
pantalla = pygame.display.set_mode((anchoPantalla, altoPantalla))

# Celdas
cantidadCeldas = 49
n = int(math.sqrt(cantidadCeldas))
dimCelda = altoPantalla // n +1

# Bombas
cantidadBombas = 10

# Colores
negro = (0, 0, 0)
gris = (200, 200, 200)

# Fuente
fontsize = 48
fuente = pygame.font.Font(None, fontsize)

# Cuadricula
cuadricula = crearCuadricula()
plantarBombasEnCuadricula()
contarTodosVecinos()

# Sprites
tamaño = (dimCelda, dimCelda)
CeldaNoVisible = pygame.transform.scale(pygame.image.load(r".\Sprites\CeldaNoVisible.png").convert_alpha(), tamaño)
CeldaVisible = pygame.transform.scale(pygame.image.load(r".\Sprites\CeldaVisible.png").convert_alpha(), tamaño)
CeldaVisibleBomba = pygame.transform.scale(pygame.image.load(r".\Sprites\CeldaVisibleBomba.png").convert_alpha(), tamaño)

# Bucle Principal
ejecutando = True
while ejecutando:
    
    # manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            manejarClick(evento.pos)
    
    # manejo de teclas
    keys = pygame.key.get_pressed()
    tecleado(keys)

    # Dibujo
    dibujarCuadricula()
    pygame.display.flip()
