import socket
import json
from minesweeper import Minesweeper


HOST = '127.0.0.1'
PORT = 3000
BUF_SIZE = 1024


## Create server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
    ss.bind((HOST, PORT))
    ss.listen()
    print('[+] Listening for incomming connections...')

    ## Accept client
    conn, addr = ss.accept()
    with conn:
        print('[+] Connected by', addr)

        ## Get difficulty level
        difficulty = conn.recv(BUF_SIZE).decode()
        print('[DEBUG] Game difficulty:', difficulty)

        ## Create minesweeper
        mspr = Minesweeper(difficulty)
        conn.send(b'Game started')

        ## Start game
        while True:
            ## Get coordinate
            coord = conn.recv(BUF_SIZE).decode()
            col = ord(coord[0].lower()) - 96
            row = int(coord[1:])

            ## Check if the cell is already uncovered
            if mspr.isUncovered(row, col):
                conn.send(b'Uncovered')
                continue
            else: conn.send(b'Covered')
            conn.recv(BUF_SIZE) # Unused recv

            ## Generate mines if it is the first shot
            if len(mspr.mines) == 0:
                mspr.generateMines((row, col))
                print('[DEBUG] Mines:', mspr.mines)

            ## Check if a mine has been hit
            if mspr.containsMine(row, col):
                conn.send(b'Game over')
                conn.recv(BUF_SIZE) # Unused recv
                conn.send(json.dumps(list(mspr.mines)).encode())
                print('[DEBUG] Game over')
                break

            ## Uncover cell
            value = mspr.uncoverCell(row, col)
            conn.send(value.encode())
