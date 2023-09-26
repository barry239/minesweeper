import socket
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
        conn.sendall(b'Game started')

        ## Start game
        while True:
            ## Get coordinate
            coord = conn.recv(BUF_SIZE).decode()
            col = ord(coord[0].lower()) - 96
            row = int(coord[1:])

            ## Check if the cell is already uncovered
            if mspr.isUncovered(row, col):
                conn.sendall(b'Uncovered')
                continue
            else: conn.sendall(b'Covered')

            ## Generate mines if it is the first shot
            if len(mspr.mines) == 0:
                mspr.generateMines((row, col))
                print('[DEBUG] Mines:', mspr.mines)

            print(f'({row},{col})')
