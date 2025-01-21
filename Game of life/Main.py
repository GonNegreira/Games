import pygame
import random

# Funciones
def crearMatriz(n, m, aleatorio=True):
    matriz = []
    for i in range(n):
        fila = []
        for j in range(m):
            if aleatorio:
                if tirarDado(2):
                    fila.append(1)
                else:
                    fila.append(0)
            else:
                fila.append(0)
        matriz.append(fila)
    return matriz

def tirarDado(caras:int):
    return random.randint(0, caras-1) == caras-1

def dibujarMatriz():
    global pantalla
    pantalla.fill(negro)
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            x = j * dimCelda
            y = i * dimCelda
            if matriz[i][j] == 1:
                pygame.draw.rect(pantalla, blanco, pygame.Rect(x, y, dimCelda, dimCelda))

def generarNuevaGeneracion():
    global matriz
    nuevaGeneracion = crearMatriz(dimMatriz, dimMatriz, False)  # Matriz vacía
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            viva = matriz[i][j] == 1
            cantidadVecinos = contarVecinos((i, j))
            if viva:
                # Sobrevive si tiene 2 o 3 vecinos vivos
                nuevaGeneracion[i][j] = 1 if cantidadVecinos in (2, 3) else 0
            else:
                # Revive si tiene exactamente 3 vecinos vivos
                nuevaGeneracion[i][j] = 1 if cantidadVecinos == 3 else 0
            if generacionEspontanea and tirarDado(1000):
                nuevaGeneracion[i][j] = 1
    matriz = nuevaGeneracion

def contarVecinos(celula):
    (y, x) = celula
    # Coordenadas de los posibles desplazamientos a los vecinos
    desplazamientos = [(-1, -1), (-1, 0), (-1, 1), 
                       (0, -1),         (0, 1), 
                       (1, -1), (1, 0), (1, 1)]
    contador = 0
    for dy, dx in desplazamientos:
        ny, nx = y + dy, x + dx
        if enRango(ny) and enRango(nx):  # Verifica si está dentro de los límites de la matriz
            if matriz[ny][nx] == 1:
                contador += 1
    return contador

def enRango(numero):
    return -1 < numero and numero < dimMatriz

def manejarTecleado(keys):
    global iniciado, matriz, generacionEspontanea
    if keys[pygame.K_SPACE]:
        iniciado = not(iniciado)
    if keys[pygame.K_v]:
        matriz = crearMatriz(dimMatriz, dimMatriz, False)
    if keys[pygame.K_r]:
        matriz = crearMatriz(dimMatriz, dimMatriz, True)
    if keys[pygame.K_a]:
        generacionEspontanea = not(generacionEspontanea)

def manejarClick(mouse_pos):
    global matriz
    x, y = mouse_pos
    j = int(x // dimCelda)
    i = int(y // dimCelda)
    if enRango(i) and enRango(j):
        matriz[i][j] = 1 if matriz[i][j] == 0 else 0  # Alternar entre 0 y 1

# Matriz
dimMatriz = 150
matriz = crearMatriz(dimMatriz, dimMatriz)

# Pantalla
altoPantalla, anchoPantalla = 800, 800
pantalla = pygame.display.set_mode((altoPantalla, anchoPantalla))
dimCelda = altoPantalla/dimMatriz

# Colores
negro = (0, 0, 0)
blanco = (255, 255, 255)

# Variables miscleaneas
iniciado = False
generacionEspontanea = False

# Main loop
ejecutando = True
while ejecutando:

    # Manejo de Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            manejarClick(evento.pos)
    
    # Manejo de tecleados
    keys = pygame.key.get_pressed()
    manejarTecleado(keys)


    # Dibujo de Matriz
    dibujarMatriz()
    pygame.display.flip()
    if iniciado:
        generarNuevaGeneracion()