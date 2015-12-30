#############################################################################
#			CONNECT-4 MODULE: ai_player.py - 03/12/2013			#
#			This module contains the the code repsonsible		#
#			for ai interaction and ai move selection to			#
#			increase the difficulty of the game.				#
#		----		Designed for Python 3.3			----		#
#############################################################################
import random
import grid
from grid import player_marker
from grid import B
from grid import BOARD_HEIGHT
from grid import BOARD_WIDTH
#############################################################################
# A function designed to randomly generate a row and column to place a
# marker in

def get_choice(board):
	row, column = authenticate_marker(board)		# Getting a valid row and column to place a marker from a different function
	return row, column								# Returning row and column to the module where AI input was called for.

#############################################################################
# A function designed to block the user's moves, or generate a random row and
# column, then return the row and column to authenticate_marker
# for validation

def determine_marker(board):
	column = None											# Setting the initial column value to None, which will be reassigned to an actual column
	row = None												# Setting the initial row value to None, which will be reassigned in this function if a random marker is placed
	column = vertical3_assign(board)						# If 3 vertically connected user-markers are found, then this will block that win-tactic by assigning column a value
	if column != None:										# If the prior check returned a value, then stop the block-tactic progression, is the same for the following repetitions
		return row, column									# Returns row as None and column as an assigned column to block, is the same for the following repetitions
	column = horizontal1space1space1_assign(board)			# If a horizontal win tactic of the form X _ X _ X is encountered, a column to block is assigned
	if column != None:
		return row, column
	column = horizontal2_assign(board)						# If 2 horizontal markers are placed beside each other, will block further progress with that horizontal win tactic
	if column != None:
		return row, column
	column = horizontal2space1_assign(board)				# If a horizontal win tactic of the form X X _ X is encountered, this will block the tactic by placing in the blank space
	if column != None:
		return row, column
	column = horizontal3_assign(board)						# If 3 horizontal markers are encountered, a marker will be placed to the right to block a horizontal win-state
	if column != None:
		return row, column
	column = positive_diagonal3_assign(board)				# If a positive diagonal tactic is encountered, will block the top-most position of the diagonal
	if column != None:
		return row, column
	column = negative_diagonal3_assign(board)				# If a negative diagonal tactic is encountered, will block the top-most position of the diagonal
	if column != None:
		return row, column
	else:													# If a block tactic is not utilized, then a random column will be selected
		column = random.randint(0,BOARD_WIDTH-1)			# Getting a random column on the board
		row = board.assign_row(column)						# Assigning a row to that column
		board.moves_made.append(str(row)+str(column))		# Recording the move to be made in the Game_State class variable of AI moves
	return row, column										# Returning the row and column for row assignment if it is None, and move validation.

#############################################################################
# A function designed to get a row and column from another function, and
# if the column and corresponding row was not randomly generated, then assign
# a row to the returned column. Following this assignment, the row and column
# are validated to be on the board, otherwise get a new row and column by
# recursion.

def authenticate_marker(board):
	row, column = determine_marker(board)			# Getting a row and column from determine_marker (row will be 'None' unless the current move is random)
	if row == None:									# If the move to be made is not random, then execute the 'if' statement
		row = board.assign_row(column)				# Assigning the appropriate row based on the determined column
	if validate_move(board, row, column):			# Checking if the move to be made falls on the board (is valid)
		row, column = authenticate_marker(board)	# If the move is not valid, then get a new row and column
	return row, column

#############################################################################
# A boolean function designed to check if the move to made falls on the board,
# otherwise a new move will be generated

def validate_move(board, row, column):
	if (row<0 or row>=BOARD_HEIGHT or column<0 or column>=BOARD_WIDTH):			# If the move to be made is not on the board, returns True
		return True
	else:
		return False															# If the move to be made is valid, then returns False
#############################################################################
# Blocks a vertical connecting tactic by the user by placing a marker in the
# same column as the user's markers after 3 user markers are connected to
# prevent further use of that column to win vertically.

