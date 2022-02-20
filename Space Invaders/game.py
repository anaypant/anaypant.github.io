import pygame
import objects
from settings import *
import random

pygame.init()
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
game_over = False
backgroundImage = pygame.transform.scale(pygame.image.load("images/bg.png"), (GAME_WIDTH, GAME_HEIGHT))
player = objects.PlayerShip(screen)
clock = pygame.time.Clock()
alienList = [objects.Enemy(random.randint(0, NUM_SPAWN_POINTS) * ALIEN_W, gui=screen)]
alienTick = 0
def checkCollision(enemCoords, playerCoords):
    enemW = enemCoords[2]
    enemH = enemCoords[3]
    playerW = playerCoords[2]
    playerH = playerCoords[3]
    largerBoxCoords = [enemCoords[0] - (enemW/2), enemCoords[1] - (enemH / 2)]
    largerBoxWidth = enemW * 2
    largerBoxHeight = enemH * 2
    p1 = playerCoords[0] + (playerW/2)
    p2 = playerCoords[1] + (playerH/ 2)
    if(p1 > largerBoxCoords[0] and p1 < largerBoxCoords[0] + largerBoxWidth):
        if(p2 > largerBoxCoords[1] and p2 < largerBoxCoords[1] + largerBoxWidth):
            return True
    
    return False

while not game_over:
    screen.fill((0,0,0)) #Just a black Background
    screen.blit(backgroundImage, (0,0))
    if alienTick >= ALIEN_SPAWN_DELAY:
        alienTick = 0
        alienList.append(objects.Enemy(random.randint(0, NUM_SPAWN_POINTS) * ALIEN_W, gui=screen))
    breakLoop = False
    for z in range(len(alienList)):
        tempAlien = alienList[z]
        for q in range(len(player.bulletList)):
            tempBullet = player.bulletList[q]
            breakLoop = False
            if(checkCollision([tempAlien.x, tempAlien.y, tempAlien.w, tempAlien.h], [tempBullet.x, tempBullet.y, tempBullet.w, tempBullet.h])):
                del[player.bulletList[q]]
                del[alienList[z]]
                breakLoop = True
            if(breakLoop):
                break
        if(breakLoop):
            break
    
    for alien in alienList:
        alien.update()
        alien.draw()

    player.update()
    player.draw()
    for z in range(len(alienList)):
        tempAlien1 = alienList[z]
        if(tempAlien1.y >= GAME_HEIGHT - tempAlien1.h):
            game_over = True
            breakLoop = True
        if(checkCollision([tempAlien1.x, tempAlien1.y, tempAlien1.w, tempAlien1.h], [player.x, player.y, player.w, player.h])):
            game_over = True
            breakLoop = True
            if(breakLoop):
                break
        if(breakLoop):
            break

    clock.tick(FPS)
    pygame.display.update()
    alienTick += 2