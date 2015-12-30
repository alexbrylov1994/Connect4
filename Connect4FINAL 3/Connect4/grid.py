#############################################################################
#			CONNECT-4 MODULE: grid.py - 03/12/2013				#
#			This module is responsible for anything				#
#			board management, or board related.					#
#		----		Designed for Python 3.3			----		#
#############################################################################
BOARD_HEIGHT = 6
BOARD_WIDTH = 7
B="_"
player_marker = "X"
ai_marker = "O"
#############################################################################

class Game_State:
	# The constructor checks if a file is provided to load, and if so, will load
	# the chosen program
	def __init__(self, filename = 'NONE', moves_made_filename = 'NONE'):				# If filenames are provided as arguments, the else statement will run, otherwise starts new
		if filename == 'NONE' and moves_made_filename == 'NONE':
			self.moves_made=[]
			self.board =	[[B,B,B,B,B,B,B], \
							 [B,B,B,B,B,B,B], \
							 [B,B,B,B,B,B,B], \
							 [B,B,B,B,B,B,B], \
							 [B,B,B,B,B,B,B], \
							 [B,B,B,B,B,B,B]]
		else:
			self.board = self.load_file(filename)										# Loads the filename if a file is provided to load
			self.moves_made = self.load_moves_made(moves_made_filename)					# Loads the moves made if a load action is being processed
			
#############################################################################
# This method gets the file to be loaded and transcribes the saved
# board into a useful self.board
	def load_file(self,filename):
			self.board = []										# Creating an empty self.board to add items to
			loadfile = open(filename, 'r')						# Opening the file that is to be loaded
			line = loadfile.readline()							# Beginning the while loop by reading the first line
			while line != '':									# Loop advances until no further lines (rows) are available
				self.board.append(line.split(","))				# Separates a row into individual items in a list by the commas between them
				line = loadfile.readline()						# Advancing the loop
			loadfile.close()
			return self.board									# Returning the filled 2D list to the constructor

#############################################################################
# A method to load the moves_made class variable which contains the moves
# made by the AI.
				
	def load_moves_made(self, moves_made_filename):
		loadfile = open(moves_made_filename, 'r')				# Opening the moves_made text file to read
		line = loadfile.readline()								# Reading all the information in the single-line file of the saved moves_made
		self.moves_made = line.split(",")						# Creating the list of saved moves made
		loadfile.close()										# Closing the opened file
		return self.moves_made									# Returning the re-created list
	
#############################################################################
# A methods to save the moves_made class variable which contains the moves
# made by the AI.
				
	def save_moves_made(self, moves_made_filename):
			moves_made_saved = open(moves_made_filename, 'w')				# Opening/writing the file chosen
			for index in range(len(self.moves_made)):						# for every member of the self.moves_made list, write it to the file
				if index < (len(self.moves_made)-1):						# If the entry in the list is not the last entry,
					moves_made_saved.write(self.moves_made[index]+',')		# then concatenate a comma to the end of the entry.
				else:														# If the entry is the last entry in the list,
					moves_made_saved.write(self.moves_made[index])			# do not concatenate a comma to the end of the entry.
#############################################################################
# This method saves the current board to a file, which can be loaded later.
	def save_board(self, filename):
		savefile = open(filename, 'w')							# Opens a file by the argument-name provided for writing
		for row in range(0, BOARD_HEIGHT):
			for column in range(0, BOARD_WIDTH):				# Gets every value on the board and writes it to the file
				savefile.write(self.board[row][column])			# as a 2D list of the same dimensions as self.board
				savefile.write(",")								# with the items separated by commas
			savefile.write('\n')								# after a row is placed on a single line, ends the line
		savefile.close()
		
#############################################################################
# A boolean method to check if the game board (all the columns) are filled
# to capacity, making further moves not possible. If they're full, it will
# exit the game.

	def board_full(self):
		board_filled = True										# If no empty space is found on the board, all columns are filled
		for row_index in range(0, BOARD_HEIGHT):
			for column_index in range (0, BOARD_WIDTH):
				if self.board[row_index][column_index]== B :	# Checking the entire board_list for an empty space, one at a time
					board_filled = False
		return board_filled										# Returns True or False to the game loop to check if additional moves are possible

#############################################################################
# A boolean method to check if a row is filled with a marker in a given column

	def check_marker(self, row, column):
		if self.board[row][column] != B :		# If a position on the board is not empty, returns True
			column_not_filled = True
		else:									# Otherwise, returns False
			column_not_filled = False
		return column_not_filled				# Returns a True or False value to the loop in assign_row


#############################################################################
# A method designed to place markers onto the board
	def place_marker(self,row,column,marker):
		self.board[row][column] = marker	# Placing the chosen marker

#############################################################################
# A method to paint the stored game board to the console
	def paint_board(self):
		print("\t\tA B C D E F G")											# Prints the labels of the columns first, indented for aesthetics
		for row_index in range(0,BOARD_HEIGHT) :
			print('\t\t', end='')											# Indents the row being printed for aesthetics
			for column_index in range(0, BOARD_WIDTH) :
				print(self.board[row_index][column_index], sep='', end=" ")	# Prints the 6x7
			print()															# Finished printing all items in the row. Print a new line to go to the next row

#############################################################################
# This function is responsible for assigning the row based on the selected
# column. If a column is completely filled, the row returned will be -1, which
# is detected as an error in ai_player, and select_button_clicked

	def assign_row(self, column):
		row=(BOARD_HEIGHT-1)								# Start by assigning the first row at the bottom
		while self.check_marker(row,column) and row>=0:		# While a marker is in the current row and the row is on the grid,
			row-=1											# go up one row and recheck.
		return row											# Returns row to ai_player.py or select_button_clicked in gui
		
#############################################################################
# The function below checks the grid for four player's or AI's markers in a row 
# in vertical, horizontal and diagonal direction

	def win_state(self,marker) :
		win= False
		# Checking from the top down, from left to right,
		# if a player has successfully connected four VERTICALLY.
		for row in range(0, BOARD_HEIGHT-3):
			for column in range(0, BOARD_WIDTH):
				if self.board[row][column]==  \
					self.board[row+1][column]== \
					self.board[row+2][column]== \
					self.board[row+3][column] == marker  :
					win= True
					return win
		# Checking from the top down, from left to right,
		# if a player has successfully connected four HORIZONTALLY.
		for row in range(0, BOARD_HEIGHT):
			for column in range(0, BOARD_WIDTH-3):
				if self.board[row][column]==  \
					self.board[row][column+1]==  \
					self.board[row][column+2]==  \
					self.board[row][column+3] == marker  :
					win= True
					return win
		# Checking from top down, from left to right,
		# if a player has successfully connected four NEGATIVE DIAGONALLY.
		for row in range(0, BOARD_HEIGHT-3):
			for column in range(0, BOARD_WIDTH-3):
				if self.board[row][column]==  \
					self.board[row+1][column+1]==  \
					self.board[row+2][column+2]==   \
					self.board[row+3][column+3] == marker  :
					win= True
					return win
		# Checking diagonally upward from top down, from left to right,
		# if a player has successfully connected four POSITIVELY DIAGONALLY.
		for row in range(3,BOARD_HEIGHT):
			for column in range(0, BOARD_WIDTH-3):
				if self.board[row][column]== \
					self.board[row-1][column+1]== \
					self.board[row-2][column+2]== \
					self.board[row-3][column+3] == marker :
					win= True
					return win

	