import numpy as np
import random
import pygame
from settings import *
import objects
import ai

players = []
enemies = []
shipAI = []
screen = 0
backgroundImage = 0

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


for i in range(NUM_POP):
    players.append(objects.PlayerShip())
    enemies.append([objects.Enemy(random.randint(0, NUM_SPAWN_POINTS) * ALIEN_W)])
    shipAI.append(ai.ShipAI())
for curGen in range(1, NUM_GENERATIONS + 1):
    if(PYGAME_ENABLED and curGen == PYGAME_LOOK_AFTER_GEN):
        pygame.init()
        screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        backgroundImage = pygame.transform.scale(pygame.image.load("images/bg.png"), (GAME_WIDTH, GAME_HEIGHT))
        clock = pygame.time.Clock()
    if(PYGAME_ENABLED and curGen >= PYGAME_LOOK_AFTER_GEN):
        for i in range(NUM_POP):
            players[i].setGUI(screen)
            enemies[i][0].setGUI(screen)
    for i in range(NUM_POP):
        alienTick = 0
        while shipAI[i].dead == False:
            #Gen Inputs
            alienTick += 1
            aiInps = ai.genInputs(players[i], enemies[i])
            #Get Outputs
            shipAI[i].forward(aiInps)
            #Conv. To Game Moves
            if(shipAI[i].outputs[0] >= MOVE_THRESH):#w
                players[i].y -= PLAYER_SPEED
            if(shipAI[i].outputs[1] >= MOVE_THRESH):#a
                players[i].x -= PLAYER_SPEED
            if(shipAI[i].outputs[2] >= MOVE_THRESH):#s
                players[i].y += PLAYER_SPEED
            if(shipAI[i].outputs[3] >= MOVE_THRESH):#d
                players[i].x += PLAYER_SPEED
            if(shipAI[i].outputs[4] >= MOVE_THRESH):# FIRE
                players[i].fire()
            #Update Player and Check Death
            players[i].update()
            for enemy in enemies[i]:
                enemy.update()

            if alienTick >= ALIEN_SPAWN_DELAY:
                    alienTick = 0
                    enemies[i].append(objects.Enemy(random.randint(0, NUM_SPAWN_POINTS) * ALIEN_W))
                    if(PYGAME_ENABLED and curGen >= PYGAME_LOOK_AFTER_GEN):
                        enemies[i][-1].setGUI(screen)

            breakLoop = False
            for z in range(len(enemies[i])):
                tempAlien = enemies[i][z]
                for q in range(len(players[i].bulletList)):
                    tempBullet = players[i].bulletList[q]
                    breakLoop = False
                    if(checkCollision([tempAlien.x, tempAlien.y, tempAlien.w, tempAlien.h], [tempBullet.x, tempBullet.y, tempBullet.w, tempBullet.h])):
                        del[players[i].bulletList[q]]
                        del[enemies[i][z]]
                        shipAI[i].score += SCORE_INC
                        breakLoop = True
                    if(breakLoop):
                        break
                if(breakLoop):
                    break

            breakLoop = False
            for z in range(len(enemies[i])):
                tempAlien1 = enemies[i][z]
                if(tempAlien1.y >= GAME_HEIGHT - tempAlien1.h):
                    shipAI[i].dead = True
                    breakLoop = True
                if(checkCollision([tempAlien1.x, tempAlien1.y, tempAlien1.w, tempAlien1.h], [players[i].x, players[i].y, players[i].w, players[i].h])):
                    shipAI[i].dead = True
                    breakLoop = True
                    if(breakLoop):
                        break
                if(breakLoop):
                    break
            shipAI[i].score += STATIC_INC
            if PYGAME_ENABLED and curGen >= PYGAME_LOOK_AFTER_GEN:
                screen.blit(backgroundImage, (0, 0))
                players[i].draw()
                for enemy in enemies[i]:
                    enemy.draw()
                clock.tick(FPS)
                pygame.display.set_caption("GEN: " + str(curGen) + "    Ship: " + str(i) + "    Outputs: " + str(shipAI[i].outputs))
                pygame.display.update()
    
    ship_scores = []
    for i in range(NUM_POP):
        ship_scores.append(shipAI[i].score)
        elite_ships = []
    for i in range(NUM_ELITES):
            best_ship = ship_scores.index(max(ship_scores))
            if i == 0:
                if curGen % 50 == 0:
                    print("Highest score for gen " + str(curGen) + ": " + str(ship_scores[best_ship]))
            elite_ships.append(shipAI[best_ship])
            del[ship_scores[best_ship]]
            del[shipAI[best_ship]]
        
        # Crossover Elite ships
    elite_ship_weights = []
    for i in range(NUM_ELITES):
            elite_ship_weights.append([])
            for j in range(len(elite_ships[i].weights)):
                elite_ship_weights[i].append(np.ndarray.tolist(elite_ships[i].weights[j]))
        
    players.clear()
    enemies.clear()
    shipAI.clear()
    for i in range(NUM_POP - NUM_ELITES - NUM_MUTATIONS):
            elite_parent_choices = []
            for q in range(NUM_ELITES):
                elite_parent_choices.append(q)
            first_parent = elite_parent_choices[random.randint(0, len(elite_parent_choices)-1)]
            del[elite_parent_choices[first_parent]]
            second_parent = elite_parent_choices[random.randint(0, len(elite_parent_choices)-1)]
            shipAI.append(ai.ShipAI(weights=ai.crossover_weights(elite_ship_weights[first_parent], elite_ship_weights[second_parent])))

        # Mutate Some ships
    for i in range(NUM_MUTATIONS):
            elite_parent_choices = []
            for q in range(NUM_ELITES):
                elite_parent_choices.append(q)

            first_parent = elite_parent_choices[random.randint(0, len(elite_parent_choices)-1)]
            del[elite_parent_choices[first_parent]]
            second_parent = elite_parent_choices[random.randint(0, len(elite_parent_choices)-1)]
            new_weights = ai.crossover_weights(elite_ship_weights[first_parent], elite_ship_weights[second_parent], mutation=True, mutate_rate=MUTATE_RATE)
            
            shipAI.append(ai.ShipAI(weights=new_weights))
            
    for i in range(NUM_ELITES):
            elite_ships[i].resetScore()
            shipAI.append(elite_ships[i])
    for i in range(NUM_POP):
        players.append(objects.PlayerShip())
        enemies.append([objects.Enemy(random.randint(0, NUM_SPAWN_POINTS) * ALIEN_W)])