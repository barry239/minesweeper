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
    global mspr, start, connections

    try:
        ## Send player number
        conn.send(json.dumps({'type': 0, 'cont': i}).encode())

        ## Start game
        playing = True
        while playing:
            ## Get coordinate
            msg = json.loads(conn.recv(BUF_SIZE).decode())
            coord = msg['cont']
            col = ord(coord[0].lower()) - 96
            row = int(coord[1:])

            ## Check if the cell is already uncovered
            if mspr.isUncovered(row, col):
                conn.send(json.dumps({'type': 2, 'cont': 'Uncovered'}).encode())
                continue
            else: conn.send(json.dumps({'type': 2, 'cont': 'Covered'}).encode())

            ## Generate mines if it is the first shot
            if len(mspr.mines) == 0:
                mspr.generateMines((row, col))
                logging.debug('Mines: %s', mspr.mines)
            
            ## Check if a mine has been hit
            if mspr.containsMine(row, col):
                sendAll(json.dumps({'type': 4, 'cont': 'Game over'}))
                time.sleep(1.2)

                ## Send mines location
                conn.recv(BUF_SIZE) # Unused recv
                time.sleep(1.2)
                sendAll(json.dumps({'type': 6, 'cont': list(mspr.mines)}))
                time.sleep(1.2)

                ## Send elapsed time
                conn.recv(BUF_SIZE) # Unused recv
                time.sleep(1.2)
                sendAll(json.dumps({'type': 7, 'cont': time.time() - start}))

                logging.debug('Game over')
                playing = False

            ## Uncover cell
            value = mspr.uncoverCell(row, col)
            sendAll(json.dumps({'type': 3, 'cont': coord, 'val': value}))

            ## Check if the game was won
            if mspr.gameWon():
                sendAll(json.dumps({'type': 5, 'cont': 'Game won'}))

                ## Send mines location
                conn.recv(BUF_SIZE) # Unused recv
                sendAll(json.dumps({'type': 6, 'cont': list(mspr.mines)}))

                ## Send elapsed time
                conn.recv(BUF_SIZE) # Unused recv
                sendAll(json.dumps({'type': 7, 'cont': time.time() - start}))

                logging.debug('Game won')
                playing = False
    except ConnectionResetError:
        connections.pop(connections.index(conn))
        logging.debug('Jugador %i desconectado', i)

def acceptConnections(ss: socket.socket) -> None:
    global num, connections, cthreads
    
    for i in range(num):
        conn, addr = ss.accept()
        logging.debug('Connected by %s', addr)

        ## Add to connection list
        connections.append(conn)

        ## Create client thread
        t = threading.Thread(target=handleGame, args=(conn, i))
        cthreads.append(t)


## Configure logging
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.NOTSET)

## Enter host
# host = helpers.getHost()
host = '127.0.0.1'

## Enter port
# port = helpers.getPort()
port = 3000

## Enter number of connections
# num = helpers.getNumConnections()
num = 2

## Create server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
    ss.bind((host, port))
    ss.listen()
    logging.debug('Server sucessfully started on %s:%s', host, port)
    logging.info('Listening for incomming connections...')

    ## Accept clients
    connections = []
    cthreads = []
    athread = threading.Thread(target=acceptConnections, args=(ss,))
    athread.start()
    athread.join()
    
    ## Create minesweeper
    mspr = Minesweeper('0')

    ## Get current time
    start = time.time()

    ## Start threads
    for t in cthreads: t.start()

    ## Wait for threads
    for t in cthreads: t.join()

    ## Close connections
    for conn in connections: conn.close()