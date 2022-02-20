import pygame
import random # picking a new spot for apple
import settings
import keyboard

class Snake():
    def __init__(self, gui=None):
        
        self.gui = None
        self.gui_enabled = False

        if gui != None:
            self.gui = gui
            self.gui_enabled = True

        self.x = settings.SNAKE_WIDTH * ((settings.COLUMNS + 1) / 2)
        self.y = settings.SNAKE_WIDTH * ((settings.ROWS + 1) / 2) 
        self.bodyColor = (0, 255, 0)
        self.headColor = (255, 255, 0)
        self.snake = [[self.x, self.y]]
        self.dir = [1, 0]
        self.width = settings.SNAKE_WIDTH
        self.length = 1
        self.keyboardEnabled = settings.KEYBOARD_ENABLED
        self.dead = False

    def update(self):
        
        if self.keyboardEnabled:
            if keyboard.is_pressed('w'):
                self.dir = [0, -1]
            elif keyboard.is_pressed('a'):
                self.dir = [-1, 0]
            elif keyboard.is_pressed('s'):
                self.dir = [0, 1]
            elif keyboard.is_pressed('d'):
                self.dir = [1, 0]
        self.x += self.dir[0] * self.width
        self.y += self.dir[1] * self.width

        
        self.snake.append([self.x, self.y])
        if(len(self.snake) > self.length):
            del[self.snake[0]]

        if self.gui_enabled:
            for i in range(len(self.snake)):
                if i == len(self.snake) - 1:
                    pygame.draw.rect(self.gui, self.headColor, [self.snake[i][0], self.snake[i][1], self.width, self.width])
                else:
                    pygame.draw.rect(self.gui, self.bodyColor, [self.snake[i][0], self.snake[i][1], self.width, self.width])


class Apple():
    def __init__(self, gui=None):
        self.gui = None
        self.gui_enabled = False

        if gui != None:
            self.gui = gui
            self.gui_enabled = True
        
        self.x = random.randint(1, settings.COLUMNS) * settings.SNAKE_WIDTH
        self.y = random.randint(1, settings.ROWS) * settings.SNAKE_WIDTH
        self.width = settings.SNAKE_WIDTH
        self.color = (255, 0, 100)
    def update(self):
        if self.gui_enabled:
            pygame.draw.rect(self.gui, self.color, [self.x, self.y, self.width, self.width])
