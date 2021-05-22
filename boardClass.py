from squareClass import *
from backtracking import *

class Board:
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

	def __init__(self, rows, columns, width, height, window):
		self.rows = rows
		self.columns = columns
		self.width = width
		self.height = height
		self.window = window
		self.squares = [[Square(self.inputBoard[i][j], i, j, width/9, height/9) for j in range(columns)] for i in range(rows)]
		self.highlighted = None
		self.state = None

	def drawBoard(self):
		# Draw the grid
		gridGap = self.height / 9
		for i in range(self.rows + 1):
			if i == 3 or i == 6:
				gridLine = 4
				colour = (0, 0, 0) 
			else:
				gridLine = 1
				colour = (128, 128, 128)
			# Horizontal grid lines
			pygame.draw.line(self.window, colour, (0, gridGap * i), (self.width, gridGap * i),gridLine)
			# Vertical grid lines
			pygame.draw.line(self.window, colour, (gridGap * i, 0), (gridGap * i, self.height), gridLine)

		# Draw the numbers
		for i in range(self.rows):
			for j in range(self.columns):
				self.squares[i][j].drawNumber(self.window)

	# Will return position in the form (row, column)
	def clickPosition(self, mousePosition):
		return (int(mousePosition[1] // (self.width / 9)), int(mousePosition[0] // (self.width / 9)))

	def highlightSquare(self, row, column):
		# First reset any other highlighted squares
		for i in range(self.rows):
			for j in range(self.columns):
				self.squares[i][j].highlighted = False

		# Handle properties for both the square and board
		self.squares[row][column].highlighted = True
		self.highlighted = (row, column)

	# Allows the user to see their move before confirming
	def pencilIn(self, num):
		row = self.highlighted[0]
		column = self.highlighted[1]
		self.squares[row][column].setTemp(num)

	# Allows the user to clear their move
	def clear(self):
		row = self.highlighted[0]
		column = self.highlighted[1]
		self.squares[row][column].setTemp(0)

	def validatePlayerMove(self, num):
		row = self.highlighted[0]
		column = self.highlighted[1]

		# If it's an empty square, allow it as long as it's correct
		if self.squares[row][column].num == 0:
			self.squares[row][column].setNum(num)
			self.updateState()
			if isCorrect(self.state, (row, column), num) and solveBoard(self.state):
				return True
			else:
				self.squares[row][column].setNum(0)
				self.squares[row][column].setTemp(0)
				self.updateState()
				return False

	# Redefining the backtracking algorithm to work with a GUI
	def solveGUIBoard(self):
		self.updateState()
		square = emptySquare(self.state)
		if square:
			row = square[0]
			column = square[1]
		else:
			return True
		
		for number in range(1,10):
			if isCorrect(self.state, (row, column), number):
				self.state[row][column] = number
				self.squares[row][column].setNum(number)
				self.squares[row][column].solvedDrawNumber(self.window)
				self.updateState()

				if self.solveGUIBoard():
					return True

				self.state[row][column] = 0
				self.squares[row][column].setNum(0)
				self.updateState()
				self.squares[row][column].solvedDrawNumber(self.window)

		return False

	# Updates the state of the board after moves have been made
	def updateState(self):
		self.state = [[self.squares[i][j].num for j in range(self.columns)] for i in range(self.rows)]

	# Checks for empty squares in the board
	def gameDone(self):
		for i in range(self.rows):
			for j in range(self.columns):
				if self.squares[i][j].num == 0:
					return False
		return True