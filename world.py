import pygame
from pygame.locals import *

LAND = (186, 144, 28)
SKY = (50, 255, 255)
DEATH = (203, 0, 0)
LEDGE = (0, 120, 120)
LEDGE_HEIGHT = 2
BLOCK_SIZE = 20
GRAVITY = 0.001

class Wall:
	def __init__(self, rect, char):
		self.rect = rect
		self.color = get_color(char)

	def collide(self, other_rect):
		return self.rect.colliderect(other_rect)

def get_color(value):
	if value == ' ':
		return SKY
	elif value == '#':
		return LAND
	elif value == '$':
		return DEATH
	elif value == 'L':
		return LEDGE


def load_map(filename):
	grid = []
	solid_tiles = []
	row = 0
	for line in open(filename, 'r'):
		# if line[0] == "#":
		# 	continue
		tile_row = []
		for col, char in enumerate(line.strip()):
			tile = Wall(pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), char)
			tile_row.append(tile)
			if tile.color != SKY:
				solid_tiles.append(tile)

		grid.append(tile_row)
		row += 1
	return grid, solid_tiles