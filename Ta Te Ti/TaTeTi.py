##IMPORTS
import tkinter as tk
import time

##VARIABLES GLOBAL
seleccion, movimiento = None, None
tablero = [[' ', ' ', ' '],
           [' ', ' ', ' '],
           [' ', ' ', ' ']]
jugador = '●'
jugadores = '●x'
victorias1, victorias2 = 0, 0
turno = 1
pantalla = tk.Tk('Pantalla')
pantalla.config(bg='black', border=3)
pantalla.iconname('TaTeTi')
ganador = None

def mostrarTablero():
    etiqueta = tk.Label(pantalla, name='jugador', text='Turno de: '+ jugador, font=('Consolas', 24), bg='black', fg='white')
    etiqueta.grid(row=(0), columnspan=len(tablero[0]))
    for fila in range(len(tablero)):
        for columna in range(len(tablero)):
            casillaVisitada = (columna, fila)
            colorCasilla, colorTexto = decidirColores(casillaVisitada)
            etiqueta = tk.Label(pantalla, name=str((columna, fila)), text=tablero[fila][columna], bg=colorCasilla, fg=colorTexto, width=10, height=5, font=('Consolas', 27))
            etiqueta.grid(padx=2, pady=2, column=columna, row=fila+1)
    victorias = tk.Label(pantalla, bg='grey', font=('Consolas', 24), text=' PUNTAJE '+'\n'+jugadores[0]+':'+str(victorias1) +'\n'+jugadores[1]+':'+ str(victorias2), fg='white')
    victorias.grid(column=3, row=0, rowspan=2, padx=4, pady=4)

def decidirColores(casillaVisitada):
    (x, y) = casillaVisitada
    colorTexto='black'
    colorCasilla = 'grey'
    if (x+y)% 2 == 0:
        colorCasilla = 'white'
    if casillaVisitada == seleccion and turno > 6:
        colorTexto = 'orange'
    return colorCasilla, colorTexto

def TraducirWidget(widget):
    widget = str(widget)
    widget = widget.removeprefix('.')
    tupla = (int(widget[1]), int(widget[-2]))
    return tupla

def clickIzquierdo(Evento):
    global seleccion
    seleccion = TraducirWidget(Evento.widget)
    if turno <= 6:
        colocarPieza()
    mostrarTablero()
    return

def colocarPieza():
    global tablero
    (x, y) = seleccion
    if tablero[y][x] == ' ':
        tablero[y][x] = jugador
        pasarTurno()
    return

def clickDerecho(Evento):
    global movimiento
    movimiento = TraducirWidget(Evento.widget)
    if turno > 6 and seleccion is not None:
        moverPieza()
    mostrarTablero()
    return

def moverPieza():
    global tablero
    (x, y) = movimiento
    (a, b) = seleccion
    if tablero[b][a] == jugador and tablero[y][x] == ' ' and esMovimientoValido():
        tablero[y][x] = jugador
        tablero[b][a] = ' '
        mostrarTablero()
        pasarTurno()
    return

def pasarTurno():
    global seleccion, movimiento, jugador, turno
    chequearTateti()
    turno += 1
    movimiento, seleccion = None, None
    if jugador == jugadores[0]:
        jugador = jugadores[1]
    else:
        jugador = jugadores[0]
    if ganador is not None:
        resetear()
    return

def esMovimientoValido():
    matrizValidez = [   [2, 1, 2],
                        [1, 0, 1],
                        [2, 1, 2]]
    (x, y) = movimiento
    (a, b) = seleccion
    return (matrizValidez[y][x] != matrizValidez[b][a] ) and (abs(y-b) <= 1 and abs(x-a) <= 1)

def chequearTateti():
    global ganador, victorias1, victorias2
    ganador = chequearFilas()
    if ganador is None:
        ganador = chequearColumnas()
    if ganador is None:
        ganador = chequearDiagonales()
    if ganador == jugadores[0]:
        victorias1 += 1
    if ganador == jugadores[1]:
        victorias2 += 1

def chequearFilas():
    for ganador in jugadores:
        for fila in range(len(tablero)):
            if tablero[fila][0] == tablero[fila][1] == tablero[fila][2] == ganador:
                return ganador
    return None

def chequearColumnas():
    for ganador in jugadores:
        for columna in range(len(tablero[0])):
            if tablero[0][columna] == tablero[1][columna] == tablero[2][columna] == ganador:
                return ganador
    return None

def chequearDiagonales():
    for ganador in jugadores:
        if tablero[0][0] == tablero[1][1] == tablero[2][2] == ganador:
            return ganador
        if tablero[0][2] == tablero[1][1] == tablero[2][0] == ganador:
            return ganador
    return None

def resetear():
    global seleccion, movimiento, tablero, jugador, turno, ganador
    mostrarTablero()
    seleccion, movimiento = None, None
    tablero = [[' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']]
    turno = 1
    ganador = None

def main():
    mostrarTablero()
    pantalla.bind("<Button-1>", clickIzquierdo)
    pantalla.bind("<Button-3>", clickDerecho)
    pantalla.mainloop()

if __name__ == '__main__':
    main()