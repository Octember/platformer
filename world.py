import pygame
from pygame.locals import *

LAND = (186, 144, 28)
SKY = (50, 255, 255)
SHRINK = (203, 0, 0)
GROW = (50, 50, 255)
LEDGE = (0, 120, 120)

LEDGE_HEIGHT = 5
GRAVITY = 0.001

SCALE_FACTOR = 20
BLOCK_SIZE = 10

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
		return SHRINK
	elif value == 'L':
		return LEDGE
	elif value == '%':
		return GROW

class Map:

	def __init__(self, filename):
		self.load_map(filename)

	def load_map(self, filename):
		self.grid = []
		self.walls = []
		row = 0
		for line in open(filename, 'r'):
			# if line[0] == "#":
			# 	continue
			tile_row = []
			for col, char in enumerate(line.strip()):

				if char == '1':
					self.start_position = col * BLOCK_SIZE, row * BLOCK_SIZE
					char = ' '

				tile = Wall(pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), char)
				tile_row.append(tile)
				if tile.color != SKY:
					self.walls.append(tile)

			self.grid.append(tile_row)
			row += 1
		self.height, self.width = len(self.grid) * SCALE_FACTOR, len(self.grid[0]) * SCALE_FACTOR
