import pygame
import random
import os

##Funciones##

def generarComida(): # Generar Comida en una casilla vacia
    global comida
    comida = encontrarCasillaVacia()
    actualizarLaberinto(comida, 2)

def encontrarCasillaVacia(): # Devuelve una casilla vacia
    x, y = random.randint(0, t-1), random.randint(0, t-1)
    tupla = (x, y)
    if revisarCasilla(tupla) != 0:
        return encontrarCasillaVacia()
    return tupla

def crearMatriz(t): # Crea una matriz tXt
    matriz = []
    for i in range(t):
        lista = []
        for j in range(t):
            lista.append(0)
        matriz.append(lista)
    return matriz

def bordearMatriz(matriz): # Llena los bordes de una matriz con el valor de Bordes
    t = len(matriz)
    for i in range(t):
        matriz[0][i] = 3 # Tope Arriba
        matriz[i][0] = 4 # Tope Izquierdo
        matriz[t-1][i] = 3 # Tope Abajo
        matriz[i][t-1] = 4 # Tope Derecho
    matriz[0][0], matriz[t-1][t-1], matriz[t-1][0], matriz[0][t-1] = 5, 5, 5, 5
    return matriz

def actualizarLaberinto(tupla, objeto): # Actualiza una posicion del laberito con un objeto
    global laberinto
    (y, x) = tupla
    if x >= len(laberinto):
        x = 0
    laberinto[y][x] = objeto

def sumarTuplas(A,B): # Suma dos tuplas
    (y, x) = A
    (b, a) = B
    return (y+b, x+a)

def restarTuplas(A,B): # Resta dos tuplas
    (y, x) = A
    (b, a) = B
    return (y-b, x-a)

def noSonOpuestas(DirA, DirB): # Devuelve True si dos direcciones no son opuestas
    return (DirA in (arriba, abajo) and DirB in (derecha, izquierda)) or \
        (DirA in (derecha, izquierda) and DirB in (arriba, abajo))

def noEsSuicida(dir): # Devuelve True si la direccion a la cual la cabeza se mueve no apunta a la serpiente
    if revisarCasilla(sumarTuplas(serpiente[0], dir)) == 1:
        return False
    return True

def revisarCasilla(tupla): # Devuelve el objeto guardado en una posicion del laberito
    if tupla is None:
        return 1
    else:
        (y, x) = tupla
        if y >= len(laberinto) or x >= len(laberinto):
            return 1
        return laberinto[y][x]

def cambiarDireccion(dirNueva): # Cambia la direccion
    global direccionActual
    if noSonOpuestas(dirNueva, direccionActual) and noEsSuicida(dirNueva):
        direccionActual = dirNueva

def sumarVelocidad(k):
    global velocidad
    velocidad += k

def tecleado(keys): # Asigna algunas teclas a funciones
    global direccionActual, silenciado
    if keys[pygame.K_UP]:
        cambiarDireccion(arriba)
    elif keys[pygame.K_DOWN]:
        cambiarDireccion(abajo)
    elif keys[pygame.K_LEFT]:
        cambiarDireccion(izquierda)
    elif keys[pygame.K_RIGHT]:
        cambiarDireccion(derecha)
    elif keys[pygame.K_b]:
        sumarVelocidad(-50)
    elif keys[pygame.K_s]:
        sumarVelocidad(50)
    elif keys[pygame.K_r]:
        automordida()
    elif keys[pygame.K_m]:
        silenciado = True

def dibujarLaberinto(serpienteViva): # Recorre el laberinto, bliteando en la paantalla la imagen correcta (dependiendo de posicion y si la serpiente esta viva o no)
    global pantalla, laberinto
    pantalla.fill(Blanco)
    for i in range(len(laberinto)):
        for j in range(len(laberinto[i])):
            x = j * dimCelda
            y = i * dimCelda
            casilla = (i, j)
            contenidoCasilla = revisarCasilla(casilla)
            if (i+j)%2 == 0:
                pygame.draw.rect(pantalla, Gris, pygame.Rect(x, y, dimCelda, dimCelda))
            else:
                pass
            if contenidoCasilla == 1:         # Parte de la serpiente

                if casilla == serpiente[0]:     # Cabeza
                    dibujarCabeza(x, y, serpienteViva)
                elif casilla == serpiente[-1]:  # Cola
                    dibujarCola(x, y, casilla, serpienteViva)
                else:                           # Cuerpo
                    dibujarCuerpo(x, y, casilla, serpienteViva)

            elif contenidoCasilla == 2:  # Comida
                pantalla.blit(Manzana, (x, y))

            elif contenidoCasilla == 3: # Borde Horizontal
                pantalla.blit(BordeHorizontal, (x, y))
            elif contenidoCasilla == 4: # Borde Vertical
                pantalla.blit(BordeVertical, (x, y))
            elif contenidoCasilla == 5: # Borde Esquina
                pantalla.blit(BordeEsquina, (x, y))
                
