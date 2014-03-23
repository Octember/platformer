import pygame
import math
from pygame.locals import *
from globals import *

class Creature(pygame.sprite.Sprite):

	def __init__(self, position, width, height, color):
		pygame.sprite.Sprite.__init__(self)
		self.x, self.y = position
		self.color = color
		self.y_velocity, self.x_velocity = 0, 0
		self.rect = pygame.Rect(position, (float(width), float(height)))

	def update_x(self, elapsed_time):
		self.x += self.x_velocity * elapsed_time
		self.rect.x = self.x

	def update_y(self, elapsed_time):
		self.y += self.y_velocity * elapsed_time
		self.rect.y = self.y

	def collide_x(self, wall):
		if wall.color == SHRINK:
			self.shrink()
		elif wall.color == GROW:
			self.grow()
		elif wall.color == LEDGE:
			return
		# Wall is normal ground
		collision = wall.rect
		if self.x_velocity < 0: # Moving left
			self.x = collision.right
		elif self.x_velocity > 0: # Moving right
			self.x = collision.left - self.rect.width
		self.rect.x = self.x

	def collide_y(self, wall):
		if wall.color == LEDGE:
			if self.y_velocity > 0 and self.rect.bottom - wall.rect.top <= LEDGE_HEIGHT:
				self.y = wall.rect.y - self.rect.height
				self.y_velocity = 0	
		else:
			if wall.color == SHRINK:
				self.shrink()
			elif wall.color == GROW:
				self.grow()
			collision = wall.rect
			if self.y_velocity > 0:
				self.y = collision.y - self.rect.height
				self.y_velocity = 0	
			elif self.y_velocity < 0: 
				# Moving up
				self.y = collision.bottom
				self.y_velocity = 0
		self.rect.y = self.y


class Bullet(Creature):
	MAX_SPEED = 0.5
	def __init__(self, position, velocity):
		Creature.__init__(self, position, 5, 2, (0, 0, 0))
		self.x_velocity, self.y_velocity = velocity
		self.time = 0

	def update_x(self, el):
		self.time += el
		if self.time > 5000:
			self.kill()
		Creature.update_x(self, el)

	def collide_x(self, wall):
		self.y_velocity, self.x_velocity = 0, 0

	def collide_y(self, wall):
		self.y_velocity, self.x_velocity = 0, 0


class Player(Creature):
	MAX_SPEED = 0.3

	def __init__(self, position):
		Creature.__init__(self, position, 15, 20, (77, 204, 77))
		self.health = 100

	def jump(self):
		self.y_velocity = -0.5

	def shrink(self):
		self.color = (0, 0, 0)
		self.rect.height, self.rect.width = (10, 5)

	def grow(self):
		self.color = (255, 255, 0)
		self.rect.height, self.rect.width = (100, 50)

	def update_y(self, elapsed_time):
		self.y_velocity += GRAVITY * elapsed_time
		Creature.update_y(self, elapsed_time)

	def move_left(self):
		self.x_velocity = -Player.MAX_SPEED

	def move_right(self):
		self.x_velocity = Player.MAX_SPEED

	def stop_x(self):
		self.x_velocity = 0

	def shoot(self, position):
		diff_x, diff_y = position[0] - self.rect.centerx, position[1] - self.rect.centery
		magnitude = math.sqrt(diff_x * diff_x + diff_y * diff_y)
		return Bullet(self.rect.center, (diff_x / magnitude, diff_y / magnitude))

	def damage(self, damage):
		self.health -= damage

	def alive(self):
		return self.health > 0


class Goomba(Creature):

	MAX_SPEED = 0.1

	def __init__(self, position):
		Creature.__init__(self, position, BLOCK_SIZE, BLOCK_SIZE, (76, 0, 150))
		self.move_left()

	def update_y(self, elapsed_time):
		self.y_velocity += GRAVITY * elapsed_time
		Creature.update_y(self, elapsed_time)

	def stop_x(self):
		self.x_velocity = -self.x_velocity

	def move_left(self):
		self.x_velocity = -Goomba.MAX_SPEED

	def move_right(self):
		self.x_velocity = Goomba.MAX_SPEED

	def collide_x(self, wall):
		Creature.collide_x(self, wall)
		self.x_velocity = -self.x_velocity