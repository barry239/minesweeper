import socket
import json
import threading
import helpers
from minesweeper import Minesweeper


BUF_SIZE = 1024


def handleRecv(s: socket.socket) -> None:
    global mspr, playing, num

    messages = []
    msg = None

    while playing:
        ## Get messages
        if not messages: messages = s.recv(BUF_SIZE).decode().split('#')[:-1]
        msg = json.loads(messages.pop(0))

        ## Check if the cell is already uncovered
        if msg['type'] == 2 and msg['cont'] == 'Descubierta':
            print('\n[!!] La casilla ya fue descubierta\n')
        
        ## Uncover cell
        if msg['type'] == 3:
            col = ord(msg['cont'][0].lower()) - 96
            row = int(msg['cont'][1:])
            mspr.board[row - 1][col - 1] = msg['val']

        ## Receive turn and display board
        if msg['type'] == 4:
            helpers.clear()
            mspr.displayBoard(num, msg['cont'])
            print('Ingrese la coordenada:')
        
        ## Finish game
        if msg['type'] == 5:
            helpers.clear()

            ## Get mines location
            mspr.mines = msg['mines']

            ## Get elapsed time
            elapsed = float(msg['elapsed'])

            mspr.finishGame(msg['cont'], num, elapsed)
            playing = False

def handleSend(s: socket.socket) -> None:
    global playing

    while playing:
        ## Get coordinate
        coord = helpers.getCoordinate()
        s.send(json.dumps({ 'type': 1, 'cont': coord }).encode())


## Enter host
host = helpers.getHost()
# host = '127.0.0.1'

## Enter port
port = helpers.getPort()
# port = 3000

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
    rthread = threading.Thread(target=handleRecv, args=(s,))
    sthread = threading.Thread(target=handleSend, args=(s,))
    rthread.start()
    sthread.start()

    rthread.join()
    sthread.join()