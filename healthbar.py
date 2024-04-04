import pygame
from game import Game

class HealthBar:
	def __init__(self, x, y, health, max_health):
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health
		self.game = Game()

	def draw(self, health, window):
		#update with new health
		self.health = health
		#calculate health ratio
		ratio = self.health / self.max_health
		pygame.draw.rect(window, self.game.black, (self.x - 2, self.y - 2, 154, 24))
		pygame.draw.rect(window, self.game.red, (self.x, self.y, 150, 20))
		pygame.draw.rect(window, self.game.green, (self.x, self.y, 150 * ratio, 20))