def dibujarCabeza(x, y, serpienteViva): # Dibuja la cabeza de la serpiente
    if serpienteViva:
        if direccionActual == arriba:
            imagen = CabezaArriba
        elif direccionActual == abajo:
            imagen = CabezaAbajo
        elif direccionActual == derecha:
            imagen = CabezaDerecha
        else:
            imagen = CabezaIzquierda
    else:
        if direccionActual == arriba:
            imagen = CabezaArribaMuerta
        elif direccionActual == abajo:
            imagen = CabezaAbajoMuerta
        elif direccionActual == derecha:
            imagen = CabezaDerechaMuerta
        else:
            imagen = CabezaIzquierdaMuerta
    pantalla.blit(imagen, (x, y))
    
def getImagenGiro(cy, cx, py, px, ny, nx, serpienteViva):
    if serpienteViva: 
        if (cy == ny and cy < py) and (cx == px and cx < nx) or \
        (cy == py and cy < ny) and (cx == nx and cx < px) : # Codo DR
            return dr
        elif (cy == py and cy > ny) and (cx == nx and cx > px) or \
        (cy == ny and cy > py) and (cx == px and cx > nx): # Codo UL
            return ul
        elif (cy == ny and cy > py) and (cx == px and cx < nx) or \
        (cy == py and cy > ny) and (cx == nx and cx < px): # Codo UR
            return ur
        else:
            return dl # codo DL
    else:
        if (cy == ny and cy < py) and (cx == px and cx < nx) or \
        (cy == py and cy < ny) and (cx == nx and cx < px) : # Codo DR
            return drMuerta
        elif (cy == py and cy > ny) and (cx == nx and cx > px) or \
        (cy == ny and cy > py) and (cx == px and cx > nx): # Codo UL
            return ulMuerta
        elif (cy == ny and cy > py) and (cx == px and cx < nx) or \
        (cy == py and cy > ny) and (cx == nx and cx < px): # Codo UR
            return urMuerta
        else:
            return dlMuerta # codo DL

def dibujarCuerpo(x, y, casilla, serpienteViva):
    idx = serpiente.index(casilla)
    prev_segment = serpiente[idx - 1]
    next_segment = serpiente[idx + 1]
    cx, cy = casilla[1], casilla[0]
    px, py = prev_segment[1], prev_segment[0]
    nx, ny = next_segment[1], next_segment[0]
    if py == ny and serpienteViva:      # Horizontal viva
        imagen = CuerpoHorizontal
    elif py == ny:                      # Horizontal Muerta
        imagen = CuerpoHorizontalMuerta
    elif px == nx and serpienteViva:    # Vertical
        imagen = CuerpoVertical    
    elif px == nx:                      # Vertical muerta
        imagen = CuerpoVerticalMuerta 
    else:  # Giros
        imagen = getImagenGiro(cy, cx, py, px, ny, nx, serpienteViva)
    pantalla.blit(imagen, (x, y))

def dibujarCola(x, y, casilla, serpienteViva):
    penultimate_segment = serpiente[-2]
    imagen = getImagenCola(penultimate_segment, casilla, serpienteViva)
    pantalla.blit(imagen, (x, y))

def getImagenCola(penultimate_segment, casilla, serpienteViva):
    if serpienteViva:
        if casilla[0] < penultimate_segment[0]:
            return ColaAbajo
        elif casilla[0] > penultimate_segment[0]:
            return ColaArriba
        elif casilla[1] < penultimate_segment[1]:
            return ColaDerecha
        elif casilla[1] > penultimate_segment[1]:
            return ColaIzquierda
    else:
        if casilla[0] < penultimate_segment[0]:
            return ColaAbajoMuerta
        elif casilla[0] > penultimate_segment[0]:
            return ColaArribaMuerta
        elif casilla[1] < penultimate_segment[1]:
            return ColaDerechaMuerta
        elif casilla[1] > penultimate_segment[1]:
            return ColaIzquierdaMuerta

def mover(): # Mueve la serpiente
    global serpiente
    casillaDestino = sumarTuplas(serpiente[0], direccionActual)
    contenidoDestino = revisarCasilla(casillaDestino)
    if not serpienteViva:
        return
    if contenidoDestino == 0:
        movimientoNormal(casillaDestino)
    elif contenidoDestino == 1:
        automordida()
        return
    elif contenidoDestino == 2:
        comer(casillaDestino)
    elif contenidoDestino in (3, 4, 5):
        automordida()

