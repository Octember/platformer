import pygame
from pygame.locals import *
from globals import *
from items import *

itemID = 1
number = 1
class inventory:
    content = []
    for slot in range(30):
        content.append([0,'none'])

    content[0] = [1,'TEST-1']
    content[1] = [2,'TEST-2']