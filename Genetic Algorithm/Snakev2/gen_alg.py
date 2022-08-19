import objects
import ai
import settings
import pygame
import random
import numpy as np
import keyboard

snake = []
apple = []
s_ai = []
s_dir = []
screen = None
for i in range(settings.NUM_POP):
    snake.append([[settings.SNAKE_WIDTH * ((settings.COLUMNS + 1) / 2), settings.SNAKE_WIDTH * ((settings.ROWS + 1) / 2)]])
    apple.append([random.randint(1, settings.COLUMNS) * settings.SNAKE_WIDTH, random.randint(1, settings.ROWS) * settings.SNAKE_WIDTH])
    #if(settings.RUN_GEN_WITH_PYGAME and settings.PYGAME_LOOK_GEN <= 1):
        #snake[i].append([objects.Snake(gui=0)])
        #apple.append([objects.Apple(gui=0)])

    #else:
        #snake[i].append([objects.Snake()])
        #apple.append([objects.Apple()])
    s_ai.append(ai.snakeNN())
    s_dir.append([1, 0])

for curgen in range(1, settings.NUM_GENERATIONS + 1):
    if settings.RUN_GEN_WITH_PYGAME and settings.PYGAME_LOOK_GEN == curgen:
        pygame.init()
        screen = pygame.display.set_mode((settings.CANV_WIDTH, settings.CANV_HEIGHT))
        clock = pygame.time.Clock()
        #for qu in range(settings.NUM_POP):
        #    snake[qu].gui = screen
        #    apple[qu].gui = screen
    
    for i in range(settings.NUM_POP):
        while( not s_ai[i].dead):
            if keyboard.is_pressed(" "):
                s_ai[i].dead = True
            snake_inps = ai.genInputs(snake[i], apple[i], s_dir[i])
            s_ai[i].FF(snake_inps)

            if s_ai[i].key == 0:
                s_dir[i] = s_dir[i]
            elif s_ai[i].key == 1:
                s_dir[i] = ai.getLeftCoord(s_dir[i])
            elif s_ai[i].key == 2:
                s_dir[i] = ai.getRightCoord(s_dir[i])
           

            pre_move_dist = ai.calculateDistance(snake[i][-1], apple[i])
            snake_head = [snake[i][-1][0] + s_dir[i][0] * settings.SNAKE_WIDTH, snake[i][-1][1] + s_dir[i][1] * settings.SNAKE_WIDTH]
            snake[i].append(snake_head)
            if len(snake[i]) > s_ai[i].length:
                del[snake[i][0]]

            #TODO: add deaths, steps to snake, increment score, and everything after fitness test

            if snake[i][-1] == apple[i]:
                apple[i] = ([random.randint(1, settings.COLUMNS) * settings.SNAKE_WIDTH, random.randint(1, settings.ROWS) * settings.SNAKE_WIDTH])
                s_ai[i].score += settings.SCORE_INC
                s_ai[i].length += 1
                s_ai[i].steps += settings.STEP_INC_SCORE
            if not ((0 <= snake[i][-1][0] <= settings.CANV_WIDTH - settings.SNAKE_WIDTH) and ((0 <= snake[i][-1][1] <= settings.CANV_HEIGHT - settings.SNAKE_WIDTH))):
                s_ai[i].dead = True
            if (len(snake[i]) > 1):
                for z in range(len(snake[i]) - 1):
                    if snake[i][z] == snake[i][-1]:
                        s_ai[i].dead = True
            if (settings.STEPS_ENABLED) and (s_ai[i].steps <= 0):
                s_ai[i].dead = True
            s_ai[i].steps -= 1
            #s_ai[i].score += settings.STAT_INC
            post_move_dist = ai.calculateDistance(snake[i][-1], apple[i])
            if(post_move_dist < pre_move_dist):
                s_ai[i].score += settings.STAT_INC
            else:
                s_ai[i].score -= 3 * settings.STAT_INC



            if settings.RUN_GEN_WITH_PYGAME and settings.PYGAME_LOOK_GEN <= curgen:
                screen.fill((settings.BG_COLOR))
                for x in range(len(snake[i])):
                    pygame.draw.rect(screen, (0, 255, 0), [snake[i][x][0], snake[i][x][1], settings.SNAKE_WIDTH, settings.SNAKE_WIDTH])
                pygame.draw.rect(screen, (255, 0, 100), [apple[i][0], apple[i][1], settings.SNAKE_WIDTH, settings.SNAKE_WIDTH])
                clock.tick(settings.GAME_FPS)
                pygame.display.set_caption("Gen:    " + str(curgen) + " Snake:  " + str(i) + " Score:   " + str(s_ai[i].score) + " Steps Left:  " + str(s_ai[i].steps))
                pygame.display.update()
    scores = []
    for i in range(settings.NUM_POP):
        scores.append(s_ai[i].score)
    elite_snakes = []
    print("Highest Score for Generation " + str(curgen) + ": " + str(max(scores)) + "   Average: " + str(np.mean(scores)))
    for i in range(settings.NUM_ELITES):
        elite_snakes.append(s_ai[scores.index(max(scores))])
        del[s_ai[scores.index(max(scores))]]
        del[scores[scores.index(max(scores))]]
    elite_snake_weights = []
    for i in range(settings.NUM_ELITES):
        elite_snake_weights.append([])
        for j in range(len(elite_snakes[i].weights)):
            elite_snake_weights[i].append(np.ndarray.tolist(elite_snakes[i].weights[j]))    #Clear old boys
    snake.clear()
    apple.clear()
    s_dir.clear()
    s_ai.clear()
    scores.clear()
    eliteRoulette = []
    for z in range(settings.NUM_ELITES):
        eliteRoulette.append(z)
    for i in range(settings.NUM_ELITES):
        s_ai.append(elite_snakes[i])
    for i in range(settings.NUM_POP - settings.NUM_ELITES):
        RouletteCopy = eliteRoulette[:]
        parent1 = RouletteCopy[random.randint(0, settings.NUM_ELITES - 1)]
        del[RouletteCopy[parent1]]
        parent2 = RouletteCopy[random.randint(0, settings.NUM_ELITES - 2)]
        s_ai.append(ai.snakeNN(weights=ai.crossoverWeights(elite_snake_weights[parent1], elite_snake_weights[parent2])))
    for i in range(settings.NUM_POP):
        snake.append([[settings.SNAKE_WIDTH * ((settings.COLUMNS + 1) / 2), settings.SNAKE_WIDTH * ((settings.ROWS + 1) / 2)]])
        apple.append([random.randint(1, settings.COLUMNS) * settings.SNAKE_WIDTH, random.randint(1, settings.ROWS) * settings.SNAKE_WIDTH])
        s_dir.append([1, 0])
    elite_snake_weights.clear()
    elite_snakes.clear()

