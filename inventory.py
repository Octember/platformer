import pygame
from pygame.locals import *
from globals import *
from items import *

itemID = 1
number = 1
class inventory:
    content = []
    for slot in range(50):
        content.append([0,'none'])

    content[0] = ITEMS['101']
    content[1] = ITEMS['100']
    content[11] = ITEMS['100']