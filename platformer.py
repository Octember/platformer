#!/usr/bin/python

import pygame, sys, argparse
from pygame.locals import *
from sprites import Player, Goomba
from world import Map
from globals import *
from inventory import *

VERSION = "v0.1-alpha"
# EDIT HERE TO FIT YOUR NEEDS #
screen_width = 1000
screen_height = 500
DEBUG = 1

# Load the graphics
# BLOCKS #
BLOCKGRAPHICS = { LAND : pygame.image.load(LAND),
            SKY : pygame.image.load(SKY),
            SHRINK : pygame.image.load(SHRINK),
            GROW : pygame.image.load(GROW),
            LEDGE: pygame.image.load(LEDGE) }

# SPRITES #
SPRITEGRAPHICS = { 'Goomba' : pygame.image.load(GOOMBA),
            'Player' : pygame.image.load(PLAYER),
            'Bullet' : pygame.image.load(BULLET) }

# OBJECTS #
OBJIMG = { '0' : pygame.image.load(BULLET),
            '100' : pygame.image.load(LAND),
            '101' : pygame.image.load(SHRINK) }

# Inventory slot corrdinates #
SLOTCORD = []
invframe = pygame.Rect(200, 200, 330, 400)
invframe.center = screen_width/2, screen_height/2
innerframe = pygame.Rect(200, 200, 310, 160)
innerframe.bottomleft = invframe.left+10, invframe.bottom-10
left = innerframe.left+10
top = innerframe.top+10
objectframe = pygame.Rect(0, 0, 20, 20)
for raw in range(5):
                for slot in range(10):
                    SLOTCORD.append([left, top])
                    left += 30
                left = innerframe.left+10
                top += 30
def argparser():
    parser = argparse.ArgumentParser(description="Platformer - A simple RPG", epilog="Written by Data5tream and Octember", version="v0.1-beta")
    parser.add_argument("-m", "--map", help="Use to select map file (Use map or map2) ", action="store")
    args = parser.parse_args()
    global selectedmap
    if args.map == 'map':
        selectedmap = 'map.db'
    elif args.map == 'map2':
        selectedmap = 'map2.db'
    else: # Default map
        selectedmap = 'map2.db'

