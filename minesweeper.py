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

    def displayBoard(self) -> None:
        for i, row in enumerate(self.board):
            print(f"{' ' if self.size > 9 else ''}{i + 1:>2} | ", end='')
            print(' '.join(row))
        print(f"{' ' * (4 if self.size > 9 else 3)}+{'-' * self.size * 2}")
        print(f"{' ' * (6 if self.size > 9 else 5)}{' '.join([chr(i) for i in range(ord('a'), ord('a') + self.size)])}\n")
