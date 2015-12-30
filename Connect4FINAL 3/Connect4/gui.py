#############################################################################
#			CONNECT-4 MODULE: gui.py - 03/12/2013				#
#			This module contains the game loop inside			#
#			the GUI class, and presents the game in				#
#			a visually appropriate way.							#
#		----		Designed for Python 3.3			----		#
#############################################################################
import tkinter
import tkinter.messagebox
import ai_player
import grid
from tkinter import filedialog
from grid import Game_State
from grid import BOARD_HEIGHT
from grid import BOARD_WIDTH
from grid import player_marker
from grid import ai_marker
from grid import B

################################################################################

class ConnectFourGUI :

# Creates the GUI
	def __init__(self) :
		self.main_window = tkinter.Tk()									# Setting a main window, with the following 6 items in the window
		self.main_window.title("CONNECT 4")
		select_frame = self.create_column_select_frame()				# Creating a row of column selection buttons
		board_frame = self.create_board_frame()							# Creating the game board in deactivated buttons
		marker_instruct = self.create_marker_instruct()					# Creating instructions for who's marker's are who's.
		menu_frame = self.create_menu()									# Creating a menu with save, load, and quit buttons
		
		# Labelling the row of column selection buttons
		select_label = tkinter.Label(self.main_window, \
									 text = "Select a Column", \
										font=('Helvetica',16))
		# Labelling the game board
		board_label = tkinter.Label(self.main_window, \
										text = "Board", \
										font=('Helvetica',16))
		# Positioning the created labels and frames (of buttons and messages) in the main window
		select_label.grid(row=0, column=0)
		select_frame.grid(row=1, column=0)
		board_label.grid(row=2, column=0)
		board_frame.grid(row=3, column=0)
		menu_frame.grid(row=4, column=0, columnspan=2)
		marker_instruct.grid(row=3, column=1)

		tkinter.mainloop()
	
################################################################################
# Provides instruction to the user about what their markers look like on the
# board, and what the AI's markers look like.
	
	def create_marker_instruct(self):
		frame = tkinter.Frame(self.main_window)						# Creating a frame within the main window
		self.marker_instruction_label = tkinter.Label(frame)		# Creating a label within that frame
		message = "Your pieces: "+player_marker+"\n" \
		"Computer's pieces: "+ai_marker								# The actual instruction to be printed
		self.marker_instruction_label['text'] = message				# Putting the instruction on the label in the frame
		self.marker_instruction_label.grid(row=1, column=0)			# Positioning the label within the frame
		return frame												# Returning the modified frame to the main tkinter loop
	
################################################################################	
# Returns a frame with 3 menu buttons: save, load and quit.
	def create_menu(self) :
		frame = tkinter.Frame(self.main_window)		# Creating a frame within the main window
		
		# Creating the three buttons
		save_button = tkinter.Button(frame, \
										 text='Save/Load', \
										 command = self.save_load)
		newgame_button = tkinter.Button(frame, \
										  text='New Game', \
										  command = self.new_game)
		quit_button = tkinter.Button(frame, \
										 text='Quit', \
										 command = self.main_window.destroy)
		
		# Positioning the three buttons in the created frame
		save_button.grid(row=0,column=0)
		newgame_button.grid(row=0,column=1)
		quit_button.grid(row=0,column=2)
		
		return frame								# Returning the modified frame the main tkinter loop
	
