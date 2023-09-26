import socket
import os
import re
import json
from minesweeper import Minesweeper


BUF_SIZE = 1024


clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def showMainMenu() -> None:
    clear()
    print('Bienvenido a Buscaminas\n')
    print('Instrucciones:')
    print('1) Elija una dificultad')
    print('2) Ingrese la coordenada de la casilla a descubrir (e.g. a1)')
    print('3) El juego finaliza al pisar una mina o descubrir todas las casillas vacías\n')
    input('Presione <Enter> para continuar...')

def showDifficultyMenu() -> str:
    clear()
    print('1) Principiante - 9 x 9 casillas, 10 minas')
    print('2) Avanzado - 16 x 16 casillas, 40 minas\n')
    difficulty = input('Elija la dificultad: ')
    
    return difficulty


## Enter host
while True:
    host = input('Ingrese la dirección IP: ')
    if re.match(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$', host): break
    print('\n[!!] Ingrese una dirección válida\n')

## Enter port
while True:
    port = input('Ingrese el número de puerto: ')
    if re.match(r'^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$', port): break
    print('\n[!!] Ingrese un puerto válido\n')
port = int(port)

## Create socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    ## Show main menu
    showMainMenu()

    ## Select difficulty level
    while True:
        difficulty = showDifficultyMenu()

        if difficulty not in Minesweeper.difficulties:
            print('\n[!!] Elija una opción correcta\n')
            input('Presione <Enter> para continuar...')
        else:
            s.send(difficulty.encode())
            break

    ## Check server response
    msg = s.recv(BUF_SIZE).decode()
    if msg == 'Game started':
        ## Create minesweeper
        mspr = Minesweeper(difficulty)

        ## Start game
        while True:
            ## Display board
            clear()
            mspr.displayBoard()

            ## Get coordinate
            coord = input('Ingrese la coordenada: ')
            if not re.match(r'[a-z]\d{1,2}', coord, re.IGNORECASE):
                print('\n[!!] Elija una coordenada válida\n')
                input('Presione <Enter> para continuar...')
                continue
            s.send(coord.encode())
            col = ord(coord[0].lower()) - 96
            row = int(coord[1:])

            ## Check if the cell is already uncovered
            msg = s.recv(BUF_SIZE).decode()
            if msg == 'Uncovered': continue
            s.send(b'unused') # Unused send

            ## Receive server response
            msg = s.recv(BUF_SIZE).decode()
            s.send(b'unused') # Unused send

            ## Check if a mine has been hit
            if msg == 'Game over':
                clear()

                ## Receive mines location
                mspr.mines = json.loads(s.recv(BUF_SIZE).decode())
                s.send(b'unused') # Unused send

                ## Receive elapsed time
                elapsed = float(s.recv(BUF_SIZE).decode())

                mspr.finishGame('Juego terminado, seleccionaste una mina.', elapsed)
                break

            ## Uncover cell
            mspr.board[row - 1][col - 1] = msg

            ## Receive server response
            msg = s.recv(BUF_SIZE).decode()

            ## Check if the game was won
            if msg == 'Game won':
                s.send(b'unused') # Unused send

                clear()

                ## Receive mines location
                mspr.mines = json.loads(s.recv(BUF_SIZE).decode())
                s.send(b'unused') # Unused send

                ## Receive elapsed time
                elapsed = float(s.recv(BUF_SIZE).decode())

                mspr.finishGame('¡Felicidades!, has ganado.', elapsed)
                break
