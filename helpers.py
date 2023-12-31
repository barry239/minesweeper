import re
import os


clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')


def getHost() -> str:
    pattern = r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$'
    while True:
        host = input('Ingrese la dirección IP: ')
        if re.match(pattern, host): return host
        print('\n[!!] Ingrese una dirección IP válida\n')

def getPort() -> int:
    pattern = r'^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$'
    while True:
        port = input('Ingrese el número de puerto: ')
        if re.match(pattern, port): return int(port)
        print('\n[!!] Ingrese un puerto válido\n')


def getNumConnections() -> int:
    pattern = r'^[1-9]\d*$'
    while True:
        num = input('Ingrese el número de conexiones: ')
        if re.match(pattern, num): return int(num)
        print('\n[!!] Ingrese un número válido\n')


def showMainMenu() -> None:
    clear()
    print('Bienvenido a Buscaminas\n')
    print('Instrucciones:')
    print('1) Elija una dificultad')
    print('2) Ingrese la coordenada de la casilla a descubrir (e.g. a1)')
    print('3) El juego finaliza al pisar una mina o descubrir todas las casillas vacías\n')
    input('Presione <Enter> para continuar...')

def showWaitingMenu() -> None:
    clear()
    print('Comenzando el juego...')

def getCoordinate() -> str:
    pattern = r'[a-z]\d{1,2}'
    while True:
        coord = input()
        if re.match(pattern, coord, re.IGNORECASE): return coord
        print('\n[!!] Elija una coordenada válida\n')
