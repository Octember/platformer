#!/usr/bin/python

import pygame
from pygame.locals import *
from sprites import Player, Goomba
from world import Map
from globals import *

def main():
	# Initialize
	pygame.init()

	map = Map('map.db')
	player = Player(map.start_position)

	goombas = pygame.sprite.Group(map.enemies)
	all_sprites = pygame.sprite.Group(map.enemies + [player])

	# Number of screen_rows and cols visible on the screen at any given point
	
	screen_width, screen_height = 500, 500
	screen_cols, screen_rows = screen_width / BLOCK_SIZE, screen_height / BLOCK_SIZE
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption('Zoom Man 1.0')

	clock = pygame.time.Clock()
	font = pygame.font.SysFont(None, 30)

	# Event loop
	right_down, left_down = False, False

	while 1:
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				return
			if event.type == KEYDOWN:
				if event.key in (K_LEFT, K_a):
					left_down = True
					player.move_left()
				if event.key in (K_RIGHT, K_d):
					right_down = True
					player.move_right()
				if event.key in (K_SPACE, K_w):
					player.jump()
			if event.type == KEYUP:
				if event.key in (K_LEFT, K_a):
					player.move_right() if right_down else player.stop_x()
					left_down = False
				elif event.key in (K_RIGHT, K_d):
					player.move_left() if left_down else player.stop_x()
					right_down = False
			if event.type == MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				x, y = int(pos[0] + screen_x) / BLOCK_SIZE, int(pos[1] + screen_y) / BLOCK_SIZE
				tile = map.grid[y][x]
				if event.button == 1 and tile.color == LAND:
					map.walls.remove(tile.rect)
					tile.color = SKY
				elif event.button == 3 and tile.color == SKY:
					map.walls.append(tile)
					tile.color = LAND

		elapsed_time = clock.tick()

		# Update all creatures
		for creature in all_sprites:
			creature.update_x(elapsed_time)
			collisions = [wall for wall in map.nearby_walls(creature.rect)]
			for wall in collisions:
				if wall.collide(creature.rect):
					creature.collide_x(wall)

			creature.y_velocity += GRAVITY * elapsed_time
			creature.update_y(elapsed_time)

			collisions = [wall for wall in map.nearby_walls(creature.rect)]
			for wall in collisions:
				if wall.collide(creature.rect):
					creature.collide_y(wall)

		collided_enemies = pygame.sprite.spritecollide(player, goombas, False) 
		for enemy in collided_enemies:
			player.damage(10)

		# Position screen
		screen_x, screen_y = max(player.rect.x - 250, 0), max(player.rect.y - 250, 0)
		screen_x = min(screen_x, map.width - screen_width)
		screen_y = min(screen_y, map.height - screen_height)

		# Draw the visible map
		grid_x, grid_y = int(screen_x) / BLOCK_SIZE, int(screen_y) / BLOCK_SIZE
		for row in map.grid[grid_y : grid_y + screen_rows + 1]:
			for square in row[grid_x : grid_x + screen_cols + 1]:
				screen.fill(square.color, square.rect.move(-screen_x, -screen_y))

		# Draw health bar
		pygame.draw.rect(screen, (250, 0, 0), pygame.Rect(screen_width - 100, 5, player.health, 20), 0)
		# Draw enemies
		for creature in all_sprites:
			pygame.draw.rect(screen, creature.color, creature.rect.move(-screen_x, -screen_y), 0)

		# Draw FPS
		text = font.render('FPS: ' + str(1000 / elapsed_time), True, (0, 0, 0), SKY)
		screen.blit(text, text.get_rect())

		pygame.display.flip()

if __name__ == '__main__':
	main()
