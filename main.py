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

    def containsMine(self, x: int, y: int) -> bool:
        return (x, y) in self.mines

    def showMines(self) -> None:
        for mine in self.mines:
            self.board[mine[0] - 1][mine[1] - 1] = '*'

    def displayBoard(self) -> None:
        for i, row in enumerate(self.board):
            print(f' {i + 1:>2} | ', end='')
            print(' '.join(row))
        print(f"{' ' * 4}+{'-' * self.size * 2}")
        print(f"{' ' * 6}{' '.join([chr(i) for i in range(ord('a'), ord('a') + self.size)])}\n")

clear()
print('Elija la dificultad:')
print('1) Principiante - 9 x 9 casillas, 10 minas')
print('2) Avanzado - 16 x 16 casillas, 40 minas\n')
difficulty = int(input())

mspr = Minesweeper(difficulty)
mspr.generateMines()

while True:
    clear()
    print('[DEBUG]', mspr.mines)
    mspr.displayBoard()

    x = int(input('Ingrese x: '))
    y = int(input('Ingrese y: '))

    if mspr.containsMine(x, y): mspr.showMines()
