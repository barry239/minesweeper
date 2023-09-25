import random
import os
import re

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

class Minesweeper:
    difficulties = {
        '0': { 'size': 3, 'num': 2 },
        '1': { 'size': 9, 'num': 10 },
        '2': { 'size': 16, 'num': 40 }
    }

    def __init__(self, difficulty: str) -> None:
        self.size = self.difficulties[difficulty]['size']
        self.num = self.difficulties[difficulty]['num']
        self.board = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.mines = set()

    def generateMines(self, seed: tuple[int, int]) -> None:
        while len(self.mines) < self.num:
            mine = (random.randint(1, self.size), random.randint(1, self.size))
            if mine != seed: self.mines.add(mine)
    
    def uncoverCell(self, row: int, col: int) -> None:
        count = 0
        for i in range(max(1, row - 1), min(self.size + 1, row + 2)):
            for j in range(max(1, col - 1), min(self.size + 1, col + 2)):
                if (i, j) in self.mines: count += 1
        
        self.board[row - 1][col - 1] = str(count) if count != 0 else ' '

    def showMines(self) -> None:
        for mine in self.mines:
            self.board[mine[0] - 1][mine[1] - 1] = '*'

    def displayBoard(self) -> None:
        for i, row in enumerate(self.board):
            print(f"{' ' if self.size > 9 else ''}{i + 1:>2} | ", end='')
            print(' '.join(row))
        print(f"{' ' * (4 if self.size > 9 else 3)}+{'-' * self.size * 2}")
        print(f"{' ' * (6 if self.size > 9 else 5)}{' '.join([chr(i) for i in range(ord('a'), ord('a') + self.size)])}\n")

    def isUncovered(self, row: int, col: int) -> bool:
        return self.board[row - 1][col - 1] != '.'

    def containsMine(self, row: int, col: int) -> bool:
        return (row, col) in self.mines
    
    def gameWon(self) -> bool:
        count = 0
        for row in self.board:
            count += row.count('.')
        
        return count == self.num

    def finishGame(self, msg: str) -> None:
        self.showMines()
        self.displayBoard()
        print('[+]', msg)


## Show main menu
clear()
print('Bienvenido a Buscaminas\n')
print('Instrucciones:')
print('1) Elija una dificultad')
print('2) Ingrese la coordenada de la casilla a descubrir (e.g. a1)')
print('3) El juego finaliza al pisar una mina o descubrir todas las casillas vacías\n')
input('Presione <Enter> para continuar...')

## Select difficulty level
while True:
    clear()
    print('1) Principiante - 9 x 9 casillas, 10 minas')
    print('2) Avanzado - 16 x 16 casillas, 40 minas\n')
    difficulty = input('Elija la dificultad: ')

    if difficulty not in Minesweeper.difficulties:
        print('\n[!!] Elija una opción correcta\n')
        input('Presione <Enter> para continuar...')
    else:
        break

## Create minesweeper
mspr = Minesweeper(difficulty)

## Start game
while True:
    ## Display board
    clear()
    mspr.displayBoard()
    print('[DEBUG]', mspr.mines)

    ## Get coordinate
    coord = input('Ingrese la coordenada: ')
    if not re.match(r'[a-z]\d{1,2}', coord, re.IGNORECASE):
        print('\n[!!] Elija una coordenada válida\n')
        input('Presione <Enter> para continuar...')
        continue
    col = ord(coord[0].lower()) - 96
    row = int(coord[1:])

    ## Check if the cell is already uncovered
    if mspr.isUncovered(row, col): continue

    ## Generate mines if it is the first shot
    if len(mspr.mines) == 0: mspr.generateMines((row, col))

    ## Check if a mine has been hit
    if mspr.containsMine(row, col):
        clear()
        mspr.finishGame('Juego terminado, seleccionaste una mina')
        break

    ## Uncover cell
    mspr.uncoverCell(row, col)

    ## Check if the game was won
    if mspr.gameWon():
        clear()
        mspr.finishGame('¡Felicidades!, has ganado')
        break
