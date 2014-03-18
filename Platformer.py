#!/usr/bin/python

import pygame
from pygame.locals import *
from player import Player
from world import *

def main():
	# Initialize
	pygame.init()

	grid, walls = load_map('map.db')
	map_width, map_height = len(grid[0]) * BLOCK_SIZE, len(grid) * BLOCK_SIZE

	# Number of screen_rows and cols visible on the screen at any given point
	screen_cols, screen_rows = 30, 20
	screen_width, screen_height = screen_cols * BLOCK_SIZE, screen_rows * BLOCK_SIZE
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption('Zoom Man 1.0')

	player = Player()
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
				x, y = int(pos[0] + screen_x) / BLOCK_SIZE, int(pos[1] + screen_y) / BLOCK_SIZE
				tile = grid[y][x]
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

		# Draw player
		pygame.draw.rect(screen, player.color, player.rect().move(-screen_x, -screen_y), 0)

		# Write FPS
		text = font.render('FPS: ' + str(1000 / elapsed_time), True, (255, 255, 255), SKY)
		screen.blit(text, text.get_rect())

		pygame.display.flip()

if __name__ == '__main__':
	main()