def main():
    # Initialize
    pygame.init()

    map = Map(selectedmap)
    player = Player(map.start_position)
    particles = pygame.sprite.Group([])
    goombas = pygame.sprite.Group(map.enemies)
    all_sprites = pygame.sprite.Group(map.enemies + [player])

    screen_cols, screen_rows = screen_width / BLOCK_SIZE, screen_height / BLOCK_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Platformer '+VERSION)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    invopen = 0 # True if the inventory is open, false if not.

    # Event loop
    right_down, left_down = False, False

    while 1:
        for event in pygame.event.get():
            if invopen == 0: # If inventory isn't opened do this:
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE: # Quit the game
                    return
                if event.type == KEYDOWN: # Handle pushed keys
                    if event.key in (K_LEFT, K_a):
                        left_down = True
                        player.move_left()
                    if event.key in (K_RIGHT, K_d):
                        right_down = True
                        player.move_right()
                    if event.key in (K_SPACE, K_w):
                        player.jump()
                    if event.key == K_i:
                        invopen = 1
                if event.type == KEYUP: # Handle released keys
                    if event.key in (K_LEFT, K_a):
                        player.move_right() if right_down else player.stop_x()
                        left_down = False
                    elif event.key in (K_RIGHT, K_d):
                        player.move_left() if left_down else player.stop_x()
                        right_down = False
                if event.type == MOUSEBUTTONDOWN: # Handle mouse clicks
                    pos = pygame.mouse.get_pos()
                    bullet = player.shoot((pos[0] + screen_x, pos[1] + screen_y))
                    particles.add(bullet)
                    all_sprites.add(bullet)
            elif invopen== 1: # If inventory is open do this:
                if event.type == QUIT:
                    return
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_i:
                        invopen = 0
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[0] in range(invframe.right-30, invframe.right) and pos[1] in range(invframe.top, invframe.top+30):
                        invopen = 0
                    for slot in range(50):
                        if pos[0] in range(SLOTCORD[slot][0], SLOTCORD[slot][0]+20) and pos[1] in range(SLOTCORD[slot][1], SLOTCORD[slot][1]+20):
                            #Drag the item
                            aps = 0
        '''
        TODO: Add an inventory so we don't have to disable this entirely.
        Add or remove land blocks from the selected square

        pos = pygame.mouse.get_pos()
        x, y = int(pos[0] + screen_x) / BLOCK_SIZE, int(pos[1] + screen_y) / BLOCK_SIZE
         tile = map.grid[y][x]
        if event.button == 1 and tile.color == LAND:
            map.walls.remove(tile.rect)
            tile.color = SKY
        elif event.button == 3 and tile.color == SKY:
            map.walls.append(tile)
            tile.color = LAND
        '''
        elapsed_time = clock.tick()

        # If player's healty drops beyond 0, end the game
        if player.health <= 0:
            # Player is death
            pygame.quit()
            print "[-] You have died!"
            sys.exit()

        # If all enemies were killed, quit game and display win message
        if len(goombas) == 0:
            # Player has won
            pygame.quit()
            print "[+] You have won!"
            sys.exit()

        # Update all creatures. O(v*N), N: number of sprites, v: size of sprite
        for sprite in all_sprites:
            sprite.update(elapsed_time, map)

        # O(N^2)
        collided_enemies = pygame.sprite.spritecollide(player, goombas, True)
        for enemy in collided_enemies:
            player.damage(10)
            # Display damage and health message
            if DEBUG:
                print "[-] 10 Damage recieved from "+str(enemy)
                print "[*] Player has now "+str(player.health)+" life points"

        # O(N^2)
        shot_enemies = pygame.sprite.groupcollide(goombas, particles, True, True) # KILL EM ALL

        # Position screen
        screen_x, screen_y = max(player.rect.x - 250, 0), max(player.rect.y - 250, 0)
        screen_x = min(screen_x, map.width - screen_width)
        screen_y = min(screen_y, map.height - screen_height)

        # Draw the visible map
        grid_x, grid_y = int(screen_x) / BLOCK_SIZE, int(screen_y) / BLOCK_SIZE
        for row in map.grid[grid_y : grid_y + screen_rows + 1]:
            for square in row[grid_x : grid_x + screen_cols + 1]:
                # Select the correct block and blit it to the screen
                screen.blit(BLOCKGRAPHICS[square.type], square.rect.move(-screen_x, -screen_y))
        # Draw health bar
        pygame.draw.rect(screen, (250, 0, 0), pygame.Rect(screen_width - 100, 5, player.health, 20), 0)
        # Draw sprites (Creatures, bullets, etc)
        for sprites in all_sprites:
            screen.blit(SPRITEGRAPHICS[sprites.type], sprites.rect.move(-screen_x, -screen_y))
        # Draw the inventory if necessary
        if invopen:
            invframe = pygame.Rect(200, 200, 330, 400)
            invframe.center = screen_width/2, screen_height/2
            innerframe = pygame.Rect(200, 200, 310, 160)
            innerframe.bottomleft = invframe.left+10, invframe.bottom-10
            left = innerframe.left+10
            top = innerframe.top+10
            objectframe = pygame.Rect(0, 0, 20, 20)
            pygame.draw.rect(screen, (44, 44, 44), invframe)
            pygame.draw.rect(screen, (88, 88, 88), innerframe)
            objectframe = pygame.Rect(0, 0, 20, 20)
            for raw in range(5):
                for slot in range(10):

                    objectframe.topleft = left, top
                    pygame.draw.rect(screen, (100, 100, 100), objectframe)
                    # object[1] is the itemID, OBJIMG is a dictonary of loaded images
                    object = inventory.content[slot+(10*(raw-5))]
                    screen.blit(OBJIMG[str(object[0])], objectframe)
                    left += 30
                left = innerframe.left+10
                top += 30
        # Draw FPS if necessary
        if DEBUG:
            text = font.render('FPS: ' + str(1000 / elapsed_time), True, (0, 0, 0), (250, 250, 250))
            screen.blit(text, text.get_rect())

        # Update the screen
        pygame.display.update()

if __name__ == '__main__':
    argparser()
    main()
