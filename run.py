chessboard = [
    ["BS", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
    ["10", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["09", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["08", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["07", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["06", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["05", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["04", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["03", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["02", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["01", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]
]

for row in chessboard:
    print(row)

BOARD_SIZE = 10

# Fill a list of lists with a symbol to represent blank spaces
# BOARD_SIZE + 1 is used to accomodate an extra row and col for chessboard notation "A1" etc
board = [["-" for _ in range(BOARD_SIZE + 1)] for _ in range(BOARD_SIZE + 1)]

for i in range(BOARD_SIZE + 1):
    for j in range (BOARD_SIZE + 1):
        if i and j == 0:
            board[i][j] = "BS"
        elif i == 0 and j > 0:
            board[i][j] = chr(i + 64)
        elif j == 0:
            board[i][j] = str(BOARD_SIZE - 1 - i)

for row in board:
    print(row)