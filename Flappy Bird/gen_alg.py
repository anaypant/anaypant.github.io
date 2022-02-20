from hashlib import new
import ai
import random
import pygame
import numpy as np
import matplotlib.pyplot as plt

#Parameters

#GENETIC ALGORITHM
NUM_POP = 100
NUM_ELITES = 10
NUM_MUTATIONS = 10
NUM_GENERATIONS = 200
BIRD_SCORE_INCREMENT = 0.001
BIRD_PASS_SCORE = 10
JUMP_CONFIDENCE_THRESH = 0.8
MUTATE_RATE = 0.2

#PYGAME SETTINGS
PYGAME_ENABLE = True
PYGAME_LOOK_AFTER_GEN = 50
PYGAME_BG = (113,197,207)
PYGAME_PIPE_COLOR = (113,191,46)
PYGAME_BIRD_COLOR = (212,172,87)
PYGAME_GROUND_COLOR = (101,78,86)
PYGAME_FPS = 30

# PIPES + CANVAS + GROUND
GAME_WIDTH = 600
GAME_HEIGHT = 600

PIPE_WIDTH = 30 
PIPE_GAP = 100
PIPE_DIST_BETWEEN_EACH_OTHER = 150
PIPE_SPEED = -5
GROUND_HEIGHT = 570

# BIRD
BIRD_X = 40
BIRD_Y = 300
BIRD_WIDTH = 15
GRAVITY = 1
LIFT = -12


#Plot Settings
PLOT_ENABLED = True
pltX = []
pltY = []
PLOT_COLOR = 'red'
# Check for Pygame


#Initialize Variables
birds = []
pipe = []
bird_ai = []

