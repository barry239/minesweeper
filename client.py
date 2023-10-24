import socket
import json
import threading
import helpers
from minesweeper import Minesweeper


BUF_SIZE = 1024


def handleRecv():
    global s, playing, mspr, num

    while playing:
        ## Get message
        msg = json.loads(s.recv(BUF_SIZE).decode())

        ## Check if the cell is already uncovered
        if msg['type'] == 2 and msg['cont'] == 'Uncovered':
            print('\n[!!] La casilla ya fue descubierta\n')
        
        ## Uncover cell
        if msg['type'] == 3:
            coord = msg['cont']
            col = ord(coord[0].lower()) - 96
            row = int(coord[1:])
            mspr.board[row - 1][col - 1] = msg['val']

            ## Display board
            helpers.clear()
            mspr.displayBoard(num)
            print('Ingrese la coordenada:')

        ## Check if a mine has been hit
        if msg['type'] == 4 and msg['cont'] == 'Game over':
            helpers.clear()

            ## Receive mines location
            s.send(json.dumps({'type': -1, 'cont': 'unused'}).encode()) # Unused send
            msg = json.loads(s.recv(BUF_SIZE).decode())
            mspr.mines = msg['cont']

            ## Receive elapsed time
            s.send(json.dumps({'type': -1, 'cont': 'unused'}).encode()) # Unused send
            msg = json.loads(s.recv(BUF_SIZE).decode())
            elapsed = float(msg['cont'])

            ## Finish game
            mspr.finishGame('Juego terminado, seleccionaste una mina.', num, elapsed)
            playing = False
        
        ## Check if the game was won
        if msg['type'] == 5 and msg['cont'] == 'Game won':
            helpers.clear()

            ## Receive mines location
            s.send(json.dumps({'type': -1, 'cont': 'unused'}).encode()) # Unused send
            msg = json.loads(s.recv(BUF_SIZE).decode())
            mspr.mines = msg['cont']

            ## Receive elapsed time
            s.send(json.dumps({'type': -1, 'cont': 'unused'}).encode()) # Unused send
            msg = json.loads(s.recv(BUF_SIZE).decode())
            elapsed = float(msg['cont'])

            ## Finish game
            mspr.finishGame('¡Felicidades!, has ganado.', num, elapsed)
            playing = False


def handleSend():
    global s, playing

    while playing:
        ## Get coordinate
        coord = helpers.getCoordinate()
        s.send(json.dumps({'type': 1, 'cont': coord}).encode())


## Enter host
# host = helpers.getHost()
host = '127.0.0.1'

## Enter port
# port = helpers.getPort()
port = 3000

## Create socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    ## Show main menu
    helpers.showMainMenu()

    ## Show waiting menu
    helpers.showWaitingMenu()

    ## Receive player number
    msg = json.loads(s.recv(BUF_SIZE).decode())
    num = msg['cont']

    ## Create minesweeper
    mspr = Minesweeper('0')

    ## Display board
    helpers.clear()
    mspr.displayBoard(num)
    print('Ingrese la coordenada:')

    ## Start game
    playing = True
    rthread = threading.Thread(target=handleRecv)
    sthread = threading.Thread(target=handleSend)
    rthread.start()
    sthread.start()
    rthread.join()
    sthread.join()