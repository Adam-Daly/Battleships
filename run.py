# Game board class to be used by the player and computer
class Board:
    def __init__(self, size=10):
        self.size = size
        # Fill a list of lists with a symbol to represent blank spaces
        # self.size + 1 is used to accomodate an extra row and col for chessboard notation "A1" etc
        self.board = [[" -" for _ in range(self.size + 1)] for _ in range(self.size + 1)]
        self._initialize_board()
    
    # Set row 0 and col 0 to chess notation, 
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

    # Check if locations are empty and place ship, return False otherwise
    def place_ship(self, x, y, size, direction):
        positions = []
        # direction is either "H" for horizontal or "V" for vertical
        if direction == "H":
            if y + size > self.size:
                return False
            for i in range(size):
                if self.board[x][y + i] != " -":
                    return False
                else:
                    positions.append((x, y + i))
        elif direction == "V":
            if x + size > self.size:
                return False
            for i in range(size):
                if self.board[x + i][y] != " -":
                    return False
                else:
                    positions.append((x + i, y))
        for (x_pos, y_pos) in positions:
            self.board[x_pos][y_pos] = " X"

    def print(self):
        for row in self.board:
            print(" ".join(row)) 

# Entry point for the program
def main():
    player_board = Board()
    player_board.print()

    if player_board.place_ship(2, 2, 5, "H") == False:
        print("Cannot place ship!")
    else:
        player_board.print()

# If the script is run directly, call main
if __name__ == "__main__":
    main()