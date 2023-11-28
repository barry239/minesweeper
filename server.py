import socket
import json
import time
import threading
import logging
import helpers
from minesweeper import Minesweeper


BUF_SIZE = 1024


def sendAll(msg: str) -> None:
    global connections

    for conn in connections: conn.send(msg.encode())

def handleGame(conn: socket.socket, i: int) -> None:
    global lock, connections, disconnections
    global mspr, turn, num, start, playing

    try:
        ## Send player number
        conn.send(json.dumps({ 'type': 0, 'cont': i }).encode())

        ## Start game
        while True:
            ## Receive data
            data = conn.recv(BUF_SIZE).decode()
            if not data or not playing: break

            ## Get coordinate
            msg = json.loads(data)
            coord = msg['cont']
            col = ord(coord[0].lower()) - 96
            row = int(coord[1:])

            ## Check if it is player's turn
            if turn != i: continue

            ## Acquire lock
            with lock:
                ## Check if the cell is already uncovered
                if mspr.isUncovered(row, col):
                    conn.send(f"{json.dumps({ 'type': 2, 'cont': 'Descubierta' })}#".encode())
                    continue
                else: conn.send(f"{json.dumps({ 'type': 2, 'cont': 'Cubierta' })}#".encode())
                
                ## Generate mines if it is the first shot
                if len(mspr.mines) == 0:
                    mspr.generateMines((row, col))
                    logging.debug('Mines: %s', mspr.mines)
            
                ## Check if a mine has been hit
                if mspr.containsMine(row, col):
                    ## Send game over message
                    data = json.dumps({
                        'type': 5,
                        'cont': 'Juego terminado, seleccionaste una mina.',
                        'mines': list(mspr.mines),
                        'elapsed': time.time() - start
                    })
                    sendAll(f"{data}#")
                    playing = False
                    logging.debug('Game over')
                    continue

                ## Uncover cell
                value = mspr.uncoverCell(row, col)
                sendAll(f"{json.dumps({ 'type': 3, 'cont': coord, 'val': value })}#")

                ## Send turn
                turn = (turn + 1) % num
                while turn in disconnections: turn = (turn + 1) % num
                sendAll(f"{json.dumps({ 'type': 4, 'cont': turn })}#")

                ## Check if the game was won
                if mspr.gameWon():
                    ## Send game finished message
                    data = json.dumps({
                        'type': 5,
                        'cont': '¡Felicidades!, has ganado.',
                        'mines': list(mspr.mines),
                        'elapsed': time.time() - start
                    })
                    sendAll(f"{data}#")
                    playing = False
                    logging.debug('Game won')
    except ConnectionResetError:
        connections.pop(connections.index(conn))
        disconnections.append(i)
        logging.debug('Jugador %i desconectado', i + 1)

def acceptConnections(ss: socket.socket) -> None:
    global num, connections, cthreads
    
    ## Accept clients
    for i in range(num):
        conn, addr = ss.accept()
        logging.debug('Connected by %s', addr)

        ## Add to connection list
        connections.append(conn)

        ## Create client thread
        t = threading.Thread(target=handleGame, args=(conn, i,))
        cthreads.append(t)


## Configure logging
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.NOTSET)

## Enter host
host = helpers.getHost()
# host = '127.0.0.1'

## Enter port
port = helpers.getPort()
# port = 3000

## Enter number of connections
num = helpers.getNumConnections()
# num = 3

## Create server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
    ss.bind((host, port))
    ss.listen()
    logging.debug('Server sucessfully started on %s:%i', host, port)
    logging.info('Listening for incomming connections...')

    ## Initialize connection and thread list
    connections = []
    cthreads = []

    ## Initialize disconnection list
    disconnections = []

    ## Accept clients
    athread = threading.Thread(target=acceptConnections, args=(ss,))
    athread.start()
    athread.join()
    
    ## Create minesweeper
    mspr = Minesweeper('0')

    ## Create lock
    lock = threading.Lock()

    ## Get current time
    start = time.time()

    ## Set turn
    turn = 0

    ## Start threads
    playing = True
    for t in cthreads: t.start()

    ## Wait for threads
    for t in cthreads: t.join()

    ## Close connections
    for conn in connections: conn.close()