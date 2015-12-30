#############################################################################
#			CONNECT-4 MODULE: main.py - 03/12/2013				#
#			This module contains the game loop inside			#
#			a main function, and presents the game in			#
#			a visually appropriate way in the console.			#
#		----		Designed for Python 3.3			----		#
#############################################################################
import player
import ai_player
from grid import Game_State
from grid import player_marker
from grid import ai_marker
#############################################################################
# The main function contains the game loop, and will loop until the user wishes
# to quit, the board is filled, or either the ai or the user wins the game. When
# the loop ends, the game will exit.
def main():
	game_state = 'INIT'									# Setting the game_state to INIT (initialize)
	board = Game_State()								# Calling an instance of the Game_State class to get a board
	
	while game_state != 'EXIT':							# If the game state becomes EXIT at any time, the game will quit, otherwise it will loop.
		
		if game_state == 'INIT':
			show_title(board)							# Showing a welcome screen and starting instructions, and an empty game board
			game_state = 'LOOP'							# Entering the game loop
		
		elif game_state == 'LOOP':
			column, row = player.get_input(board) 		# Retrieving a column and row from the player, the column can also be a save/load/quit command
			
			if column == "q":							# If the column is returned as 'q', the game will quit
				print("Exiting program.")				# Providing information about the action being taken.
				game_state = 'EXIT'
			
			elif column == "load" :						# If the column is returned as 'load' then the user will be prompted to load a saved file.
				board = get_and_load_files(board)		# Reassigns the board to the loaded board if a board is loaded, otherwise nothing changes
				print("Resuming game:", '\n')			# Extra line is for aesthetic purposes.
				board.paint_board()						# Shows the board of the game being resumed.
	
			elif column == "save" :						# If the column is returned as 'save' then the user will be prompted to save the game to a file
				game_save(board)						# Prompts the user for a file and saves the game to that file, or allows the user to cancel that command
	
			else:										# If the user chose not to quit, load, or save then play will occur
				board.place_marker(row, column, player_marker)				# Placing the user's marker to the board from the chosen column and assigned row
				
				if has_won(board, "Player 1"):								# If this move resulted in the user winning, then the user will be informed,
					board.paint_board()										# the winning board case will be printed,
					game_state = 'EXIT'										# and the game will quit.
					return game_state
				
				ai_row, ai_column = ai_player.get_choice(board)				# Retrieving input from the ai player
				board.place_marker(ai_row, ai_column, ai_marker)			# Placing the ai's markers on the board
				
				if has_won(board, "AI"):									# If this move resulted in the AI winning, then the user will be informed,
					board.paint_board()										# the winning board case will be printed,
					game_state = 'EXIT'										# and the game will quit.
					return game_state
				
				elif board.board_full():									# If no further moves are possible (board is full),
					print("Game board full. No further moves possible.",	# inform the user of the scenario,
						  "Exiting Game....", sep='\n')
					board.paint_board()										# show the filled board,
					game_state = 'EXIT'										# then exit the game.
					return game_state
				
				board.paint_board()					# Prints the current game board after this round of moves.
				print()								# And an empty line for aesthetic purposes

	
	
	exit()										# If the game state becomes 'EXIT', then the game will quit.

################################################################################
# A function designed to show the welcome screen and blank board
def show_title(board) :
	print("============ WELCOME TO CONNECT - 4 ============")
	print("Your markers: "+player_marker,
		  "Computer's markers: "+ai_marker,
		  "Empty Board:", sep='\n',end='\n')									# Informing the user of whose markers are whose
	board.paint_board()															# Printing empty board for user reference
	print('', "Hello, Player 1. Make your first move please.", '', sep='\n')	# Instructing the user to make a move, empty lines are for aesthetics

################################################################################
# A function which gets the filenames to be loaded and either cancels the process
# of loading as per the user's input, or loads the files.

def get_and_load_files(board):
	filename, moves_made_filename = get_file()							# Getting filenames to load, or filename=None if the user wishes to cancel the load
	if filename == None:												# If the user wants to cancel the load command,
		return board													# then return the current board state
	else:																# Otherwise reassign the current board state to the saved board state
		board = loadfile(board, filename, moves_made_filename)			# Reassigns board to the saved board state
		return board													# Returns the new board state
#################################################################################
# A function which gets a filename from the user, and creates the moves_made file
# from the filename provided. If the user enters an empty filename, this is taken
# as a cancel command.
def get_file():
	print()																	# An empty line for aesthetic purposes
	filename = input("Please enter a filename or [ENTER] to cancel: ")		# Getting a filename from the user, if it is empty, then that indicates cancel
	moves_made_filename = filename+"-moves_made.txt"						# Creating the moves_made filename from the filename by concatenation
	filename = filename+".txt"												# Creating a txt saveable filename by concatenation
	if filename == '.txt':													# If the filename was input as '', then this indicates a cancel of the load command
		filename = None														# Reassign the filename to be None to indicate this cancellation
	return filename, moves_made_filename									# Return the filename and the determined moves_made_filename for use or not

#################################################################################
# A function which loads the game, and to quit the function, the user can enter
# an empty filename.

def loadfile(board, filename, moves_made_filename):
	try:																# Perform exception handling to check if the filenames provided are valid
		test = open(filename, 'r')
		test2 = open(moves_made_filename, 'r')
		test.close()
		test2.close()
	except IOError:														# If they filenames are not valid, then a new filename will be obtained
		print("Invalid file, please enter a valid command.")
		board = get_and_load_files(board)
		return board
	else:																# If the filenames are valid:
		board = Game_State(filename, moves_made_filename)					# Reassigns board to the loaded board case
		print(" =============== Load Successful ! ===============", '\n')	# User is notified the load was successful, newlines are for aesthetics
		return board

#################################################################################
# This function serves to save the current board and ai moves made to a file
# chosen by the user, and can be canceled by the user entering an empty filename.

def game_save(board):
	filename, moves_made_filename = get_file()							# Getting the filenames to be saved
	if filename != None:												# If filename is returned as None, nothing will happen; otherwise,
		board.save_board(filename)										# the board will be saved,
		board.save_moves_made(moves_made_filename)						# along with the ai moves made
		print("------------- Save Successful ! -------------", '\n')	# and the user will be notified the save worked, newlines are for aesthetics.

#################################################################################
# This boolean type function determines if there is a winner and announces the
# respective message if the user won or lost.

def has_won(board, player) :
	if player == "Player 1":
		if board.win_state(player_marker) :						# If the user won,
			print("|--------------------|")
			print("|-------YOU WIN------|")						# Display a win statement
			print("|--------------------|")
			return True
	
	if player == "AI":
		if board.win_state(ai_marker) :							# If the AI won,
			print("|--------------------|")
			print("|------YOU LOSE------|")						# Display a lose statement
			print("|--------------------|")
			return True

main()			# Calling the main function.
