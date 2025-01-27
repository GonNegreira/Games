import pygame
import math
import random

# Clases
class Asteroide():
    def __init__(self, orden, posicion, velocidad):
        self.orden = orden
        self.posicion = posicion
        self.velocidad = escalarTupla(velocidad, 1/(3*self.orden))
        self.dimension = 20
        self.actualizarHitbox()
    
    def dibujar(self):
        pygame.draw.circle(pantalla, blanco, self.posicion, self.orden*self.dimension//2, 1)

    def mantenerEnPantalla(self):
        (x, y) = self.posicion
        if x > anchoPantalla:
            x = 0
        elif x < 0:
            x = anchoPantalla - 1
        if y > altoPantalla:
            y = 0
        elif y < 0:
            y = altoPantalla - 1
        self.posicion = (x, y)

    def mover(self):
        self.posicion = sumarTuplas(self.posicion, self.velocidad)
        self.mantenerEnPantalla()
        self.actualizarHitbox()
        self.chequearColision()
    
    def actualizarHitbox(self):
        self.hitBox = pygame.Rect(self.posicion[0]-self.orden*self.dimension//2, self.posicion[1]-self.orden*self.dimension//2, self.orden*self.dimension, self.orden*self.dimension)
    
    def chequearColision(self):
        for bala in balas:
            if self.hitBox.collidepoint(bala.posicion[0], bala.posicion[1]):
                indice = balas.index(bala)
                balas.pop(indice)
                self.explotar()

    def explotar(self):
        global puntaje
        if self.orden != 1:
            asteroides.append(Asteroide(self.orden-1, self.posicion, sumarTuplas(self.velocidad, tuplaRandom(10, 10, 0.5))))
            asteroides.append(Asteroide(self.orden-1, self.posicion, sumarTuplas(self.velocidad, tuplaRandom(10, 10, 0.5))))
        asteroides.pop(asteroides.index(self))
        puntaje += 1

class Nave():
    def __init__(self):
        self.posicion = (anchoPantalla / 2, altoPantalla / 2)
        self.x, self.y = anchoPantalla / 2, altoPantalla / 2
        self.ancho = 20  
        self.alto = 30
        self.A = (self.x, self.y - self.alto/2)
        self.B = (self.x - self.ancho/2, self.y + self.alto/2)
        self.C = (self.x + self.ancho/2, self.y + self.alto/2)
        self.angulo = math.pi / 2
        self.color = blanco
        self.actualizarHitbox()
    
    def dibujar(self):
        pygame.draw.polygon(pantalla, self.color, [self.A, self.B, self.C], 1)

    def rotar(self, direccion, sensibilidad):
        if direccion == -1: # Rotacion antihoraria
            self.A, self.B, self.C, = rotarPuntos(sensibilidad, self.A, self.B, self.C, self.posicion)
            self.angulo += sensibilidad
        else:
            self.A, self.B, self.C = rotarPuntos(-1*sensibilidad, self.A, self.B, self.C, self.posicion)
            self.angulo -= sensibilidad

    def actualizarHitbox(self):
        self.hitBox = pygame.Rect(self.x - self.ancho/2, self.y - self.alto/2, self.ancho, self.alto)

class Bala():
    def __init__(self, posicion, angulo):
        self.posicion = posicion
        self.velocidad = 2
        vectorDireccion = (1, angulo)
        self.direccion = escalarTupla(restringirTupla(cartesiano(vectorDireccion), self.velocidad), -1)
    
    def mover(self):
        self.posicion = sumarTuplas(self.posicion, self.direccion)
        if self.posicion[0] < 0 or self.posicion[0] > anchoPantalla:
            del self
            balas.pop()
            return
        if self.posicion[1] < 0 or self.posicion[1] > altoPantalla:
            del self
            balas.pop()
            return
    
    def dibujar(self):
        pygame.draw.circle(pantalla, blanco, self.posicion, 3, 1)

# Funciones

def sumarTuplas(A, B): # Dadas dos tuplas A, B, retorna la tupla suma de ambas
    (x, y) = A
    (a, b) = B
    return (x+a, y+b)

def restarTuplas(A, B): # Dadas dos tuplas A, B, retorna la tupla resta de ambas
    (x, y) = A
    (a, b) = B
    return (x-a, y-b)

def escalarTupla(A, k): # Dada una tupla A y un escalar k, retorna la tupla A*k
    (x, y) = A
    return (x*k, y*k)

def medirMagintud(A): # Dada una tupla A, retorna la magnitud de la misma
    (x, y) = A
    return math.sqrt(x**2 + y**2)

def restringirTupla(A, m): # Dada una Tupla A y un escalar k, retorna una tupla de magnitud m con misma direccion que A
    magnitudInicial = medirMagintud(A)
    if magnitudInicial != 0:
        escala = m / magnitudInicial
        return escalarTupla(A, escala)
    return escalarTupla(A, 0)

def distancia(A, B): # Dada dos tuplas A, B retorna la distancia entre ambas
    return medirMagintud(restarTuplas(B, A))

def tuplaRandom(xMax, yMax, m=1):   # Crea una tupla aleatoria con un magnitud m
    x = random.randint(0, xMax)
    y = random.randint(0, yMax)
    return restringirTupla((x, y), m)

def cartesiano(vectorPolar):
    magnitud, angulo = vectorPolar
    return (math.cos(angulo)*magnitud, math.sin(angulo)*magnitud)

def crearAsteriodes(k):
    global anchoPantalla
    asteroides = []
    for i in range(k):
        asteroides.append(Asteroide(4, tuplaRandom(anchoPantalla, altoPantalla, anchoPantalla), tuplaRandom(10, 10, 0.5)))
    return asteroides

def dibujarEspacio():
    pantalla.fill(negro)
    # Dibujar Asteroides
    for asteroide in asteroides:
        asteroide.dibujar()
        asteroide.mover()
    # Dibujar Nave
    nave.dibujar()
    # Dibujar balas
    for bala in balas:
        bala.dibujar()
        bala.mover()
    # Dibujar Vidas
    for i in range(vidas):
        x_offset = 20 + i * 30
        y_offset = 20
        ancho = 20
        alto = 30
        A = (x_offset, y_offset)
        B = (x_offset - ancho/2, y_offset + alto)
        C = (x_offset + ancho/2, y_offset + alto)
        pygame.draw.polygon(pantalla, blanco, [A, B, C], 1)
    # Dibujar score
    pantalla.blit(fuente.render('SCORE: '+ str(puntaje), 1, blanco), (anchoPantalla-185, 20))

def tecleado(teclas):
    if teclas[pygame.K_LEFT] and not teclas[pygame.K_LCTRL]:
        nave.rotar(1, 0.001)
    if teclas[pygame.K_RIGHT] and not teclas[pygame.K_LCTRL]:
        nave.rotar(-1, 0.001)
    if teclas[pygame.K_LEFT] and teclas[pygame.K_LCTRL]:
        nave.rotar(1, 0.003)
    if teclas[pygame.K_RIGHT] and teclas[pygame.K_LCTRL]:
        nave.rotar(-1, 0.003)
    if teclas[pygame.K_LEFT] and teclas[pygame.K_LSHIFT]:
        nave.rotar(1, 0.01)
    if teclas[pygame.K_RIGHT] and teclas[pygame.K_LSHIFT]:
        nave.rotar(-1, 0.01)
    if teclas[pygame.K_SPACE] and not enfriamiento:
        disparar()

def chequearColisionNave():
    global vidas, asteroides
    for asteroide in asteroides:
        if asteroide.hitBox.colliderect(nave.hitBox):
            vidas -= 1
            reiniciarNave()
            break

def reiniciarJuego():
    global cantidadAsteroides, asteroides, nave, puntaje, vidas, balas
    cantidadAsteroides = 1
    asteroides = crearAsteriodes(cantidadAsteroides)
    nave = Nave()
    puntaje = 1
    vidas = 3
    balas = []

def reiniciarNave():
    global asteroides
    asteroides = crearAsteriodes(cantidadAsteroides)

def rotarPunto(punto, centro, theta):
    # Trasladar el punto para que el centro esté en el origen
    x, y = punto
    cx, cy = centro
    x_trasladado = x - cx
    y_trasladado = y - cy

    # Aplicar rotación
    x_rotado = x_trasladado * math.cos(theta) - y_trasladado * math.sin(theta)
    y_rotado = x_trasladado * math.sin(theta) + y_trasladado * math.cos(theta)

    # Volver a trasladar el punto al sistema original
    x_final = x_rotado + cx
    y_final = y_rotado + cy
    return (x_final, y_final)
    
def rotarPuntos(theta, A, B, C, D):
        # Rotar cada punto
    A_rotado = rotarPunto(A, D, theta)
    B_rotado = rotarPunto(B, D, theta)
    C_rotado = rotarPunto(C, D, theta)

    return A_rotado, B_rotado, C_rotado
       

def disparar():
    global balas, enfriamiento
    balas.insert(0  , Bala(nave.A, nave.angulo))
    enfriamiento = True
    pygame.time.set_timer(listoParaDisparar, 200)
    

# Variables Globales

    # Pantalla
anchoPantalla, altoPantalla = 1200, 900
pantalla = pygame.display.set_mode((anchoPantalla, altoPantalla))

    # Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (255, 0, 0)
azul = (0, 0, 255)

    # Asteroides
cantidadAsteroides = 4
asteroides = crearAsteriodes(cantidadAsteroides)

    # Nave
nave = Nave()
puntaje = 1
vidas = 3

    # Balas
balas = []
enfriamiento = False

    # Fuente
pygame.font.init()
fuente = pygame.font.Font(None, 48)

    # Eventos
listoParaDisparar = pygame.USEREVENT + 1

ejecutando = True
# Bucle Principal

ejecutando = True
while vidas > 0 and ejecutando:

    # manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == listoParaDisparar:
            enfriamiento = False
        if evento.type == pygame.K_r:
            reiniciarJuego()

    # manejo de teclas  
    teclas = pygame.key.get_pressed()
    tecleado(teclas)

    if len(asteroides) == 0:
        cantidadAsteroides += 1
        asteroides = crearAsteriodes(cantidadAsteroides)
    chequearColisionNave()

    # Dibujo
    dibujarEspacio()
    pygame.display.flip()

# End Screen 

while ejecutando:
    pantalla.fill(negro)
    
    pantalla.blit(fuente.render('GAME OVER!', 1, blanco), (anchoPantalla/2-100, altoPantalla/2-100))
    pantalla.blit(fuente.render('SCORE: ' + str(puntaje), 1, blanco), (anchoPantalla/2-100, altoPantalla/2))
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    pygame.display.flip()