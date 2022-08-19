from settings import *
import pygame
import numpy as np
import objects
import ai
import random


players = []
enemies = []
blockAI = []

def newEnemy():
    randomX = random.randint(0, GAME_WIDTH / PLAYER_WIDTH) * PLAYER_WIDTH
    return objects.Enemy(randomX)

def checkCollision(enemCoords, playerCoords):
    largerBoxCoords = [enemCoords[0] - (PLAYER_WIDTH/2), enemCoords[1] - (PLAYER_WIDTH / 2)]
    largerBoxWidth = PLAYER_WIDTH * 2
    p1 = playerCoords[0] + (PLAYER_WIDTH/2)
    p2 = playerCoords[1] + (PLAYER_WIDTH / 2)
    if(p1 > largerBoxCoords[0] and p1 < largerBoxCoords[0] + largerBoxWidth):
        if(p2 > largerBoxCoords[1] and p2 < largerBoxCoords[1] + largerBoxWidth):
            return True
    
    return False

for i in range(NUM_POP):
    players.append(objects.Player())
    enemies.append([])
    enemies[i].append(newEnemy())
    blockAI.append(ai.blockNN())


for curGen in range(1, NUM_GENERATIONS + 1):
    if PYGAME_ENABLED and PYGAME_LOOK_AFTER_GEN == curGen:
        pygame.init()
        screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        clock = pygame.time.Clock()
    if PYGAME_ENABLED and PYGAME_LOOK_AFTER_GEN <= curGen:
        for z in range(NUM_POP):
            players[z].setGUI(screen)
            enemies[z][0].setGUI(screen)
    for i in range(NUM_POP):
        enemyAddCounter = 0
        while not blockAI[i].dead:
            aiInps = ai.genInputs(players[i].getCoords(), enemies[i][0].getCoords())
            blockAI[i].forward(aiInps)
            
            if(blockAI[i].key == 1):
                players[i].moveLeft()
            elif(blockAI[i].key == 2):
                players[i].moveRight()
            
            players[i].checkBounds()
            for enemy in enemies[i]:
                enemy.update()
                if(checkCollision(enemy.getCoords(), players[i].getCoords())):
                    blockAI[i].dead = True
                if(enemy.y > 600):
                    del[enemies[i][enemies[i].index(enemy)]]
                    blockAI[i].score += SCORE_INC
                    continue

            if(enemyAddCounter == 5):
                enemyAddCounter = 0
                enemies[i].append(newEnemy())
                if PYGAME_ENABLED and PYGAME_LOOK_AFTER_GEN <= curGen:
                    enemies[i][-1].setGUI(screen)
            
            if PYGAME_ENABLED and PYGAME_LOOK_AFTER_GEN <= curGen:
                    screen.fill(BG_COLOR)
                    clock.tick(FPS)
                    players[i].draw()
                    for enemy in enemies[i]:
                        enemy.draw()
                    pygame.display.set_caption("GEN: " + str(curGen) + "    Player: " + str(i) + "  Score: " + str(blockAI[i].score) + "    Outputs: " + str(blockAI[i].outputs))
                    pygame.display.update()

            enemyAddCounter += 1
            blockAI[i].score += STATIC_INC

    block_scores = []
    for i in range(NUM_POP):
        block_scores.append(blockAI[i].score)
        elite_blocks = []
    for i in range(NUM_ELITES):
            best_block = block_scores.index(max(block_scores))
            if i == 0:
                print("Highest score for gen " + str(curGen) + ": " + str(block_scores[best_block]))
            elite_blocks.append(blockAI[best_block])
            del[block_scores[best_block]]
            del[blockAI[best_block]]
        
        # Crossover Elite blocks
    elite_block_weights = []
    for i in range(NUM_ELITES):
            elite_block_weights.append([])
            for j in range(len(elite_blocks[i].weights)):
                elite_block_weights[i].append(np.ndarray.tolist(elite_blocks[i].weights[j]))
        
    players.clear()
    enemies.clear()
    blockAI.clear()
    for i in range(NUM_POP - NUM_ELITES - NUM_MUTATIONS):
            elite_parent_choices = []
            for q in range(NUM_ELITES):
                elite_parent_choices.append(q)
            first_parent = elite_parent_choices[random.randint(0, len(elite_parent_choices)-1)]
            del[elite_parent_choices[first_parent]]
            second_parent = elite_parent_choices[random.randint(0, len(elite_parent_choices)-1)]
            blockAI.append(ai.blockNN(weights=ai.crossover_weights(elite_block_weights[first_parent], elite_block_weights[second_parent])))

        # Mutate Some blocks
    for i in range(NUM_MUTATIONS):
            elite_parent_choices = []
            for q in range(NUM_ELITES):
                elite_parent_choices.append(q)

            first_parent = elite_parent_choices[random.randint(0, len(elite_parent_choices)-1)]
            del[elite_parent_choices[first_parent]]
            second_parent = elite_parent_choices[random.randint(0, len(elite_parent_choices)-1)]
            new_weights = ai.crossover_weights(elite_block_weights[first_parent], elite_block_weights[second_parent], mutation=True, mutate_rate=MUTATE_RATE)
            
            blockAI.append(ai.blockNN(weights=new_weights))
            
    for i in range(NUM_ELITES):
            blockAI.append(elite_blocks[i])

    for i in range(NUM_POP):
        players.append(objects.Player())
        enemies.append([])
        enemies[i].append(newEnemy())
