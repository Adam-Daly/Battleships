BOARD_SIZE = 10

# Fill a list of lists with a symbol to represent blank spaces
# BOARD_SIZE + 1 is used to accomodate an extra row and col for chessboard notation "A1" etc
board = [[" -" for _ in range(BOARD_SIZE + 1)] for _ in range(BOARD_SIZE + 1)]

for i in range(BOARD_SIZE + 1):
    for j in range (BOARD_SIZE + 1):
        if i == 0 and j == 0:
            board[i][j] = "  "
        elif i == 0 and j > 0:
            board[i][j] = " " + chr(j + 64)
        elif j == 0:
            if (BOARD_SIZE + 1 - i) <= 9:
               board[i][j] = " " + str(BOARD_SIZE + 1 - i)
            else: 
                board[i][j] = str(BOARD_SIZE + 1 - i)

class Board:
    def __init__(self, size=10):
        self.size = size
        self.board = [[" -" for _ in range(self.size + 1)] for _ in range(self.size + 1)]
        self._initialize_board()
    
    def _initialize_board(self):
        for i in range(self.size + 1):
            for j in range (self.size + 1):
                if i == 0 and j == 0:
                    self.board[i][j] = "  "
                elif i == 0 and j > 0:
                    self.board[i][j] = " " + chr(j + 64)
                elif j == 0:
                    if (self.size + 1 - i) <= 9:
                        self.board[i][j] = " " + str(self.size + 1 - i)
                    else: 
                        self.board[i][j] = str(self.size + 1 - i)
    
    def print(self):
        for row in self.board:
            print(" ".join(row)) 

# Entry point for the program
def main():
    for row in board:
        print(" ".join(row))

    player_board = Board()
    player_board.print()

# If the script is run directly, call main
if __name__ == "__main__":
    main()