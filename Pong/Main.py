import pygame
import random

# Funciones
def dibujarFrame():
    pantalla.fill(negro)
    pygame.draw.rect(pantalla, blanco, paletaDer)
    pygame.draw.rect(pantalla, blanco, paletaIzq)
    pygame.draw.circle(pantalla, blanco, pelota, 10)
    pantalla.blit(scoreDerText, lugarScoreDer)
    pantalla.blit(scoreIzqText, lugarScoreIzq)

def tecleado(keys):
    global paletaIzq, paletaDer
    if keys[pygame.K_UP] and paletaDer.top > 0:
        paletaDer = paletaDer.move(0, sensibilidad*-1)
    if keys[pygame.K_DOWN] and paletaDer.bottom < altoPantalla:
        paletaDer = paletaDer.move(0, sensibilidad)
    if keys[pygame.K_w] and paletaIzq.top > 0:
        paletaIzq = paletaIzq.move(0, sensibilidad*-1)
    if keys[pygame.K_s] and paletaIzq.bottom < altoPantalla:
        paletaIzq = paletaIzq.move(0, sensibilidad)

def sumarTuplas(A:tuple, B:tuple):
    a, b = A
    c, d = B
    return (a+c, b+d)

def moverPelota():
    global direccionPelota, pelota, ScoreDer, ScoreIzq
    nuevaPosicion = sumarTuplas(pelota, direccionPelota)
    x, y = nuevaPosicion
    if y <= radio:
        rebotarHaciaAbajo()
    elif y >= altoPantalla - radio:
        rebotarHaciaArriba()
    elif x <= radio:
        ScoreDer += 1
        actualizarScores()
        reiniciar()
    elif x >= anchoPantalla - radio:
        ScoreIzq += 1
        actualizarScores()
        reiniciar()
    elif paletaDer.collidepoint(nuevaPosicion):
        direccionPelota = random.choice([izquierdaAbajo, izquierdaArriba])
    elif paletaIzq.collidepoint(nuevaPosicion):
        direccionPelota = random.choice([derechaAbajo, derechaArriba])
    else:
        pelota = nuevaPosicion

def rebotarHaciaArriba():
    global direccionPelota, pelota
    if direccionPelota == izquierdaAbajo:
        direccionPelota = izquierdaArriba
    else:
        direccionPelota = derechaArriba
    pelota = sumarTuplas(pelota, direccionPelota)

def rebotarHaciaAbajo():
    global direccionPelota, pelota
    if direccionPelota == izquierdaArriba:
        direccionPelota = izquierdaAbajo
    else:
        direccionPelota = derechaAbajo
    pelota = sumarTuplas(pelota, direccionPelota)

def reiniciar():
    global direccionPelota, pelota
    pelota = (anchoPantalla//2, altoPantalla//2)
    direccionPelota = random.choice([derechaAbajo, derechaArriba, izquierdaAbajo, izquierdaArriba])

def actualizarScores():
    global scoreDerText, scoreIzqText
    scoreDerText = fuente.render(str(ScoreDer), True, blanco)
    scoreIzqText = fuente.render(str(ScoreIzq), True, blanco)

# Pantalla
pygame.init()
anchoPantalla, altoPantalla = 1200, 600
espacio = 55
pantalla = pygame.display.set_mode((anchoPantalla, altoPantalla))
pygame.display.set_caption('P o n g')


# Paletas
paletaDer = pygame.Rect(anchoPantalla - espacio, altoPantalla//2, 15, 120)
paletaIzq = pygame.Rect(espacio, altoPantalla//2, 15, 120)
sensibilidad = 1


# Pelota
pelota = (anchoPantalla//2, altoPantalla//2)
radio = 15

# Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (255, 0, 0)

# Scores
ScoreDer = 0
ScoreIzq = 0
fuente = pygame.font.Font(None, 48)
lugarScoreIzq = (espacio*2, espacio*2)
lugarScoreDer = (anchoPantalla - (espacio*2), espacio*2)
actualizarScores()

# Direcciones
derechaAbajo = (1, 1)
derechaArriba = (1, -1)
izquierdaAbajo = (-1, 1)
izquierdaArriba = (-1, -1)
direccionPelota = random.choice([derechaAbajo, derechaArriba, izquierdaAbajo, izquierdaArriba])

# Timers
movimiento = pygame.USEREVENT + 1
pygame.time.set_timer(movimiento, 1)

# Main loop
ejecutando = True
while ejecutando:

    #Manejar Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: #Salir
            ejecutando = False
        if evento.type == movimiento:
            moverPelota()
    
    #Manejar Teclas
    keys = pygame.key.get_pressed()
    tecleado(keys)

    #Dibujar Frame
    dibujarFrame()
    pygame.display.flip()

pygame.quit()