def vertical3_assign(board):
	for row in range(0, BOARD_HEIGHT-2):								# Checks every row for 3 vertically connected markers from the top down.
		for column in range(0, BOARD_WIDTH):							# checks every column for 3 vertically connected markers
			# If the user has connected 3 markers vertically, and the
			# tactic has not been blocked before in that position, then
			# execute the first 'if' statement
			if board.board[row][column]==  \
				board.board[row+1][column]== \
				board.board[row+2][column]== player_marker and \
				(str(row)+str(column) not in board.moves_made):
					board.moves_made.append(str(row)+str(column))		# Adding this move to the list of moves made by the AI so far
					return column										# Returning the column the vertically connected 3 markers are in

#############################################################################
# Places a marker in the third column form the left when the horizontal win
# tactic X X _ X is encountered to prevent a horizontal win by the user.

def horizontal2space1_assign(board):
	for row in range(0, BOARD_HEIGHT):									# Checks every possible starting row for user markers of the form X X _ X
		for column in range(0, BOARD_WIDTH-3):							# Checks from every possible starting column for user markers of the form X X _ X in a row
			# If the user has connected markers of the form X X _ X, and the
			# tactic has not been blocked before in that position, then
			# execute the first 'if' statement
			if board.board[row][column] == \
				board.board[row][column+1] == \
				board.board[row][column+3] == player_marker and \
				board.board[row][column+2] == B and \
				(str(row)+str(column+2) not in board.moves_made):
				try:													# Exception handling for an error with checking the row below the bottom row (off the board)
					if board.board[row+1][column+2] != B:				# Attempts to prevent the AI from enabling the user to win horizontally
						column = column+2								# Reassigning the column to be returned to block the a horizontal win tactic by blocking the blank in X X _ X
						board.moves_made.append(str(row)+str(column))	# Adding this move to the list of moves made by the AI so far
						return column
				except IndexError:										# This exception handling is responsible for keeping the block tactic working in the bottom row
					column = column+2									# Reassigning the column to be returned to block the a horizontal win tactic by blocking the blank in X X _ X
					board.moves_made.append(str(row)+str(column))		# Adding this move to the list of moves made by the AI so far
					return column

#############################################################################
# Places a marker in the second column from the left when the instance of the
# tactic X _ X _ X is encountered to prevent advancement of this type of
# horizontal win tactic.

def horizontal1space1space1_assign(board):
	for row in range(0, BOARD_HEIGHT):									# Checks every possible starting row for user markers of the form X _ X _ X
		for column in range(0, BOARD_WIDTH-4):							# Checks from every possible starting column for user markers of the form X _ X _ X in a row
			# If the user has markers arranged X _ X _ X, and the
			# tactic has not been blocked before in that position, then
			# execute the first 'if' statement
			if board.board[row][column] == \
				board.board[row][column+2] == \
				board.board[row][column+4] == player_marker and \
				board.board[row][column+1] == \
				board.board[row][column+3] == B and\
				(str(row)+str(column+1) not in board.moves_made):
				try:													# Exception handling for an error with checking the row below the bottom row (off the board)
					if board.board[row+1][column+1] != B:				# Attempts to prevent the AI from enabling the user to win horizontally
						column = column+1								# Reassigning the column to be returned to block a horizontal win tactic of connecting 5
						board.moves_made.append(str(row)+str(column))	# Adding this move to the list of moves made by the AI so far
						return column
				except IndexError:										# This exception handling is responsible for keeping the block tactic working in the bottom row
					column = column+1									# Reassigning the column to be returned to block a horizontal win tactic of connecting 5
					board.moves_made.append(str(row)+str(column))		# Adding this move to the list of moves made by the AI so far
					return column

#############################################################################
# Places a marker to the left of 2 user connected markers, making sure it is
# not in fact 3 markers connected, to prevent the advancement of a possible
# horizontal win tactic.