################################################################################
# Saves the current game board to a text file and the AI moves made to a text file
	
	def save_load(self) :
		self.child_window = tkinter.Toplevel(self.main_window)				# Creating a save/load window
		frame = tkinter.Frame(self.child_window)
		self.child_window.title("Save or Load a File")						# Giving a title to the save/load window
		
		# Defining all the objects within the save/load window
		self.file_entry = tkinter.Entry(frame, width=25)
		self.instructioninfo = tkinter.Label(frame, text = "Enter a filename to save or load")
		self.inputinfo = tkinter.Label(frame, text="Saves/loads as .txt")
		self.save_button = tkinter.Button(frame, text='save', command=self.game_save)
		self.save_exit_button = tkinter.Button(frame, text='save and exit', command=self.save_exit)
		self.load_button = tkinter.Button(frame, text='load', command=self.loadfile)
		self.close_button = tkinter.Button(frame, text='close', command=self.child_window.destroy)
		
		# Positioning the frames and boxes within the save/load window
		self.instructioninfo.grid(row=0,column=0)
		self.file_entry.grid(row=1,column=0)
		self.inputinfo.grid(row=2,column=0)
		self.save_button.grid(row=3,column=0)
		self.save_exit_button.grid(row=4,column=0)
		self.load_button.grid(row=3,column=1)
		self.close_button.grid(row=4,column=1)
		frame.grid(row=0,column=0)
		#filename = filedialog.asksaveasfilename()
		#self.board.save_board(filename)							# Saving the board to the file board.txt
		#tkinter.messagebox.showinfo('Message', "Game saved.")		# Let the user know that the game was successfully saved.
	
################################################################################
# A method which saves the game then continues if the 'Save' button is pushed.
# Will get a valid filename to assign the game board and moves made files to.
	
	def game_save(self) :
		filename = self.file_entry.get()+'.txt'										# Getting text input from an input window
		moves_made_filename = self.file_entry.get()+'-moves_made.txt'				# Getting the same text input from the input window
		if filename == '':
			tkinter.messagebox.showinfo('Invalid entry', "Please enter a filename to save")
			self.child_window.update()
			self.child_window.deiconify()
		else:
			self.board.save_board(filename)						# Saving the current game board to a text file
			self.board.save_moves_made(moves_made_filename)			# Saving the moves_made class list to a separate text file
			tkinter.messagebox.showinfo('Game Saved As', (" Game saved as: " + filename + ".txt"))
			self.child_window.destroy()

################################################################################
# A method which quits the game if the save and quit button is pushed.

	def save_exit(self):
		self.game_save()			# Save the game
		self.main_window.destroy()		# Then exit the game

################################################################################
# Loads a previously saved game and uses exception handling to ensure it is valid.
	
	def loadfile(self) :
		filename = self.file_entry.get()+'.txt'								# Getting the correct filename to look for
		moves_made_filename = self.file_entry.get()+'-moves_made.txt'		# Getting the correct moves_made filename to look for
		try:																# Perform exception handling to check if the filenames provided are valid
			test = open(filename, 'r')
			test2 = open(moves_made_filename, 'r')
			test.close()
			test2.close()
		except IOError:														# If the filenames are not valid, then notify the user via pop-up window and
			self.file_entry.delete(0, 20)									# clear the entry box
			tkinter.messagebox.showinfo('File Not Found', "Please enter a different file.")
			#self.child_window.update()
			#self.child_window.deiconify()
		else:																# If the load filenames are valid, then load the instance of the Game_State class.
			self.board = Game_State(filename, moves_made_filename)
			tkinter.messagebox.showinfo('Game Loaded As',(" Game loaded as: " + filename))	# Notify the user which file was loaded
			self.update_board()												# Update the GUI based on the loaded game
			self.child_window.destroy()										# Close the save/load window

################################################################################
# A method which starts a new game and updates the GUI in response to the command.

	def new_game(self) :
		self.board = Game_State()			# Reassigning self.board to a blank game board
		
		self.update_board()					# Updating the GUI to reflect the new game.
				
################################################################################
# Creates the row of column selection buttons for the user to press. If a column
# is full and the button is pushed, an error message pops up to inform the user.
	
	def create_column_select_frame(self) :
		frame = tkinter.Frame(self.main_window)				# Creating a frame within the main window
		buttons = []										# Creating an empty list to contain the 7 buttons
		
		for column_index in range(0,BOARD_WIDTH) :			# A loop to produce all 7 buttons
			letter = chr(ord('a')+column_index)				# Defining the letter for each button (a-g)
			
			# Using a lambda function to take the column from each button and
			# feed it into select_button_clicked to assign a row and place the
			# marker on the board
			button = tkinter.Button(frame, \
									text = letter, \
									command=lambda \
									column=column_index: \
									self.select_button_clicked(column))
			
			button.grid(row=1, column=column_index)			# Positioning the buttons within the created frame
		buttons.append(button)								# Populating the originally empty list with 7 buttons (a-g)
		self.select_buttons = buttons						# Renaming the list of column selection buttons
		return frame										# Returning the modified frame to the main tkinter loop

