#############################################################################
#			CONNECT-4 MODULE: player.py - 03/12/2013			#
#			This module contains all the code reponsible		#
#			for user interaction and user input handling		#
#			to prevent the game from crashing based on			#
#			input provided										#
#		----		Designed for Python 3.3			----		#
#############################################################################
import grid
from grid import BOARD_WIDTH
#############################################################################
# A function designed to get input for a column from the user, or a command
# to save, load, or quit, and the assigned row

def get_input(board):
	column, row = handle_input(board)				# Getting a useable input and assigned row
	return column, row								# Returning these two values for use

#############################################################################
# A function which handles the input it obtains and returns valid variables
# to get_input

def handle_input(board):
	print("Enter the location for a marker, or",
		  "Enter 'q' to quit, or",
		  "Enter 'load' to load a text save-file by name, or",
		  "Enter 'save' to save a text save-file by name", '', sep='\n', end='\n')		# Providing the available options for the user to utilize
	player_input = input("Column (a-g): ").lower()										# Obtaining non-case sensitive input from the user
	row = None																			# Assigning the row to None to avoid errors if a quit, load or save command is chosen
	if player_input == "q":																# If the obtained input is 'q', indicates the user wants to quit the game
		return player_input, row														# Return 'q' to be utilized in a different module
	elif player_input == "load":														# If obtained input is 'load', indicates the user wants to load a save
		return player_input, row														# Returns 'load' to be utilized in a different module
	elif player_input == "save":														# If obtained input is 'save', indicates the user wants to save the game
		return player_input, row														# Returns 'save' to be utilized in a different module
	else:																				# If the user did not enter one of these commands, then the input will be checked for move use
		player_input, row = validate_move(board, player_input)							# Reassigning the value to be returned based on validation for legal moves
		return player_input, row														# Returns a valid column and valid row to be used for marker placement

#############################################################################
# A function which validates the move the user wishes to make, and returns
# a valid value after a new value is obtained by recursion (if necessary)

def validate_move(board, player_input):
	try:							# Exception handling for the ord() call to prevent TypeError's from crashing the game with bad input
		if ord(player_input)>=ord("a") and ord(player_input)<(ord("a")+BOARD_WIDTH):				# If the column to be used is on the board
			column = ord(player_input)-ord("a")														# Convert this column string to a useable integer
			row = board.assign_row(column)															# Assign the appropriate row based on the selected column
			if row == -1:																			# If the row assigned is -1, then the column is full, so get a new column
				print('' , "ERROR: Column Full. Please enter a different column.", '', sep='\n')	# Inform the user the column is full
				column, row = handle_input(board)													# Get a new column/row or a command
				return column, row
			else:																					# If the column is not full, then return the column, row coordinates
				return column, row
		else:																						# If the column to be used is not on the board/invalid
			print('' , "Invalid input. Please enter a different command", '', sep='\n')				# Inform the user
			player_input, row = handle_input(board)													# And get new input
			return player_input, row
	except TypeError:																				# If a TypeError traceback is raised, then consider the input invalid
			print('' , "Invalid input. Please enter a different command", '', sep='\n')				# So inform the user
			player_input, row = handle_input(board)													# And get new input
			return player_input, row

