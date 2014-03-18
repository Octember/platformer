#!/usr/bin/python

import pygame
from pygame.locals import *

GRAVITY = 0.001
MAX_SPEED = 0.3
BLOCK_SIZE = 20
LAND = (186, 144, 28)
SKY = (50, 255, 255)
DEATH = (203, 0, 0)
LEDGE = (0, 120, 120)


class Character:

	def __init__(self):
		self.x, self.y = 300, 5
		self.y_velocity, self.x_velocity = 0, 0
		self.width = 10
		self.height = 20
		self.color = (77, 204, 77)

	def position(self):
		return (int(self.x), int(self.y))

	def rect(self):
		return pygame.Rect(self.position(), (self.width, self.height))

	def jump(self):
		self.y_velocity = -0.5

	def collide_x(self, wall):
		if wall.color == DEATH:
			self.die()
		if wall.color == LEDGE:
			return

		collision = wall.rect
		if self.x_velocity < 0: # Moving left
			self.x = collision.right
		elif self.x_velocity > 0: # Moving right
			self.x = collision.left - self.width

	def collide_y(self, wall):
		if wall.color == DEATH:
			self.die()

		collision = wall.rect
		if self.y_velocity > 0:
			self.y = collision.y - self.height
			self.y_velocity = 0	
		elif self.y_velocity < 0 and wall.color != LEDGE: 
			# Moving up
			self.y = collision.bottom
			self.y_velocity = 0

	def die(self):
		self.color = (0, 0, 0)
		print "die"

	def move_left(self):
		self.x_velocity = -MAX_SPEED

	def move_right(self):
		self.x_velocity = MAX_SPEED

	def stop_x(self):
		self.x_velocity = 0

	def update_x(self, elapsed_time):
		self.x += self.x_velocity * elapsed_time

	def update_y(self, elapsed_time):
		self.y += self.y_velocity * elapsed_time


class Wall:
	def __init__(self, rect, char):
		self.rect = rect
		self.color = get_color(char)

	def collide(self, other_rect):
		return self.rect.colliderect(other_rect)


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

def get_color(value):
	if value == ' ':
		return SKY
	elif value == '#':
		return LAND
	elif value == '$':
		return DEATH
	elif value == 'L':
		return LEDGE

def main():
	# Initialize
	pygame.init()

	grid, walls = load_map('map.db')
	map_width, map_height = len(grid[0]) * BLOCK_SIZE, len(grid) * BLOCK_SIZE

	# Number of screen_rows and cols visible on the screen at any given point
	screen_cols, screen_rows = 30, 20
	screen_width, screen_height = screen_cols*BLOCK_SIZE, screen_rows*BLOCK_SIZE
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption('Zoom Man 1.0')

	# Return the grid member at the given point 
	def getSquareAt(pos):
		x, y = int(pos[0] + screen_x) / BLOCK_SIZE, int(pos[1] + screen_y) / BLOCK_SIZE
		return grid[y][x]

	player = Character()
	clock = pygame.time.Clock()
	font = pygame.font.SysFont(None, 30)

	# Event loop
	right_down, left_down = False, False

	while 1:
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				return
			if event.type == KEYDOWN:
				if event.key == K_LEFT:
					left_down = True
					player.move_left()
				if event.key == K_RIGHT:
					right_down = True
					player.move_right()
				if event.key == K_SPACE:
					player.jump()
			if event.type == KEYUP:
				if event.key == K_LEFT:
					player.move_right() if right_down else player.stop_x()
					left_down = False
				elif event.key == K_RIGHT:
					player.move_left() if left_down else player.stop_x()
					right_down = False
			if event.type == MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				tile = getSquareAt(pos)
				if event.button == 1 and tile.color == LAND:
						walls.remove(tile.rect)
						tile.color = SKY
				elif event.button == 3 and tile.color == SKY:
					 	walls.append(tile)
					 	tile.color = LAND

		elapsed_time = clock.tick()
		# Update Player

		# Horizontal movement
		player.update_x(elapsed_time)

		collisions = [wall for wall in walls if wall.collide(player.rect())]
		for wall in collisions:
			player.collide_x(wall)

		# Vertical movement
		player.y_velocity += GRAVITY * elapsed_time
		player.update_y(elapsed_time)

		collisions = [wall for wall in walls if wall.collide(player.rect())]
		for wall in collisions:
			player.collide_y(wall)

		screen_x, screen_y = max(player.x - 250, 0), max(player.y - 250, 0)
		screen_x, screen_y = min(screen_x, map_width - screen_width), min(screen_y, map_height - screen_height)

		# Draw the visible map
		grid_x, grid_y = int(screen_x) / BLOCK_SIZE, int(screen_y) / BLOCK_SIZE
		for row in grid[grid_y : grid_y + screen_rows + 1]:
			for square in row[grid_x : grid_x + screen_cols + 1]:
				screen.fill(square.color, square.rect.move(-screen_x, -screen_y))

		# Draw grid. Slows everything way down, for testing speed
		# for i in range(screen_cols + 1):
		# 	for j in range(screen_rows):
		# 		rect = pygame.Rect(i * BLOCK_SIZE - screen_x % BLOCK_SIZE, j * BLOCK_SIZE, BLOCK_SIZE + 1, BLOCK_SIZE + 1)
		# 		pygame.draw.rect(screen, (0, 0, 0), rect, 1)

		# Draw player
		pygame.draw.rect(screen, player.color, player.rect().move(-screen_x, -screen_y), 0)

		# Write FPS
		text = font.render('FPS: ' + str(1000 / elapsed_time), True, (255, 255, 255), SKY)
		screen.blit(text, text.get_rect())

		pygame.display.flip()

if __name__ == '__main__':
	main()

