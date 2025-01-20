import tkinter as tk
from tkinter import font


#Definicion de las variables globales
seleccion, movimiento = None, None 
tablero = [ 
    ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],  #0
    ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],  #1
    [" ", " ", " ", " ", " ", " ", " ", " "],   #2
    [" ", " ", " ", " ", " ", " ", " ", " "],   #3
    [" ", " ", " ", " ", " ", " ", " ", " "],   #4
    [" ", " ", " ", " ", " ", " ", " ", " "],   #5
    ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],   #6  
    ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]]   #7
    #  0    1     2     3     4     5     6    7
root = tk.Tk('Ajedrez')
fuente = font.Font(family='Helvetica', size=30)
root.configure(background='black')
movimientosPosibles = []
piezasBlancas, piezasNegras = ('♙','♖','♘','♗','♕','♔'), ('♟','♜','♞','♝','♛','♚')
pieza = None
jugador = 'Blanco'
enemigos = piezasNegras
amigos = piezasBlancas
flagEnPassant = False

def tuplaEnTablero(tupla):
    x, y = detuplar(tupla)
    return -1 < x < 8 and -1 < y < 8

def traducirWidget(seleccion):
    ##Transforma un Widget .yx a una tupla (y,x)
    return (int(seleccion[1]), int(seleccion[2]))

def detuplar(tupla):
    ##Transforma una Tupla (y,x) a los valores y, x
    y = tupla[0]
    x = tupla[1]
    return y, x

def pasarDeTurno():
    global jugador, amigos, enemigos
    if jugador == 'Blanco':
        jugador = 'Negro'
    else:
        jugador = 'Blanco'
    reconocerAmigos()
    reconocerEnemigos()

def resetearSelecciones(event):
    ##Resetea las selecciones a None
    global seleccion, movimiento, pieza, movimientosPosibles
    seleccion, movimiento, pieza, movimientosPosibles = None, None, None, []
    mostrarTablero()

def mover(event):
    ##Movimiento Simple de testeo
    global seleccion, movimiento
    if movimiento in movimientosPosibles:
        tablero[movimiento[0]][movimiento[1]] = pieza
        tablero[seleccion[0]][seleccion[1]] = ' '
        pasarDeTurno()
    mostrarTablero()
    resetearSelecciones(event)

def seleccionarCasilla(event):
    ##Setea la variable Movimiento
    global movimiento
    movimiento = str(event.widget)
    movimiento = traducirWidget(movimiento)
    mostrarTablero()

def seleccionarPieza(event):
    ##Setea la variable seleccion
    resetearSelecciones(event)
    global seleccion, tablero, pieza, movimientosPosibles
    seleccion = str(event.widget)
    seleccion = traducirWidget(seleccion)
    y, x = detuplar(seleccion)
    pieza = tablero[y][x]
    if pieza in amigos:
        getMovimientosPosibles()
    mostrarTablero()

def getMovimientosPosibles():
    ##Sete la variable MovimientosPosibles dependiendo la pieza
    global pieza, seleccion
    y, x = detuplar(seleccion)
    if pieza in ('♘', '♞'):
        movimientosCaballos(y, x)
    elif pieza == '♙':
        movimientosPeonBlanco(y, x)
    elif pieza == '♟':
        movimientosPeonNegro(y, x)
    elif pieza in ('♜', '♖'):
        movimientosTorre(y, x)
    elif pieza in ('♝', '♗'):
        movimientosDiagonales(y, x)
    elif pieza in ('♕', '♛'):
        movimientosDiagonales(y,x)
        movimientosHorizontales(y,x)
        movimientosVerticales(y,x)
    elif pieza in ('♔', '♚'):
        movimientosRey(y,x)
    else:
        return

def reconocerEnemigos():
    global enemigos
    if jugador == 'Blanco':
        enemigos = piezasNegras
        return
    enemigos = piezasBlancas

def reconocerAmigos():
    global amigos
    if jugador == 'Blanco':
        amigos = piezasBlancas
        return
    amigos = piezasNegras

def movimientosCaballos(y, x):
    global movimientosPosibles, tablero, jugador, piezasBlancas, piezasNegras
    listaPosible = [(y-2, x+1), (y-2, x-1), 
             (y-1, x+2), (y-1, x-2),
             (y+2, x+1), (y+2, x-1),
             (y+1, x+2), (y+1, x-2)]
    for tupla in listaPosible:
        y, x = tupla[0], tupla[1]
        if x > 7 or y > 7:
            continue
        else:
            pieza = tablero[y][x]
            if pieza == ' ':
                movimientosPosibles.append(tupla)
            if jugador == 'Blanco' and pieza in piezasNegras:
                movimientosPosibles.append(tupla)
            if jugador == 'Negro' and pieza in piezasBlancas:
                movimientosPosibles.append(tupla)

def movimientosPeonBlanco(y, x):
    global movimientosPosibles, tablero, piezasNegras
    if y > 0 and tablero[y-1][x] == ' ':
        movimientosPosibles.append((y-1,x))
        if tablero[y-2][x] == ' ' and y == 6:
            movimientosPosibles.append((y-2,x))
    if x > 0 and y > 0 and tablero[y-1][x-1] in piezasNegras:
        movimientosPosibles.append((y-1,x-1))
    if y > 0 and x < 7 and tablero[y-1][x+1] in piezasNegras:
        movimientosPosibles.append((y-1,x+1))

def movimientosPeonNegro(y, x):
    global movimientosPosibles, tablero, piezasBlancas
    if tablero[y+1][x] == ' ':
        movimientosPosibles.append((y+1, x))
        if tablero[y+2][x] == ' ' and y == 1:
            movimientosPosibles.append((y+2, x))
    if y < 7 and x < 7 and tablero[y+1][x+1] in piezasBlancas:
        movimientosPosibles.append((y+1, x+1))
    if y < 7 and x > 0 and tablero[y+1][x-1] in piezasBlancas:
        movimientosPosibles.append((y+1, x-1))

