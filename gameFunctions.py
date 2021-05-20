import pygame
import time

def formatTime(milliseconds):
	seconds = int(milliseconds / 1000);
	return time.strftime('%M:%S', time.gmtime(seconds))

def drawWindow(window, board, clock):
	window.fill((248, 248, 255))
	# Drawing the board
	board.drawBoard()
	# Drawing the time
	font = pygame.font.SysFont('arial', 20)
	message = font.render(str(formatTime(clock)), 1, (0, 0, 0))
	window.blit(message, (525, 615))