for i in range(NUM_POP):
    bird_ai.append(ai.nn())
    birds.append([BIRD_X, BIRD_Y])
    pipe.append([])
    #Iterate over each of 3 pipes for the pipe list
    for j in range(4):
        top_pipe_height = random.randint((GAME_WIDTH/2) - (PIPE_GAP//2), (GAME_WIDTH/2) + (PIPE_GAP//2))
        pipe[i].append([[PIPE_DIST_BETWEEN_EACH_OTHER * j + 150, 0],[PIPE_DIST_BETWEEN_EACH_OTHER * j + 150, top_pipe_height]])

for current_gen in range(1, NUM_GENERATIONS):
    # Run Through All Birds
    if PYGAME_ENABLE and current_gen == PYGAME_LOOK_AFTER_GEN:
        pygame.init()
        screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        clock = pygame.time.Clock()

    for i in range(len(birds)):
        while not bird_ai[i].dead:
            #Check to see if bird is jumping or not
            if bird_ai[i].velocity >= 2:
                bird_ai[i].is_jumping = False

            # Generate the inputs for the birds
            bird_x1 = (pipe[i][0][0][0] + PIPE_WIDTH/2) - birds[i][0]
            bird_y1 = pipe[i][0][1][1] - PIPE_GAP/2 - birds[i][1]
            bird_v = bird_ai[i].velocity
            
            #Forward Propagate the Bird
            bird_ai[i].forward([bird_x1, bird_y1, bird_v])
            if bird_ai[i].outputs[0] >= JUMP_CONFIDENCE_THRESH and bird_ai[i].is_jumping == False:
                bird_ai[i].is_jumping = True
                bird_ai[i].velocity += LIFT
            
            bird_ai[i].velocity += GRAVITY
            birds[i][1] += bird_ai[i].velocity

            for q in range(len(pipe[i])):
                pipe[i][q][0][0] += PIPE_SPEED
                pipe[i][q][1][0] += PIPE_SPEED
            
            if pipe[i][0][0][0] <= 0:
                del[pipe[i][0]]
                bird_ai[i].score += BIRD_PASS_SCORE
            
                top_pipe_height = random.randint((GAME_WIDTH/2) - (PIPE_GAP//2), (GAME_WIDTH/2) + (PIPE_GAP//2))
                pipe[i].append([[PIPE_DIST_BETWEEN_EACH_OTHER * 3 + 150, 0],[PIPE_DIST_BETWEEN_EACH_OTHER * 3 + 150, top_pipe_height + PIPE_GAP]])

            for specific_pipe in pipe[i]:
                if specific_pipe[0][0] <= birds[i][0] + BIRD_WIDTH <= specific_pipe[0][0] + PIPE_GAP:
                    if specific_pipe[0][1] <= birds[i][1] - BIRD_WIDTH <= specific_pipe[1][1] - PIPE_GAP:
                        # Bird Is Dead
                        bird_ai[i].dead = True
                        
                    elif specific_pipe[1][1] <= birds[i][1] + BIRD_WIDTH <= GAME_HEIGHT:
                        # Bird Is Dead
                        bird_ai[i].dead = True
                        
            

            if birds[i][1] >= GROUND_HEIGHT or birds[i][1] - BIRD_WIDTH <= 0:
                bird_ai[i].dead = True
            
            bird_ai[i].score += BIRD_SCORE_INCREMENT
            if PYGAME_ENABLE and current_gen >= PYGAME_LOOK_AFTER_GEN:
                screen.fill(PYGAME_BG)
                #Draw Pipes:
                for z in range(len(pipe[i])):
                    pygame.draw.rect(screen, PYGAME_PIPE_COLOR, [pipe[i][z][0][0], pipe[i][z][0][1], PIPE_WIDTH, pipe[i][z][1][1] - PIPE_GAP])
                    pygame.draw.rect(screen, PYGAME_PIPE_COLOR, [pipe[i][z][1][0], pipe[i][z][1][1], PIPE_WIDTH, GAME_HEIGHT - pipe[i][z][1][1]])

                #Draw Bird
                pygame.draw.circle(screen, PYGAME_BIRD_COLOR, [birds[i][0], birds[i][1]], BIRD_WIDTH)

                #Draw Ground
                pygame.draw.rect(screen, PYGAME_GROUND_COLOR, [0, GROUND_HEIGHT, GAME_WIDTH, GAME_HEIGHT - GROUND_HEIGHT])

                #Write Caption
                pygame.display.set_caption("Gen " + str(current_gen) + "    Bird " + str(i) + "     Score: " + str(bird_ai[i].score) + "    Outputs: " + str(bird_ai[i].outputs))

                #Clock FPS
                clock.tick(PYGAME_FPS)

                #Update
                pygame.display.update()

    # Find the Best Birds
    bird_scores = []
    for i in range(NUM_POP):
        bird_scores.append(bird_ai[i].score)
    if PLOT_ENABLED:
        pltX.append(current_gen)
        pltY.append(np.mean(bird_scores))
    elite_birds = []
    for i in range(NUM_ELITES):
        best_bird = bird_scores.index(max(bird_scores))
        if i == 0:
            print("Highest score for gen " + str(current_gen) + ": " + str(bird_scores[best_bird]))
        elite_birds.append(bird_ai[best_bird])
        del[bird_scores[best_bird]]
        del[bird_ai[best_bird]]
    
    # Crossover Elite Birds
    elite_bird_weights = []
    for i in range(NUM_ELITES):
        elite_bird_weights.append([])
        for j in range(len(elite_birds[i].weights)):
            elite_bird_weights[i].append(np.ndarray.tolist(elite_birds[i].weights[j]))
    
    birds.clear()
    pipe.clear()
    bird_ai.clear()
    for i in range(NUM_POP - NUM_ELITES - NUM_MUTATIONS):
        elite_parent_choices = []
        for q in range(NUM_ELITES):
            elite_parent_choices.append(q)
        first_parent = elite_parent_choices[random.randint(0, len(elite_parent_choices)-1)]
        del[elite_parent_choices[first_parent]]
        second_parent = elite_parent_choices[random.randint(0, len(elite_parent_choices)-1)]
        bird_ai.append(ai.nn(weights=ai.crossover_weights(elite_bird_weights[first_parent], elite_bird_weights[second_parent])))

    # Mutate Some Birds
    for i in range(NUM_MUTATIONS):
        elite_parent_choices = []
        for q in range(NUM_ELITES):
            elite_parent_choices.append(q)

        first_parent = elite_parent_choices[random.randint(0, len(elite_parent_choices)-1)]
        del[elite_parent_choices[first_parent]]
        second_parent = elite_parent_choices[random.randint(0, len(elite_parent_choices)-1)]
        new_weights = ai.crossover_weights(elite_bird_weights[first_parent], elite_bird_weights[second_parent], mutation=True, mutate_rate=MUTATE_RATE)
        
        bird_ai.append(ai.nn(weights=new_weights))
        
    for i in range(NUM_ELITES):
        bird_ai.append(elite_birds[i])

    for i in range(NUM_POP):    
        birds.append([BIRD_X, BIRD_Y])
        pipe.append([])
        #Iterate over each of 3 pipes for the pipe list
        for j in range(4):
            top_pipe_height = random.randint((GAME_WIDTH/2) - (PIPE_GAP//2), (GAME_WIDTH/2) + (PIPE_GAP//2))
            pipe[i].append([[PIPE_DIST_BETWEEN_EACH_OTHER * j + 150, 0],[150 * j + 150, top_pipe_height]])


        
    
    # Rinse + Repeat!
if PLOT_ENABLED:
    plt.plot(pltX, pltY, color=PLOT_COLOR)
    plt.show()