import pygame
from pygame.locals import *
from world import *

MAX_SPEED = 0.3

class Player:

	def __init__(self):
		self.x, self.y = 300, 5
		
		self.width = 10
		self.height = 20
		self.color = (77, 204, 77)
		self.y_velocity, self.x_velocity = 0, 0

	def position(self):
		return (int(self.x), int(self.y))

	def rect(self):
		return pygame.Rect(self.position(), (self.width, self.height))

	def jump(self):
		self.y_velocity = -0.5

	def collide_x(self, wall):
		if wall.color == DEATH:
			self.die()
		elif wall.color == LEDGE:
			return
		# Wall is normal ground
		collision = wall.rect
		if self.x_velocity < 0: # Moving left
			self.x = collision.right
		elif self.x_velocity > 0: # Moving right
			self.x = collision.left - self.width

	def collide_y(self, wall):
		if wall.color == LEDGE:
			if self.y_velocity > 0 and self.rect().bottom - wall.rect.top <= LEDGE_HEIGHT:
				self.y = wall.rect.y - self.height
				self.y_velocity = 0	
		else:
			if wall.color == DEATH:
				self.die()
			collision = wall.rect
			if self.y_velocity > 0:
				self.y = collision.y - self.height
				self.y_velocity = 0	
			elif self.y_velocity < 0: 
				# Moving up
				self.y = collision.bottom
				self.y_velocity = 0

	def die(self):
		self.color = (0, 0, 0)

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