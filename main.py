import random

class Minesweeper:
    __difficulties = {
        0: { 'size': 9, 'num': 10 },
        1: { 'size': 16, 'num': 40 }
    }

    def __init__(self, difficulty: int) -> None:
        self.size = self.__difficulties[difficulty]['size']
        self.num = self.__difficulties[difficulty]['num']
        self.mines = set()

    def genMines(self) -> None:
        while len(self.mines) < self.num:
            self.mines.add((random.randint(0, self.size - 1), random.randint(0, self.size - 1)))

mspr = Minesweeper(1)
mspr.genMines()
print(mspr.mines)