def horizontal2_assign(board):
	for row in range(0, BOARD_HEIGHT):										# Checks every possible starting row for 2 connected horizontal user markers
		for column in range(0, BOARD_WIDTH-1):								# Checks from every possible starting column for 2 connected user markers in a row
			# If the user has connected 2 markers horizontally, and the
			# tactic has not been blocked before in that position, and the 2
			# connected markers aren't actually 3, then execute the first 'if'
			# statement
			if board.board[row][column]==  \
				board.board[row][column+1]== player_marker and \
				(str(row)+str(column-1) not in board.moves_made) and \
				(board.board[row][column-1] != player_marker):
					try:													# Exception handling for an error with checking the row below the bottom row (off the board)
						if board.board[row+1][column-1] != B:				# Attempts to prevent the AI from enabling the user to win horizontally
							column = column-1								# Reassigning the column to be returned to be the column to the left of the connected 2 markers
							board.moves_made.append(str(row)+str(column))	# Adding this move to the list of moves made by the AI so far
							return column
					except IndexError:										# This exception handling is responsible for keeping the block tactic working in the bottom row
						column = column-1									# Reassigning the column to be returned to be the column to the left of the connected 2 markers
						board.moves_made.append(str(row)+str(column))		# Adding this move to the list of moves made by the AI so far
						return column

#############################################################################
# Places a marker to the right of 3 connected markers by the user to block
# a horizontal connect 4. Will not place a marker in that column until
# it would be placed in the same row as the 3 connected markers.

def horizontal3_assign(board):
	for row in range(0, BOARD_HEIGHT):										# Checks every possible starting row for 3 connected horizontal user markers
		for column in range(0, BOARD_WIDTH-3):								# Checks from every possible starting column for 3 connected user markers in a row
			# If the user has connected 3 markers horizontally, and the
			# tactic has not been blocked before in that position, then
			# execute the first 'if' statement
			if board.board[row][column]==  \
				board.board[row][column+1]== \
				board.board[row][column+2] == player_marker and \
				(str(row)+str(column+3) not in board.moves_made):
					try:													# Exception handling for an error with checking the row below the bottom row (off the board)
						if board.board[row+1][column+3] != B:				# Attempts to prevent the AI from enabling the user to win horizontally
							column = column+3								# Reassigning the column to be returned to be the column to the right of the connected 3 markers
							board.moves_made.append(str(row)+str(column))	# Adding this move to the list of moves made by the AI so far
							return column
					except IndexError:										# This exception handling is responsible for keeping the block tactic working in the bottom row
						column = column+3									# Reassigning the column to be returned to be the column to the right of the connected 3 markers
						board.moves_made.append(str(row)+str(column))		# Adding this move to the list of moves made by the AI so far
						return column

#############################################################################
# Blockes a negative sloped win-tactic from the user where the 4th marker
# to be placed would be in the top left position of the connected 4 markers

def negative_diagonal3_assign(board):
	for row in range(3, BOARD_HEIGHT):										# Checks every possible starting row for a (-)ive diagonal tactic
		for column in range(3, BOARD_WIDTH):								# Checks every possible starting column in the respective row for a (-)ive diagonal tactic
			# If the user has connected 3 markers with a (-)ive slope, and
			# the tactic has not been blocked before in that position, then
			# execute the first 'if' statement
			if board.board[row][column] == \
				board.board[row-1][column-1] == \
				board.board[row-2][column-2] == player_marker and \
				(str(row-3)+str(column-3) not in board.moves_made):
					if board.board[row-2][column-3] != B:					# Prevents the AI from enabling the user to win with a negative slope
						column = column-3									# Changing the column to where the top position in the 3-marker line is located
						board.moves_made.append(str(row-3)+str(column))		# Adding the made move to the list of moves made so far
						return column

#############################################################################
# Designed to block the user if they are attempting to connect 4 diagonally
# up and to the right ((+)ive slope)

def positive_diagonal3_assign(board):
	for row in range(3,BOARD_HEIGHT):										# Checks every possible starting row for a (+)ive diagonal tactic
		for column in range(0, BOARD_WIDTH-3):								# Checks every possible starting column in the respective row for a (+)ive diagonal tactic
			# If the user has connected 3 markers with a (+)ive slope, and
			# the tactic has not been blocked before in that position, then
			# execute the first 'if' statement
			if board.board[row][column]== \
				board.board[row-1][column+1]== \
				board.board[row-2][column+2]== player_marker and \
				((str(row-3)+str(column+3)) not in board.moves_made):
						if board.board[row-2][column+3] != B:				# Prevents the AI from enabling the user to win with a positive slope
							column = column+3								# Changing the column to where the top position in the 3-marker line is located
							board.moves_made.append(str(row-3)+str(column))	# Adding the made move to the list of moves made so far
							return column
