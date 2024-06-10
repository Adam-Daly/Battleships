import os
import platform
import random

# Game board class to be used by the player and computer
# The size parameter allows the board size to be specificed when creating a new board
class Board:
	def __init__(self, size=10):
	# Self.size + 1 is used to accomodate an extra row and col for chessboard notation "A1" etc
		self.size = size + 1
		# Default symbol representing a blank space
		self.space_dash = " -"
		# Initialize the default board
		self.board = self._initialize_board(self.space_dash)
		# Dictionary of possible ships
		self.ships = {
			"Carrier": 5,
			"Battleship": 4,
			"Destroyer": 3,
			"Submarine": 3,
			"Patrol Boat": 2
		}
		self.ship_positions = {}
		self.opp_tracking_board = self._initialize_board(self.space_dash)

	# Set row 0 and col 0 to chess notation for the player to identify locations
	def _initialize_board(self, empty_symbol):
		board = [[(empty_symbol) for _ in range(self.size)] for _ in range(self.size)]
		for i in range(self.size):
			for j in range (self.size):
				# Set the top left corner blank for visual clarity
				if i == 0 and j == 0:
					board[i][j] = "  "
				# Assign row 0 with letters, starting one before the ascii value 65 for "A", as j will be 1
				elif i == 0 and j > 0:
					board[i][j] = " " + chr(j + 64)
				# Assign numbers to col 0, descending order
				# Add a leading space to single digit numbers for visual clarity
				elif j == 0:
					if (self.size - i) <= 9:
						board[i][j] = " " + str(self.size - i)
					else:
						board[i][j] = str(self.size - i)
		return board
	# Takes an origin location, a ship name and an orientation ("H" for horizontal, "V" for vertical)
	# Check if locations are empty and place ship, return False otherwise
	# Ships will only ever be placed left to right, or top to bottom
	def place_ship(self, board_row : int, board_col : int, ship_name : str, orientation : str) -> bool:
		# Check if the row and col values are on the board
		if not (board_row in range(0, self.size) and board_col in range(0, self.size)):
			return False
		# Check if the orientation is valid
		if orientation not in {"H", "V"}:
			return False
		# Get the ship length from matching ship in ships dictionary
		ship_length = self.ships.get(ship_name)
		if ship_length is None:
			return False
		# List for storing positions until they are found valid
		positions = []
		if orientation == "H":
			# Check if ship can fit at chosen position
			if board_col + ship_length > self.size:
				return False
			# Loop through positive direction in horizontal orientation
			# Return False if not a valid position
			# Add position to list if valid
			for i in range(ship_length):
				if self.board[board_row][board_col + i] != self.space_dash:
					return False
				else:
					positions.append((board_row, board_col + i))
		elif orientation == "V":
			# Check if ship can fit at chosen position
			if board_row + ship_length > self.size:
				return False
			# Loop through positive direction in vertical orientation
			# Return False if not a valid position
			# Add position to list if valid
			for i in range(ship_length):
				if self.board[board_row + i][board_col] != self.space_dash:
					return False
				else:
					positions.append((board_row + i, board_col))
		# If we haven't returned yet, all positions are valid so we place the ship
		ship_letter = ship_name[0][:1].upper()
		for (row_pos, col_pos) in positions:
			self.board[row_pos][col_pos] = " " + ship_letter
		return True

	# Place all ships randomly for computer and optionally for player
	def randomize_ships(self):
		for ship in self.ships:
			placed = False
			while not placed:
				row = random.randint(1, self.size - 1)
				col = random.randint(1, self.size - 1)
				orientation = random.choice(["V", "H"])
				success = self.place_ship(row, col, ship, orientation)
				if success:
					self.ship_positions[ship] = (row, col, orientation)
					placed = True

	# Place ships manually with user input
	def manual_placement(self):
		print("Ships will be placed left to right or top to bottom")
		print("Ships can be in horizontal (H) or vertical (V) orientation")
		for ship in self.ships:
			placed = False
			while not placed:
				self.print()
				print(f"Pick a spot for {ship} ({self.ships[ship]} spaces) and an orientation, e.g., A1H")
				ship_input = input()
				row, col, orientation = self.validate_input(ship_input)
				print(row, col, orientation)
				# If any are None, all are None
				if row is not None:
					success = self.place_ship(row, col, ship, orientation)
					if success:
						self.ship_positions[ship] = (row, col, orientation)
						placed = True
					else: 
						print("Failed to place ship. Please pick a spot that can fit the ship. \n")
				else:
					print("Invalid input. Please enter try again. \n")

	def validate_input(self, user_input):
		board_size = self.size - 1
		# Make sure input is the expected length
		if len(user_input) not in {3, 4}:
			return None, None, None
		# Separate first, last and middle characters into separate variables
		letter = user_input[0]
		orientation = user_input[-1]
		number = user_input[1:-1]
		# Validate letter
		if not (letter.isalpha() and "A" <= letter <= chr(ord("A") + board_size - 1)):
			return None, None, None
		# Validate number
		if not (number.isdigit() and 1 <= int(number) <= board_size):
			return None, None, None
		# Validate orientation
		if orientation.upper() not in ("H", "V"):
			return None, None, None
		# Convert string number to int and modify number so it matches list coordinates
		row =  board_size - int(number) + 1
		# Convert letter to int
		col = ord(letter) - ord("A") + 1

		return row, col, orientation	

	def print(self):
		print("Your Board:" + "                         " + "Your Opponent's Board")
		for row1, row2 in zip(self.board, self.opp_tracking_board):
			print(" ".join(row1) + "    " + " ".join(row2))

def show_rules():
	rules = """
Battleships Game Rules:
1. Game Setup:
	- You and the computer have 5 ships with varying segments.
	- Ships: Carrier (5), Battleship (4), Destroyer (3),
		Submarine (3), Patrol Boat (2).

2. Placing Ships:
	- Ships placed horizontally or vertically on a 10x10 grid.
	- No overlapping or extending beyond the grid.

3. Taking Turns:
	- Players call out grid coordinates (e.g., A5, B3).
	- Hit (X) if a ship is at the coordinate; miss (O) if not.

4. Objective:
	- Sink all of the opponent's ships.
	- A ship is sunk when all its segments are hit.

5. Winning:
	- First player to sink all opponent's ships wins.

Press enter to return to the main menu...
	"""
	print(rules)

def clear_console():
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

def start_game():
	player_board = Board()

		print("Do you want to automate your ship placement? y / n")
		automate = input()
		if automate.lower() == "y":
			player_board.randomize_ships()
			player_board.print()
			input()
		elif automate.lower() == "n":
			player_board.manual_placement()
			player_board.print()
			input()

# Entry point for the program
def main():
	print("Welcome to Battleships!")
	while True:
		player_name = input("Please enter a name: \n")
		print(f"You entered {player_name}, is this correct? y / n")
		confirm_name = input()
		if confirm_name.lower() == "y":
			break

	while True:
		clear_console()
		print()
		print(f"Welcome to Battleships, {player_name}!")
		print("1. Play against the computer")
		print("2. See the rules of battleships")
		choice = input("Please choose an option \n")
		if choice.isdigit():
			choice = int(choice)
			if choice == 1:
				start_game()
			elif choice == 2:
				clear_console()
				show_rules()
				input()
		else:
			print("Please enter a valid option!")

# If the script is run directly, call main
if __name__ == "__main__":
	main()