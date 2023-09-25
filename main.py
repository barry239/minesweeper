import random
import os

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

class Minesweeper:
    __difficulties = {
        1: { 'size': 10, 'num': 10 },
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

    def displayBoard(self) -> None:
        for i, row in enumerate(self.board):
            print(f' {i + 1:>2} | ', end='')
            print(' '.join(row))
        print(f"{' ' * 4}+{'-' * self.size * 2}")
        print(f"{' ' * 6}{' '.join([chr(i) for i in range(ord('a'), ord('a') + self.size)])}")

clear()
print('Elija la dificultad:')
print('1) Principiante - 9 x 9 casillas, 10 minas')
print('2) Avanzado - 16 x 16 casillas, 40 minas\n')
difficulty = input()

mspr = Minesweeper(int(difficulty))
mspr.generateMines()

clear()
mspr.displayBoard()