def automordida(): # Movimiento de serpiente a una casilla con serpiente
    global serpienteViva, direccionActual
    serpienteViva = False
    return
    
def movimientoNormal(casillaDestino): # Movimiento de serpiente a una casilla vacia
    global serpiente
    actualizarLaberinto(serpiente[-1], 0)
    serpiente.pop()
    serpiente.insert(0, casillaDestino)
    actualizarLaberinto(serpiente[0], 1)

def comer(casillaDestino): # Movimiento de serpiente a una casilla con comida}
    global comida, puntuaje
    #puntuaje += 1
    #mostrarPuntuaje()
    serpiente.insert(0, casillaDestino)
    actualizarLaberinto(serpiente[0], 1)
    comida = generarComida()
    if not silenciado:
        bip.play()

def mostrarPuntuaje():
    os.system('cls')
    print('SCORE:', puntuaje)

def reiniciar(s=0):  # Reinicia todas las variables globales
    global laberinto, serpiente, comida, direccionActual, serpienteViva
    pygame.time.wait(s)
    laberinto = crearMatriz(t)
    laberinto = bordearMatriz(laberinto)
    direccionActual = abajo
    serpienteViva = True
    serpiente = [(3, 1), (2, 1), (1, 1)]
    actualizarLaberinto(serpiente[0], 1)   # 1- es el codigo de Serpiente
    actualizarLaberinto(serpiente[1], 1)
    actualizarLaberinto(serpiente[2], 1)
    comida = generarComida()

##Variables Globales##

pygame.init()
pygame.mixer.init()

    ##Pantalla##
anchoPantalla, altoPantalla = 800, 800
pantalla = pygame.display.set_mode((anchoPantalla, altoPantalla))
pygame.display.set_caption("Snake")

    ##Laberinto##
tamañoLaberinto = t = 16
laberinto = crearMatriz(t)
laberinto = bordearMatriz(laberinto)
# 0 -> Vacio    ;   1 -> Serpiente  ;   2 -> Comida     ;   3 -> Borde Horizontal   ; 4 -> Borde Vertical   ;   5 -> Borde Esquina


    ##Direcciones##
derecha = (0, 1)
izquierda = (0, -1)
arriba = (-1, 0)
abajo = (1, 0)
quieto = (0, 0)
direccionActual = abajo

    ##Colores##
Negro = (0, 0, 0)
Verde = (0, 255, 0)
Rojo = (255, 0, 0)
Azul = (0, 0, 255)
Gris = (220, 220, 220)
Blanco = (255, 255, 255)
Naranja = (218, 72, 15)
celeste = (91, 123, 249)

    ##Sonidos##
bip = pygame.mixer.Sound(r".\Sonidos\bip.mp3")
bop = pygame.mixer.Sound(r".\Sonidos\bop.mp3")
silenciado = False

    ##Serpiente##
serpienteViva = True
serpiente = [(3, 1), (2, 1), (1, 1)]
actualizarLaberinto(serpiente[0], 1)   # 1- es el codigo de Serpiente
actualizarLaberinto(serpiente[1], 1)
actualizarLaberinto(serpiente[2], 1)

    ##Comida##
comida = generarComida()

    ##Clock##
clock = pygame.time.Clock()
velocidad = 75

    ##Puntuaje##
puntuaje = 0

    ##Tamaño Celdas y Tamaño de Sprites##
