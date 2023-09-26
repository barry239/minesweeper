import random

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

    def displayBoard(self) -> None:
        for i, row in enumerate(self.board):
            print(f"{' ' if self.size > 9 else ''}{i + 1:>2} | ", end='')
            print(' '.join(row))
        print(f"{' ' * (4 if self.size > 9 else 3)}+{'-' * self.size * 2}")
        print(f"{' ' * (6 if self.size > 9 else 5)}{' '.join([chr(i) for i in range(ord('a'), ord('a') + self.size)])}\n")

    def isUncovered(self, row: int, col: int) -> bool:
        return self.board[row - 1][col - 1] != '.'
