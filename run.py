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

for row in board:
    print(" ".join(row))