def movimientosTorre(y, x):
    global movimientosPosibles
    movimientosVerticales(y,x)
    movimientosHorizontales(y, x)
    
def movimientosVerticales(y, x):
    global movimientosPosibles
    for i in range(y+1, 8):
        if tablero[i][x] == ' ':
            movimientosPosibles.append((i, x))
        elif tablero[i][x] in enemigos:
            movimientosPosibles.append((i, x))
            break
        else:
            break
    for i in range(y-1, -1, -1):
        if tablero[i][x] == ' ':
            movimientosPosibles.append((i,x))
        elif tablero[i][x] in enemigos:
            movimientosPosibles.append((i,x))
            break
        elif tablero[i][x] == pieza:
            continue
        else:
            break

def movimientosHorizontales(y, x):
    global movimientosPosibles
    for i in range(x+1, 8):
        if tablero[y][i] == ' ':
            movimientosPosibles.append((y, i))
        elif tablero[y][i] in enemigos:
            movimientosPosibles.append((y, i))
            break
        else:
            break
    for i in range(x-1, -1, -1):
        if tablero[y][i] == ' ':
            movimientosPosibles.append((y,i))
        elif tablero[y][i] in enemigos:
            movimientosPosibles.append((y,i))
            break
        elif tablero[y][i] == pieza:
            continue
        else:
            break

def movimientosDiagonales(y, x):
    global movimientosPosibles, enemigos
    j, i = y + 1 , x + 1
    while i < 8 and j < 8:
        if tablero[j][i] == ' ':
            movimientosPosibles.append((j, i))
        elif tablero[j][i] in enemigos:
            movimientosPosibles.append((j, i))
            break
        else:
            break
        j += 1
        i += 1
    j, i = y + 1 , x - 1
    while i > -1 and j < 8:
        if tablero[j][i] == ' ':
            movimientosPosibles.append((j, i))
        elif tablero[j][i] in enemigos:
            movimientosPosibles.append((j, i))
            break
        else:
            break
        j += 1
        i -= 1
    j, i = y -1, x - 1
    while i > -1 and j > -1:
        if tablero[j][i] == ' ':
            movimientosPosibles.append((j, i))
        elif tablero[j][i] in enemigos:
            movimientosPosibles.append((j, i))
            break
        else:
            break
        j -= 1
        i -= 1
    j, i = y-1, x+1
    while i < 8 and j > -1:
        if tablero[j][i] == ' ':
            movimientosPosibles.append((j, i))
        elif tablero[j][i] in enemigos:
            movimientosPosibles.append((j, i))
            break
        else:
            break
        j -= 1
        i += 1

def movimientosRey(y,x):
    global movimientosPosibles, enemigos
    listaPosibles = [
                    (y+1, x-1), (y+1, x), (y+1, x+1),
                    (y, x-1), (y,x) ,(y, x+1),
                    (y-1, x-1), (y-1, x), (y-1, x+1)
                    ]
    for tupla in listaPosibles:
        b, a= detuplar(tupla)
        if tuplaEnTablero(tupla):
            if tablero[b][a] == ' ':
                movimientosPosibles.append((b, a))
            elif tablero[b][a] in enemigos:
                movimientosPosibles.append((b, a))
            else:
                continue
        else:
            continue

def pronostico(titulo):
    print(f'---{titulo}---')
    print('Seleccion: ', seleccion)
    print('Movimiento: ', movimiento)
    print('Pieza: ', pieza)
    print('Jugador: ', jugador)
    print('Enemigos: ', enemigos)
    print('Amigos: ', amigos)

def chequearGanador():
    ganadores = ['Blanco', 'Negro', None]
    for i in range(8):
        for j in range(8):
            piezaVisitada = tablero[i][j]
            if piezaVisitada == '♔':
                ganadores.pop(1)
            if piezaVisitada == '♚':
                ganadores.pop(0)
    return ganadores[0]

def mostrarTablero():
    ##Muestra el tablero
    global seleccion, movimiento, root, tablero, movimientosPosibles
    x, y, a, b = -1, -1, -1, -1
    if seleccion is not None:
        y, x = detuplar(seleccion)
    if movimiento is not None:
        a, b = detuplar(movimiento)
    for fila in range(8):
        for columna in range(8):
            texto = tablero[fila][columna]
            colorPieza = 'black'
            casillaVisitada = (fila, columna)
            if casillaVisitada == (y, x):
                colorPieza = 'grey'
            if casillaVisitada in movimientosPosibles and texto == ' ':
                texto = '•'
            elif casillaVisitada in movimientosPosibles:
                texto += '×'
            if (fila + columna) % 2 == 0:
                colorCasilla = 'white'
            else:
                colorCasilla = 'lightgrey'
            if casillaVisitada == (a, b):
                colorCasilla = 'brown'
            etiqueta = tk.Label(root, name=str(fila)+str(columna), text=texto, width=4, height=2, bg=colorCasilla, fg=colorPieza, font=fuente)
            etiqueta.grid(row=fila, column=columna, padx=3, pady=3)
    ganador = chequearGanador()
    if ganador is None:
        return
    elif ganador == 'Blanco':
        fin('Blanco')
    else:
        fin('Negro')

def fin(color):
    return

def jugar():
    mostrarTablero()
    root.bind("<Button-1>", seleccionarPieza)
    root.bind("<Button-3>", seleccionarCasilla)
    root.bind("<space>", mover)
    root.bind("<Escape>", resetearSelecciones)
    root.mainloop()

jugar()
