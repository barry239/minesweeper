import socket
import os
import re
from minesweeper import Minesweeper


HOST = '127.0.0.1'
PORT = 3000
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


## Create socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    ## Show main menu
    showMainMenu()

    ## Select difficulty level
    while True:
        difficulty = showDifficultyMenu()

        if difficulty not in Minesweeper.difficulties:
            print('\n[!!] Elija una opción correcta\n')
            input('Presione <Enter> para continuar...')
        else:
            s.sendall(difficulty.encode())
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
            s.sendall(coord.encode())

            ## Check server response
            msg = s.recv(BUF_SIZE).decode()
            if msg == 'Uncovered': continue
