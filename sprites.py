import pygame
from math import sqrt
from random import randint
from pygame.locals import *
from globals import *

'''
Base class for all sprites. Handles simple collision and updating position.

One weird nuance is that the pygame Rect can only store ints. So external
x and y coordinates are defined to handle smooth subpixel movement. But the
coordinates should be accessed from the rect field.
'''
class Sprite(pygame.sprite.Sprite):

    def __init__(self, position, dimensions, color):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = position
        self.color = color
        self.y_velocity, self.x_velocity = 0, 0
        self.rect = pygame.Rect(position, dimensions)

    '''
    Called once per frame. Clients can override to manage passing time
    '''
    def update(self, elapsed_time, map):
        self._update_x(elapsed_time)
        collisions = [wall for wall in map.nearby_walls(self.rect)]
        for wall in collisions:
            if wall.collide(self.rect):
                self._collide_x(wall)
                self.interact_with(wall)

        self._update_y(elapsed_time)

        collisions = [wall for wall in map.nearby_walls(self.rect)]
        for wall in collisions:
            if wall.collide(self.rect):
                self._collide_y(wall)
                self.interact_with(wall)
    '''
    Interaction with the given wall. Override to define special functionality
    '''
    def interact_with(self, wall):
        pass

    def _update_x(self, elapsed_time):
        self.x += self.x_velocity * elapsed_time
        self.rect.x = self.x

    def _update_y(self, elapsed_time):
        self.y += self.y_velocity * elapsed_time
        self.rect.y = self.y

    def _collide_x(self, wall):
        # Wall is normal ground
        if wall.type != LEDGE:
            collision = wall.rect
            if self.x_velocity < 0: # Moving left
                self.x = collision.right
            elif self.x_velocity > 0: # Moving right
                self.x = collision.left - self.rect.width
            self.rect.x = self.x

    def _collide_y(self, wall):
        if wall.type == LEDGE:
            if self.y_velocity > 0 and self.rect.bottom - wall.rect.top <= LEDGE_HEIGHT:
                self.y = wall.rect.y - self.rect.height
                self.y_velocity = 0
        else:
            collision = wall.rect
            if self.y_velocity > 0:
                self.y = collision.y - self.rect.height
                self.y_velocity = 0
            elif self.y_velocity < 0:
                # Moving up
                self.y = collision.bottom
                self.y_velocity = 0
        self.rect.y = self.y

'''
Simple bullet. Shoots in the given direction, until it hits a wall
'''
class Bullet(Sprite):
    MAX_SPEED = 0.5
    LIFESPAN = 5000
    DIMENSIONS = (5, 2)
    COLOR = (0, 0, 0)

    def __init__(self, position, velocity):
        Sprite.__init__(self, position, Bullet.DIMENSIONS, Bullet.COLOR)
        self.x_velocity, self.y_velocity = velocity
        self.time = 0

    def update(self, elapsed_time, map):
        self.time += elapsed_time
        if self.time > Bullet.LIFESPAN:
            self.kill()
        Sprite.update(self, elapsed_time, map)

    def interact_with(self, wall):
        self.y_velocity, self.x_velocity = 0, 0

class Creature(Sprite):

    def __init__(self, position, dimensions, color):
        Sprite.__init__(self, position, dimensions, color)
        self.jumping = False
        self.health = 100

    def damage(self, damage):
        self.health -= damage

    def update(self, elapsed_time, map):
        self.y_velocity += GRAVITY * elapsed_time
        Sprite.update(self, elapsed_time, map)

    def jump(self, speed):
        if not self.jumping:
            self.y_velocity = -speed
            self.jumping = True

    def _collide_y(self, wall):
        if self.y_velocity > 0:
            self.jumping = False
        Sprite._collide_y(self, wall)


'''
The player! Our hero. We love him so
'''
class Player(Creature):
    MAX_SPEED = 0.3
    COLOR = (77, 204, 77)
    DIMENSIONS = (15, 20)

    def __init__(self, position):
        Creature.__init__(self, position, Player.DIMENSIONS, Player.COLOR)
        self.health = 100

    def jump(self):
        Creature.jump(self, Player.MAX_SPEED)

    def shrink(self):
        self.color = (0, 0, 0)
        self.rect.height, self.rect.width = (10, 5)

    def grow(self):
        self.color = (255, 255, 0)
        self.rect.height, self.rect.width = (100, 50)

    def interact_with(self, wall):
        if wall.type == SHRINK:
            self.shrink()
        elif wall.type == GROW:
            self.grow()

    def move_left(self):
        self.x_velocity = -Player.MAX_SPEED

    def move_right(self):
        self.x_velocity = Player.MAX_SPEED

    def stop_x(self):
        self.x_velocity = 0

    def shoot(self, position):
        diff_x  = position[0] - self.rect.centerx
        diff_y = position[1] - self.rect.centery
        magnitude = sqrt(diff_x * diff_x + diff_y * diff_y)
        return Bullet(self.rect.center, (diff_x / magnitude, diff_y / magnitude))

    def alive(self):
        return self.health > 0

class Goomba(Creature):
    MAX_SPEED = 0.1
    DIMENSIONS = (BLOCK_SIZE, BLOCK_SIZE)
    COLOR = (76, 0, 150)

    def __init__(self, position):
        Sprite.__init__(self, position, Goomba.DIMENSIONS, Goomba.COLOR)
        self.move_left()
        self.time = randint(0, 3000)

    def update(self, elapsed_time, map):
        self.time -= elapsed_time
        if self.time <= 0:
            self.time = randint(0, 3000)
            Creature.jump(self, Goomba.MAX_SPEED)
        Creature.update(self, elapsed_time, map)
    def stop_x(self):
        self.x_velocity = -self.x_velocity

    def move_left(self):
        self.x_velocity = -Goomba.MAX_SPEED

    def move_right(self):
        self.x_velocity = Goomba.MAX_SPEED

    def interact_with(self, wall):
        if self.y_velocity != 0:
            self.x_velocity = -self.x_velocity