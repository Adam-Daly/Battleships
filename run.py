import os
import platform
import random

# Game board class to be used by the player and computer
# The size parameter allows the board size to be specificed when creating a new board
class Game:
	def __init__(self, size=10):
		# Self.size + 1 is used to accomodate an extra row and col for chessboard notation "A1" etc
		self.size = size + 1
		# Default symbol representing a blank space
		self.space_dash = " -"
		# Dictionary of possible ships
		self.ships = {
			"Carrier": 5,
			"Battleship": 4,
			"Destroyer": 3,
			"Submarine": 3,
			"Patrol Boat": 2
		}
		# Initialize the player board
		self.player_board = self.initialize_board(self.space_dash)
		# Initialize the player ship positions
		self.player_ship_positions = self.initialize_ships()
		# Shot tracking board for showing hits and misses on opponents ships
		self.shot_tracking_board = self.initialize_board(self.space_dash)
		# Opponent board and ship positions
		self.opponent_board = self.initialize_board(self.space_dash)
		self.opponent_ship_positions = self.initialize_ships()

	# For each ship and segment in that ship, generate a row, col and hit flag
	def initialize_ships(self):
		return {
			ship_name: [{"row": None, "col": None, "hit": False} for _ in range(length)]
			for ship_name, length in self.ships.items()
		}

	# Set row 0 and col 0 to chess notation for the player to identify locations
	# Set empty space using empty_symbol parameter, such as " -"
	def initialize_board(self, empty_symbol):
		board = [[(empty_symbol) for _ in range(self.size)] for _ in range(self.size)]
		for i in range(self.size):
			for j in range(self.size):
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
	# Check if location is valid to place ship, return False otherwise
	# Ships will only ever be placed left to right, or top to bottom
	def validate_ship_position(self, board_row, board_col, ship_name, orientation):
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
		board = self.initialize_board(self.space_dash)
		if orientation == "H":
			# Check if ship can fit at chosen position
			if board_col + ship_length > self.size:
				return False
			# Loop through positive direction in horizontal orientation
			# Return False if not a valid position
			# Add position to list if valid
			for i in range(ship_length):
				if board[board_row][board_col + i] != self.space_dash:
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
				if board[board_row + i][board_col] != self.space_dash:
					return False
				else:
					positions.append((board_row + i, board_col))
		# If we haven't returned yet, all positions are valid to return
		return positions

	# Place all ships, "random" or "manually" and for "player" or "opponent". Keep track of them in a list
	def place_ships(self, agent, placement_type):
		# Get board and ship pos for specific agent
		if agent == "player":
			self.player_board = self.initialize_board(self.space_dash)
			self.player_ship_positions = self.initialize_ships()
			board, ship_positions = self.player_board, self.player_ship_positions
		elif agent == "opponent":
			self.opponent_board = self.initialize_board(self.space_dash)
			self.opponent_ship_positions = self.initialize_ships()
			board, ship_positions = self.opponent_board, self.opponent_ship_positions
		# Place random or manual, for each ship
		for ship in self.ships:
			placed = False
			while not placed:
				if placement_type == "random":
					row = random.randint(1, self.size - 1)
					col = random.randint(1, self.size - 1)
					orientation = random.choice(["V", "H"])
				elif placement_type == "manual":
					self.print()
					print(f"Pick an spot for {ship} ({self.ships[ship]} spaces) and an orientation, e.g., A1H")
					print("'H' for horizontal, left to right. 'V' for vertical, top to bottom.")
					ship_input = input()
					row, col, orientation = self.validate_input(ship_input, "placement")
				# If any are None, all are None
				if row is not None:
					checked_positions = self.validate_ship_position(row, col, ship, orientation)
					# Check that checked_position isn't False and doesn't overlap with previous ships
					if checked_positions and all(board[x][y] == ' -' for x, y in checked_positions):
						ship_letter = ship[0][:1].upper()
						for segment, (row_pos, col_pos) in enumerate(checked_positions):
							board[row_pos][col_pos] = " " + ship_letter
							ship_positions[ship][segment]["row"] = row_pos
							ship_positions[ship][segment]["col"] = col_pos
						placed = True
					else:
						if placement_type == "manual":
							print("Failed to place ship. Please pick a spot that can fit the ship. \n")
				else:
					if placement_type == "manual":
						print("Invalid input. Please enter try again. \n")

	# Helper methods to allow for player and opponent using same method, keeping signatures simple
	def player_place_ships(self, placement_type):
		self.place_ships("player", placement_type)

	def opponent_place_ships(self, placement_type):
		self.place_ships("opponent", placement_type)

	# Validate input in the form A1 or A1H, such as with chess notation but with orientation sometimes
	def validate_input(self, user_input, context):
		board_size = self.size - 1
		# Check if the input is empty
		if not user_input:
			if context == "placement":
				return None, None, None
			else:
				return None, None
		# Make sure input is the expected length
		if context == "placement":
			if len(user_input) not in {3, 4}:
				return None, None, None
		elif context == "call_shot":
			if len(user_input) not in {2, 3}:
				return None, None
		# Separate first, last and middle characters into separate variables
		letter = user_input[0].upper()
		if context == "placement":
			number = user_input[1:-1]
			orientation = user_input[-1].upper()
		elif context == "call_shot":
			number = user_input[1:]

		# Validate letter
		if not (letter.isalpha() and "A" <= letter <= chr(ord("A") + board_size - 1)):
			return (None, None, None) if context == "placement" else (None, None)
		# Validate number
		if not (number.isdigit() and 1 <= int(number) <= board_size):
			return (None, None, None) if context == "placement" else (None, None)
		if context == "placement":
			# Validate orientation
			if orientation not in ("H", "V"):
				return None, None, None
		# Convert string number to int and modify number so it matches list coordinates
		row = board_size - int(number) + 1
		# Convert letter to int
		col = ord(letter) - ord("A") + 1
		if context == "placement":
			return row, col, orientation
		elif context == "call_shot":
			return row, col

	# Get ship positions based on agent, then check check if they are hit or not, or even destroyed
	def check_shot(self, row, col, target_agent):
		if target_agent == "player":
			ship_positions = self.player_ship_positions
		elif target_agent == "opponent":
			ship_positions = self.opponent_ship_positions
		for ship_name, segments in ship_positions.items():
			for segment in segments:
				if segment["row"] == row and segment["col"] == col:
					if segment["hit"]:
						print("This part of the ship was already hit!")
					else:
						segment["hit"] = True
						print("Direct hit!")
						# Check if all segments of this ship are hit
						if all(s["hit"] for s in segments):
							print(f"The {ship_name} is destroyed!")
						return " X"
		print("Plop! Hit the water!")
		return " O"

	# Players method to take turns shooting at the opp board
	def call_shot(self):
		row = None
		while row is None:
			print("Enter a location to try to hit your opponent's ships! E.g, E5")
			location = input()
			row, col = self.validate_input(location, "call_shot")
		self.shot_tracking_board[row][col] = self.check_shot(row, col, "opponent")

	# Allows the computer to take turns and guess positions to hit
	def computer_turn(self):
		ship_positions = self.player_ship_positions

		# Find existing hits
		hit_positions = []
		for segments in ship_positions.values():
			for segment in segments:
				if segment["hit"]:
					hit_positions.append((segment["row"], segment["col"]))

		possible_moves = []
		if hit_positions:
			# Choose a random position near an existing hit
			# First, get random existing hit
			current_row, current_col = random.choice(hit_positions)
			# Loop through possible moves around the hit position
			for row_offset in [-1, 1, 0, 0]:
				for col_offset in [-1, 1, 0, 0]:
					new_row = current_row + row_offset
					new_col = current_col + col_offset
					if 0 <= new_row < self.size and 0 <= new_col < self.size:
						possible_moves.append((new_row, new_col))
		else:
			# Generate all possible positions if no hits
			possible_moves = [(row, col) for row in range(self.size) for col in range(self.size)]

		# Filter out positions that already have "O"
		valid_moves = [(row, col) for row, col in possible_moves if self.player_board[row][col] != "O"]

		# If no valid moves near hits, choose any random valid move
		if not valid_moves:
			for row in range(self.size):
				for col in range(self.size):
					if self.player_board[row][col] != "O":
						valid_moves.append((row, col))

		row, col = random.choice(valid_moves)
		self.player_board[row][col] = self.check_shot(col, row, "player")

	# Check if all ships in a list are destroyed and declare a winner if so
	def check_winner(self):
		def all_ships_destroyed(ship_positions):
			for segments in ship_positions.values():
				if not all(segment["hit"] for segment in segments):
					return False
			return True

		player_ships_destroyed = all_ships_destroyed(self.player_ship_positions)
		opponent_ships_destroyed = all_ships_destroyed(self.opponent_ship_positions)

		if player_ships_destroyed:
			print("Computer wins! Maybe next time!")
			return True
		elif opponent_ships_destroyed:
			print("Player wins! Good job!")
			return True
		else:
			return False

	# Print a single or double side by side board
	def print(self, show_tracking_board=False):
		if show_tracking_board is False:
			print("Your Board:")
			for row in self.player_board:
				print(" ".join(row))
		else:
			print("Your Board:" + "                         " + "Your Opponent's Board")
			for row1, row2 in zip(self.player_board, self.shot_tracking_board):
				print(" ".join(row1) + "    " + " ".join(row2))

# Rules for battleships
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

# Clear console depending on system
def clear_console():
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

# Main game loop
def start_game():
	game = Game()
	game.opponent_place_ships("random")
	print("Do you want to automate your ship placement? y / n")
	automate = input()
	clear_console()
	if automate.lower() == "y":
		game.player_place_ships("random")
		game.print(show_tracking_board=True)
	elif automate.lower() == "n":
		game.player_place_ships("manual")
		game.print()
	while not game.check_winner():
		print("Your turn to shoot!")
		print()
		game.call_shot()
		input("Press enter to continue...")
		clear_console()
		game.print(show_tracking_board=True)
		print("Marking board...")
		input("Press enter to continue...")
		print("Your opponent's turn to shoot!")
		print()
		game.computer_turn()
		input("Press enter to continue...")
		clear_console()
		game.print(show_tracking_board=True)
		print("Marking board...")
		input("Press enter to continue...")

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
