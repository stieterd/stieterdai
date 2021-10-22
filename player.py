import pygame
import math

def euclidean(a, b):
	return math.sqrt( ( (a.posx + a.size //2) - (b.posx+ a.size //2))**2 + ((a.posy+ a.size //2)  - (b.posy+ a.size //2) )**2 )


class Player:

	def __init__(self, posx, posy):

		self.posx = posx
		self.posy = posy

		self.size = 25
		self.speed = 2

		self.points = 0

		self.rect = pygame.Rect(self.posx, self.posy, self.size, self.size)

	def move(self, outputs, width, height):


		if outputs[0] == 1:

			self.posx = self.posx

		elif outputs[0] == 0:

			if outputs[1] == 0 and self.posx > self.speed:
				self.posx += -self.speed

			elif outputs[1] == 1 and self.posx < (width - self.size - self.speed):
				self.posx += self.speed

		if outputs[2] == 1:

			self.posy = self.posy

		elif outputs[2] == 0:

			if outputs[3] == 0  and self.posy > self.speed:
				self.posy += -self.speed

			elif outputs[3] == 1 and self.posy < (height - self.size - self.speed):
				self.posy += self.speed

		
		self.rect = pygame.Rect(self.posx, self.posy, self.size, self.size)

	def calculation_move(self, outputs, width, height, item):

		posx = 0
		posy = 0

		if outputs[0] == 1:

			posx = self.posx

		elif outputs[0] == 0:

			if outputs[1] == 0:
				posx += -self.speed

			elif outputs[1] == 1:
				posx += self.speed

		if outputs[2] == 1:

			posy = self.posy

		elif outputs[2] == 0:

			if outputs[3] == 0:
				posy += -self.speed

			elif outputs[3] == 1:
				posy += self.speed

		return euclidean(Player(posx, posy), item)


	def draw_player(self, screen):
		pygame.draw.rect(screen, (230, 50, 50), self.rect)


class Item:

	def __init__(self, posx, posy):
		
		self.posx = posx
		self.posy = posy

		self.size = 10

		self.rect = pygame.Rect(self.posx, self.posy, self.size, self.size)

	def draw_item(self, screen):
		pygame.draw.rect(screen, (50, 230, 50), self.rect)

	def collision(self, plr):

		if plr.rect.colliderect(self.rect):

			plr.points += 1

			return True

		else:

			return False