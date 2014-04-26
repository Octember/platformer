import pygame
from pygame.locals import *
from globals import *

itemID = 1
number = 1
class inventory:
    content = []
    for slot in range(30):
        content.append([slot,itemID, number])

'''
Item structure:
ITEM[(itemID), (itemname), (itemclass)]
'''