################################################################################
# Creates the actual game board out of disabled buttons in the main window
	
	def create_board_frame(self) :
		frame = tkinter.Frame(self.main_window)			# Creating a frame within the main window
		buttons = []									# Creating an empty list to hold the 42 buttons
		board = Game_State()							# Creating an instance of the class Game_State to get a new board

		for row_index in range(0,BOARD_HEIGHT) :		# Creating the individual buttons a row at a time
			row = []									# an empty list to hold a given row at a time
			for column_index in range(0,BOARD_WIDTH) :
				
				# Creates a new disabled blank button for each of the 42 squares on the board
				button = tkinter.Button(frame, \
										text = "  ", \
										state='disabled')
				
				button.grid(row=row_index, column=column_index)	# Positioning the buttons within the created frame
				row.append(button)								# Populating a single row with 7 different column buttons
			buttons.append(row)									# Populating the empty button list with 6 rows of 7 column buttons each

		self.board_buttons = buttons							# Renaming the 6x7 game board of deactivated buttons
		self.board = board										# Renaming the actual game board that contains the game data
		return frame											# Returning the modified frame the main tkinter loop

################################################################################
# When one of the column selection buttons is pushed, this code is executed
# with the column chosen from the column of the selection button (same as the
# board)
	
	def select_button_clicked(self,column) :
		row = self.board.assign_row(column)								# The row is assigned based on available spaces in a column
		if row == -1:													# If a column is filled, -1 is returned as the row (an error code)
			message = 'Column full, please pick a different column'		# The user is informed of the filled column
			tkinter.messagebox.showinfo('Error', message)				# This info is provided by a pop-up window
		else:
			self.board_marker_assign(row, column)						# If a column isn't full, placement of the markers occurs

#################################################################################
# This method determines if there is a winner and announces one, then exits the
# game.

	def has_won(self,player) :
		if player == "Player 1" :										
			if self.board.win_state(marker= player_marker) :					# If the user won,
				message = 'YOU WON'
				tkinter.messagebox.showinfo('Good job', message)				# Display a pop-up window notifying the user they won,
				self.main_window.quit()											# Then quit the game

		if player == "AI":	
			if self.board.win_state(marker= ai_marker) :						# If the AI won,
				message = 'YOU LOST'
				tkinter.messagebox.showinfo('Better luck next time', message)	# Display a pop-up window notifying the user they lost,
				self.main_window.quit()											# Then quit the game

################################################################################
# Update the board based on the stored board data

	def update_board(self):
		for row_index in range(0,BOARD_HEIGHT) :							# Iterate for every space on the board
			for column_index in range(0,BOARD_WIDTH) :
				button = self.board_buttons[row_index][column_index]		# Defining each button
				button['text'] = self.board.board[row_index][column_index]	# Put text on the buttons coinciding with what's on the game_state instance
				if button['text'] == B:										# Interpretting B as two empty spaces on the buttons for aesthetics
					button['text'] = '  '
################################################################################
# This method gets input from ai and the user and calls for pieces to be put on
# the board

	def board_marker_assign(self, row, column) :
		self.board.place_marker(row, column, player_marker)					# User's marker is placed
		self.update_board()													# Update the GUI based on the move made
		self.has_won("Player 1")											# Check if the user made a winning move, if so, end the game
		
		ai_row, ai_column = ai_player.get_choice(self.board)				# AI's row and column is obtained
		self.board.place_marker(ai_row, ai_column, ai_marker)				# AI's marker is placed
		self.update_board()													# Update the GUI based on the move made
		self.has_won("AI")													# Check if the AI made a winning move, if so, end the game
					
		if self.board.board_full():											# If the board is filled with markers, making additional moves impossible,
			message = 'No further moves possible.'+'\n'+'Ending Game.'		# the user is notified of this event and the game automatically quits
			tkinter.messagebox.showinfo('Game Over', message)				# Notification is done by pop-up window.
			self.main_window.destroy()										# Quiting the game by closing the main window


my_gui = ConnectFourGUI()							# Run the application by creating an instance of the GUI class.
