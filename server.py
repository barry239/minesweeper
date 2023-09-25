import socket


class Minesweeper:
    difficulties = {
        '0': { 'size': 3, 'num': 2 },
        '1': { 'size': 9, 'num': 10 },
        '2': { 'size': 16, 'num': 40 }
    }


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
        while True:
            difficulty = conn.recv(BUF_SIZE).decode()

            if difficulty in Minesweeper.difficulties:
                conn.sendall(b'Game started')
                break
            else:
                conn.sendall(b'Invalid option')
