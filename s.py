import socket
import json
import time
import re
from minesweeper import Minesweeper


BUF_SIZE = 1024


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

## Create server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
    ss.bind((host, port))
    ss.listen()
    print(f'[+] Server sucessfully started on {host}:{port}')
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

        ## Get current time
        start = time.time()

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

                ## Send mines location
                conn.send(json.dumps(list(mspr.mines)).encode())
                conn.recv(BUF_SIZE) # Unused recv

                ## Send elapsed time
                conn.send(str(time.time() - start).encode())

                print('[DEBUG] Game over')
                break

            ## Uncover cell
            value = mspr.uncoverCell(row, col)
            conn.send(value.encode())
            conn.recv(BUF_SIZE) # Unused recv

            ## Check if the game was won
            conn.send(b'Game won' if mspr.gameWon() else b'Game continues')
            if mspr.gameWon():
                conn.recv(BUF_SIZE) # Unused recv

                ## Send mines location
                conn.send(json.dumps(list(mspr.mines)).encode())
                conn.recv(BUF_SIZE) # Unused recv

                ## Send elapsed time
                conn.send(str(time.time() - start).encode())

                print('[DEBUG] Game won')
                break
