import random
import os

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

class Minesweeper:
    __difficulties = {
        1: { 'size': 9, 'num': 10 },
        2: { 'size': 16, 'num': 40 }
    }

    def __init__(self, difficulty: int) -> None:
        self.size = self.__difficulties[difficulty]['size']
        self.num = self.__difficulties[difficulty]['num']
        self.board = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.mines = set()

    def generateMines(self) -> None:
        while len(self.mines) < self.num:
            self.mines.add((random.randint(1, self.size), random.randint(1, self.size)))

    def containsMine(self, row: int, col: int) -> bool:
        return (row, col) in self.mines
    
    def uncoverCell(self, row: int, col: int) -> None:
        count = 0
        for i in range(max(1, row - 1), min(self.size + 1, row + 2)):
            for j in range(max(1, col - 1), min(self.size + 1, col + 2)):
                if (i, j) in self.mines: count += 1
        
        self.board[row - 1][col - 1] = str(count)

    def showMines(self) -> None:
        for mine in self.mines:
            self.board[mine[0] - 1][mine[1] - 1] = '*'

    def displayBoard(self) -> None:
        for i, row in enumerate(self.board):
            print(f"{' ' if self.size > 9 else ''}{i + 1:>2} | ", end='')
            print(' '.join(row))
        print(f"{' ' * (4 if self.size > 9 else 3)}+{'-' * self.size * 2}")
        print(f"{' ' * (6 if self.size > 9 else 5)}{' '.join([chr(i) for i in range(ord('a'), ord('a') + self.size)])}\n")

    def finishGame(self, msg: str) -> None:
        self.showMines()
        self.displayBoard()
        print('[+]', msg)


## Show main menu
clear()
print('Elija la dificultad:')
print('1) Principiante - 9 x 9 casillas, 10 minas')
print('2) Avanzado - 16 x 16 casillas, 40 minas\n')
difficulty = int(input())

## Create minesweeper
mspr = Minesweeper(difficulty)
mspr.generateMines()

## Start game
while True:
    ## Display board
    clear()
    mspr.displayBoard()
    print('[DEBUG]', mspr.mines)

    ## Enter coordinates
    row = int(input('Ingrese la fila: '))
    col = int(input('Ingrese la columna: '))

    ## Check if a mine has been hit
    if mspr.containsMine(row, col):
        clear()
        mspr.finishGame('Juego terminado, seleccionaste una mina')
        break

    ## Uncover cell
    mspr.uncoverCell(row, col)
