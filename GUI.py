from boardClass import *
from gameFunctions import drawWindow
import pygame
from pygame.locals import *
pygame.init()

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