#!/usr/bin/python

import pygame, sys, argparse
from pygame.locals import *
from sprites import Player, Goomba
from world import Map
from globals import *
from inventory import *

version = "v0.1-alpha"
# EDIT HERE TO FIT YOUR NEEDS #
screen_width = 1000
screen_height = 500
DEBUG = 1

# Load the graphics
# BLOCKS #
landblock = pygame.image.load(LAND)
skyblock = pygame.image.load(SKY)
shrinkblock = pygame.image.load(SHRINK)
growblock = pygame.image.load(GROW)
ledgeblock = pygame.image.load(LEDGE)
# SPRITES #
goombamat = pygame.image.load(GOOMBA)
playermat = pygame.image.load(PLAYER)
bulletmat = pygame.image.load(BULLET)

def argparser():
    parser = argparse.ArgumentParser(description="Platformer - A simple RPC", epilog="Written by Data5tream and Octember", version="v0.1-beta")
    parser.add_argument("-m", "--map", help="Use to select map file (Use map or map2) ", action="store")
    args = parser.parse_args()
    global selectedmap
    if args.map == 'map':
        selectedmap = 'map.db'
    elif args.map == 'map2':
        selectedmap = 'map2.db'
    else:
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
    pygame.display.set_caption('Platformer '+version)

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
                if square.type == LAND:
                    screen.blit(landblock, square.rect.move(-screen_x, -screen_y))
                elif square.type == SKY:
                    screen.blit(skyblock, square.rect.move(-screen_x, -screen_y))
                elif square.type == SHRINK:
                    screen.blit(shrinkblock, square.rect.move(-screen_x, -screen_y))
                elif square.type == GROW:
                    screen.blit(growblock, square.rect.move(-screen_x, -screen_y))
                elif square.type == LEDGE:
                    screen.blit(ledgeblock, square.rect.move(-screen_x, -screen_y))
        # Draw health bar
        pygame.draw.rect(screen, (250, 0, 0), pygame.Rect(screen_width - 100, 5, player.health, 20), 0)
        # Draw sprites (Creatures, bullets, etc)
        for sprites in all_sprites:
            if sprites.type == "Goomba":
                screen.blit(goombamat, sprites.rect.move(-screen_x, -screen_y))
            elif sprites.type == "Player":
                screen.blit(playermat, sprites.rect.move(-screen_x, -screen_y))
            elif sprites.type == "Bullet":
                screen.blit(bulletmat, sprites.rect.move(-screen_x, -screen_y))
        # Draw the inventory if necessary
        if invopen:
            invframe = pygame.Rect(200, 200, 400, 400)
            invframe.center = screen_width/2, screen_height/2
            innerframe = pygame.Rect(200, 200, 380, 200)
            innerframe.bottomleft = invframe.left+10, invframe.bottom-10
            pygame.draw.rect(screen, (44, 44, 44), invframe)
            pygame.draw.rect(screen, (88, 88, 88), innerframe)
            objectframe = pygame.Rect(0, 0, 20, 20)
            left = innerframe.left+10
            top = innerframe.top+10
            for raw in range(4):
                for slot in range(12):
                    objectframe.topleft = left, top
                    pygame.draw.rect(screen, (100, 100, 100), objectframe)
                    # Put something here to catch the object in slot 'slot' and display
                    '''
                    object = inventory.content[slot+(12*(raw-1))]
                    '''
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
