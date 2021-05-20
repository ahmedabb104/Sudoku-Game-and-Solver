from backtracking import isCorrect, solveBoard, emptySquare
from gameFunctions import drawWindow
import pygame
from pygame.locals import *
pygame.init()

# ---------------------- Board Class ----------------------
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
		

# ---------------------- Square Class ----------------------
class Square:
	def __init__(self, num, row, column, width, height):
		self.num = num
		self.row = row
		self.column = column
		self.width = width
		self.height = height
		self.temp = 0
		self.highlighted = False

	def drawNumber(self, window):
		# Drawing the numbers
		font = pygame.font.SysFont('arial', 40)
		if self.num == 0 and self.temp != 0:
			message = font.render(str(self.temp), 1, (255, 0, 0))
			window.blit(message, (self.column * self.width + 20, self.row * self.width + 10))
		elif self.num != 0:
			message = font.render(str(self.num), 1, (0, 0, 0))
			window.blit(message, (self.column * self.width + 20, self.row * self.width + 10))

		# Highlighting the box if it's selected
		if self.highlighted:
			pygame.draw.rect(window, (255, 0, 0), (self.column * self.width, self.row * self.width, self.width, self.width), 4)

	def solvedDrawNumber(self, window):
		font = pygame.font.SysFont('arial', 40)
		message = font.render(str(self.num), 1, (0, 0, 0))
		window.blit(message, (self.column * self.width + 20, self.row * self.width + 10))

	def setNum(self, num):
		self.num = num

	def setTemp(self, num):
		self.temp = num


# ---------------------- Main Loop ----------------------
def gameLoop():
	window = pygame.display.set_mode((600, 650))
	pygame.display.set_caption("Sudoku Hax")
	sudokuBoard = Board(9, 9, 600, 600, window)
	clockObject = pygame.time.Clock()
	total_time = 0
	valueToRender = None
	quit = False

	while not quit:

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					valueToRender = 1
				if event.key == pygame.K_2:
					valueToRender = 2
				if event.key == pygame.K_3:
					valueToRender = 3
				if event.key == pygame.K_4:
					valueToRender = 4
				if event.key == pygame.K_5:
					valueToRender = 5
				if event.key == pygame.K_6:
					valueToRender = 6
				if event.key == pygame.K_7:
					valueToRender = 7
				if event.key == pygame.K_8:
					valueToRender = 8
				if event.key == pygame.K_9:
					valueToRender = 9

				if event.key == pygame.K_BACKSPACE:
					sudokuBoard.clear()
					valueToRender = None

				if event.key == pygame.K_RETURN:
					row = sudokuBoard.highlighted[0]
					column = sudokuBoard.highlighted[1]
					if sudokuBoard.squares[row][column].temp != 0:
						if sudokuBoard.validatePlayerMove(sudokuBoard.squares[row][column].temp):
							continue
						else:
							print("WRONG")

				if event.key == pygame.K_SPACE:
					sudokuBoard.solveGUIBoard()

			if event.type == pygame.MOUSEBUTTONDOWN:
				mousePosition = pygame.mouse.get_pos()
				clickPos = sudokuBoard.clickPosition(mousePosition)
				if clickPos:
					sudokuBoard.highlightSquare(clickPos[0], clickPos[1])
					valueToRender = None

			if event.type == pygame.QUIT:
				quit = True

		if valueToRender != None and sudokuBoard.highlighted:
			sudokuBoard.pencilIn(valueToRender)

		total_time = total_time + clockObject.get_time()
		drawWindow(window, sudokuBoard, total_time)
		pygame.display.update()

		clockObject.tick()

# ---------------------- Run game ----------------------
gameLoop()
pygame.quit()