dimCelda = (altoPantalla//(t))
tamaño = (dimCelda, dimCelda)

    ##Sprites##
# Cabeza
CabezaArriba = pygame.transform.scale(pygame.image.load(r".\Sprites\CabezaArriba.png").convert_alpha(), tamaño)
CabezaAbajo = pygame.transform.scale(pygame.image.load(r".\Sprites\CabezaAbajo.png").convert_alpha(), tamaño)
CabezaDerecha = pygame.transform.scale(pygame.image.load(r".\Sprites\CabezaDerecha.png").convert_alpha(), tamaño)
CabezaIzquierda = pygame.transform.scale(pygame.image.load(r".\Sprites\CabezaIzquierda.png").convert_alpha(), tamaño)
CabezaArribaMuerta = pygame.transform.scale(pygame.image.load(r".\Sprites\CabezaArribaMuerta.png").convert_alpha(), tamaño)
CabezaAbajoMuerta = pygame.transform.scale(pygame.image.load(r".\Sprites\CabezaAbajoMuerta.png").convert_alpha(), tamaño)
CabezaDerechaMuerta = pygame.transform.scale(pygame.image.load(r".\Sprites\CabezaDerechaMuerta.png").convert_alpha(), tamaño)
CabezaIzquierdaMuerta = pygame.transform.scale(pygame.image.load(r".\Sprites\CabezaIzquierdaMuerta.png").convert_alpha(), tamaño)

# Cuerpo
CuerpoHorizontal = pygame.transform.scale(pygame.image.load(r".\Sprites\CuerpoHorizontal.png"), tamaño)
CuerpoVertical = pygame.transform.scale(pygame.image.load(r".\Sprites\CuerpoVertical.png"), tamaño)
CuerpoHorizontalMuerta = pygame.transform.scale(pygame.image.load(r".\Sprites\CuerpoHorizontalMuerta.png"), tamaño)
CuerpoVerticalMuerta = pygame.transform.scale(pygame.image.load(r".\Sprites\CuerpoVerticalMuerta.png"), tamaño)

# Cola
ColaDerecha = pygame.transform.scale(pygame.image.load(r".\Sprites\ColaDerecha.png"), tamaño)
ColaIzquierda = pygame.transform.scale(pygame.image.load(r".\Sprites\ColaIzquierda.png"), tamaño)
ColaArriba = pygame.transform.scale(pygame.image.load(r".\Sprites\ColaArriba.png"), tamaño)
ColaAbajo = pygame.transform.scale(pygame.image.load(r".\Sprites\ColaAbajo.png"), tamaño)
ColaDerechaMuerta = pygame.transform.scale(pygame.image.load(r".\Sprites\ColaDerechaMuerta.png"), tamaño)
ColaIzquierdaMuerta = pygame.transform.scale(pygame.image.load(r".\Sprites\ColaIzquierdaMuerta.png"), tamaño)
ColaArribaMuerta = pygame.transform.scale(pygame.image.load(r".\Sprites\ColaArribaMuerta.png"), tamaño)
ColaAbajoMuerta = pygame.transform.scale(pygame.image.load(r".\Sprites\ColaAbajoMuerta.png"), tamaño)

# Manzana
Manzana = pygame.transform.scale(pygame.image.load(r".\Sprites\Manzana.png"), tamaño)

# Giros
ul = pygame.transform.scale(pygame.image.load(r".\Sprites\UL.png"), tamaño)
ur = pygame.transform.scale(pygame.image.load(r".\Sprites\UR.png"), tamaño)
dl = pygame.transform.scale(pygame.image.load(r".\Sprites\DL.png"), tamaño)
dr = pygame.transform.scale(pygame.image.load(r".\Sprites\DR.png"), tamaño)
ulMuerta = pygame.transform.scale(pygame.image.load(r".\Sprites\ULMuerta.png"), tamaño)
urMuerta = pygame.transform.scale(pygame.image.load(r".\Sprites\URMuerta.png"), tamaño)
dlMuerta = pygame.transform.scale(pygame.image.load(r".\Sprites\DLMuerta.png"), tamaño)
drMuerta = pygame.transform.scale(pygame.image.load(r".\Sprites\DRMuerta.png"), tamaño)

# Bordes
BordeHorizontal = pygame.transform.scale(pygame.image.load(r".\Sprites\BordeHorizontal.png"), tamaño)
BordeVertical = pygame.transform.scale(pygame.image.load(r".\Sprites\BordeVertical.png"), tamaño)
BordeEsquina = pygame.transform.scale(pygame.image.load(r".\Sprites\BordeEsquina.png"), tamaño)

    ##Eventos automaticos##
movimiento = pygame.USEREVENT + 1
pygame.time.set_timer(movimiento, velocidad)
reinicio = pygame.USEREVENT + 2
flagReinicio = False


##Bucle principal

ejecutando = True
while ejecutando:

    #Manejar Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: #Salir
            ejecutando = False
        if evento.type == movimiento:
            mover()
            dibujarLaberinto(serpienteViva)
        if evento.type == reinicio:
            reiniciar()
            pygame.time.set_timer(reinicio, 0)
            flagReinicio = False
    
    #Manejar Teclas
    keys = pygame.key.get_pressed()
    if serpienteViva:
        tecleado(keys)
    else:
        if not flagReinicio:
            pygame.time.set_timer(reinicio, 1000)
            if not silenciado:
                bop.play()
            flagReinicio = True
    
    #Dibujar Frame
    pygame.display.flip()
    clock.tick(60)
    mostrarPuntuaje
pygame.quit()