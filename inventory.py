import pygame
from pygame.locals import *
from globals import *

class inventory:
    content = []
    for slot in range(30):
        content.append([slot,'itemID','stack'])
