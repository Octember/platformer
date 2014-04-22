import pygame
from pygame.locals import *
from sprites import Goomba

from globals import *

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
		self.enemies = []
		row = 0
		for line in open(filename, 'r'):
			# if line[0] == "#":
			# 	continue
			tile_row = []
			for col, char in enumerate(line.strip()):

				if char == '1':
					self.start_position = col * BLOCK_SIZE, row * BLOCK_SIZE
					char = ' '
				elif char == 'G':
					self.enemies.append(Goomba((col * BLOCK_SIZE, row * BLOCK_SIZE)))
					char = ' '

				tile = Wall(pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE,
											 BLOCK_SIZE, BLOCK_SIZE), char)
				tile_row.append(tile)
				if tile.color != SKY:
					self.walls.append(tile)

			self.grid.append(tile_row)
			row += 1
		self.height, self.width = len(self.grid) * BLOCK_SIZE, len(self.grid[0]) * BLOCK_SIZE

	def nearby_walls(self, rect):
		x1, x2 = rect.x / BLOCK_SIZE, (rect.x + rect.width) / BLOCK_SIZE + 1
		y1, y2 = rect.y / BLOCK_SIZE, (rect.y + rect.height) / BLOCK_SIZE + 1 
		return [tile for row in self.grid[y1 : y2] for tile in row[x1 : x2] if tile.color != SKY]

