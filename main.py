import pygame, sys
from pygame.locals import *

import player
import neural

import random
import math

pygame.init()
pygame.font.init() 

WIDTH = 1200
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

plr = player.Player(20, 20)

itemsize = 10
item = player.Item(random.randint(0, WIDTH-itemsize), random.randint(0, HEIGHT-itemsize))

nn = neural.Network(4,8,4)
LR = 0.05

clock = pygame.time.Clock()
myfont = pygame.font.Font(None, 36)

accuracy = []

while True: # main game loop
	
 
	## set up the background & shit ##
	clock.tick(120)

	screen.fill((30,30,30))

	for event in pygame.event.get():

		if event.type == QUIT:

			pygame.quit()

			sys.exit()

	## Working with the item ##
	item.draw_item(screen)

	if item.collision(plr):
		item = player.Item(random.randint(0, WIDTH-10), random.randint(0, HEIGHT-10))

	## Working with the player ##
	plr.draw_player(screen)


	## Neural Network stuff ##

	labels = get_labels(plr, item)
	row = [plr.posx, plr.posy, item.posx, item.posy]

	outputs = nn.forward_propagate(row)
	outputs = [round(x) for x in outputs]

	nn.backward_propagate(labels)
	nn.update_weights(row, LR)
	
	dist1 = player.euclidean(item, plr)
	plr.move(outputs, WIDTH, HEIGHT)
	dist2 = player.euclidean(item, plr)

	accuracy.append(right_wrong(dist1, dist2))


	textsurface = myfont.render(f"{round( sum(accuracy) /len(accuracy) * 100, 1)}% accuracy", False, (230, 230, 230))
	screen.blit(textsurface, (30,30))

	pygame.display.update()


