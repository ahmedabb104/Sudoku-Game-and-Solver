# Discovering and developing the backtracking algorithm needed to program a sudoku solver

# A 9x9 sudoku board is represented as a 2D list with a sublist for each row
inputBoard = [
			  [0, 0, 0, 2, 6, 0, 7, 0, 1],
			  [6, 8, 0, 0, 7, 0, 0, 9, 0],
			  [1, 9, 0, 0, 0, 4, 5, 0, 0],
			  [8, 2, 0, 1, 0, 0, 0, 4, 0],
			  [0, 0, 4, 6, 0, 2, 9, 0, 0],
			  [0, 5, 0, 0, 0, 3, 0, 2, 8],
			  [0, 0, 9, 3, 0, 0, 0, 7, 4],
			  [0, 4, 0, 0, 5, 0, 0, 3, 6],
			  [7, 0, 3, 0, 1, 8, 0, 0, 0]
			]

# Expected output:  [
				#   [4, 3, 5, 2, 6, 9, 7, 8, 1],
				#   [6, 8, 2, 5, 7, 1, 4, 9, 3],
				#   [1, 9, 7, 8, 3, 4, 5, 6, 2],
				#   [8, 2, 6, 1, 9, 5, 3, 4, 7],
				#   [3, 7, 4, 6, 8, 2, 9, 1, 5],
				#   [9, 5, 1, 7, 4, 3, 6, 2, 8],
				#   [5, 1, 9, 3, 2, 6, 8, 7, 4],
				#   [2, 4, 8, 9, 5, 7, 1, 3, 6],
				#   [7, 6, 3, 4, 1, 8, 2, 5, 9]
				# ]

def isCorrect(board, position, number):
	"""Checks if the input number is a valid move in the board position

	Args:
		board (list): The sudoku board, 9x9 2D list
		position (tuple): The position of the move, 2 value tuple (row, column)
		number (int): The input number move, an int from 1 to 9 inclusive

	Returns:
		bool: whether it is a valid move or not
	"""
	row = position[0]
	column = position[1]

	# Check the column
	for i in range(9):
		if board[i][column] == number and row != i:
			return False

	# Check the row
	for i in range(9):
		if board[row][i] == number and column != i:
			return False

	# Check the 3x3 square
	rval = row - row % 3
	cval = column - column % 3
	for i in range(3):
		for j in range(3):
			if board[i + rval][j + cval] == number and position != (i + rval, j + cval):
				return False

	return True

def emptySquare(board):
	"""Looks for an empty square on the board, returning nothing if there's none

	Args:
		board (list): The sudoku board, 9x9 2D list

	Returns:
		tuple: The position of the square, (row, column)
	"""
	for i in range(9):
		for j in range(9):
			if board[i][j] == 0:
				return (i, j)
	return

def solveBoard(board):
	"""Solves a 9x9 sudoku board

	Args:
		board (list): The sudoku board, 9x9 2D list

	Returns:
		bool: Whether the board is finished being solved or not
	"""
	square = emptySquare(board)
	if square:
		row = square[0]
		column = square[1]
	else:
		# We are done, no more empty squares
		return True

	for number in range(1,10):
		if isCorrect(board, (row, column), number):
			board[row][column] = number

			# If success
			if solveBoard(board):
				return True
			
			# If failure, reset it
			board[row][column] = 0

	# Triggers the backtracking
	return False

solveBoard(inputBoard)
print(inputBoard)