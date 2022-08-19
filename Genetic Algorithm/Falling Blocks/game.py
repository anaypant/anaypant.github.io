import objects
from settings import *
import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
clock = pygame.time.Clock()
game_over = False
addCounter = 0
#Initialize Players and EnemList
EnemList = []
player = objects.Player(gui=screen)

def checkCollision(enemCoords, playerCoords):
    largerBoxCoords = [enemCoords[0] - (PLAYER_WIDTH/2), enemCoords[1] - (PLAYER_WIDTH / 2)]
    largerBoxWidth = PLAYER_WIDTH * 2
    p1 = playerCoords[0] + (PLAYER_WIDTH/2)
    p2 = playerCoords[1] + (PLAYER_WIDTH / 2)
    if(p1 > largerBoxCoords[0] and p1 < largerBoxCoords[0] + largerBoxWidth):
        if(p2 > largerBoxCoords[1] and p2 < largerBoxCoords[1] + largerBoxWidth):
            return True
    
    return False

for i in range(NUM_STARTING_ENEMIES):
    randomX = random.randint(0, GAME_WIDTH / PLAYER_WIDTH) * PLAYER_WIDTH
    EnemList.append(objects.Enemy(randomX, gui=screen))

while not game_over:
    if(addCounter == ADD_THRESH):
        addCounter = 0
        randomX = random.randint(0, GAME_WIDTH / PLAYER_WIDTH) * PLAYER_WIDTH
        EnemList.append(objects.Enemy(randomX, gui=screen))

    screen.fill(BG_COLOR)
    clock.tick(FPS)
    player.update()
    player.draw()
    for enemy in EnemList:
        enemy.update()
        enemy.draw()
        if(checkCollision(enemy.getCoords(), player.getCoords())):
            game_over = True
        if(enemy.y > 600):
            del[EnemList[EnemList.index(enemy)]]
            player.score += 1
            print("New Score: " + str(player.score))
            continue
    pygame.display.set_caption(GAME_CAPTION)
    pygame.display.update()
    addCounter += 1

print("Final Score: " + str(player.score))