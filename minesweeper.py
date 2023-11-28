import random

class Minesweeper:
    difficulties = {
        '0': { 'size': 3, 'num': 1 },
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

    def uncoverCell(self, row: int, col: int) -> str:
        count = 0
        for i in range(max(1, row - 1), min(self.size + 1, row + 2)):
            for j in range(max(1, col - 1), min(self.size + 1, col + 2)):
                if (i, j) in self.mines: count += 1
        
        self.board[row - 1][col - 1] = str(count) if count != 0 else ' '

        return self.board[row - 1][col - 1]
    
    def showMines(self) -> None:
        for mine in self.mines:
            self.board[mine[0] - 1][mine[1] - 1] = '*'

    def displayBoard(self, num: int, turn: int = 0) -> None:
        print(f'Número de jugador: {num + 1}')
        print(f'Turno del jugador: {turn + 1}\n')
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

    def finishGame(self, msg: str, num: int, time: float) -> None:
        self.showMines()
        self.displayBoard(num)
        print('[+]', msg, f'Tiempo: {time:.2f} s')
