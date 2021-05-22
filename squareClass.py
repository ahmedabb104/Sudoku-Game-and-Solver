import pygame

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