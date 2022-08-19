import pygame
import settings
import objects
import random

pygame.init()
screen = pygame.display.set_mode((settings.CANV_WIDTH, settings.CANV_HEIGHT))
clock = pygame.time.Clock()
player = objects.Snake(gui=screen)
apple = objects.Apple(gui=screen)
game_over = False

while not game_over:
    screen.fill(settings.BG_COLOR)
    player.update()
    apple.update()
    if(player.snake[-1] == [apple.x, apple.y]):
        player.length += 1
        apple.x = random.randint(1, settings.COLUMNS) * settings.SNAKE_WIDTH
        apple.y = random.randint(1, settings.ROWS) * settings.SNAKE_WIDTH

    clock.tick(settings.GAME_FPS)
    pygame.display.update()