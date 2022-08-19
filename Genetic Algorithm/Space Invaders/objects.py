import pygame
from settings import *
import keyboard

class PlayerShip():
    def __init__(self, gui=None):
        self.x = SHIP_START_X
        self.y = SHIP_START_Y
        self.w = SHIP_W
        self.h = SHIP_H
        self.img = pygame.transform.scale(pygame.image.load('images/spaceship.png'), (self.w, self.h))
        self.gui = -1
        self.bulletList = []
        self.bulletTicker = 0
        if(gui!=None):
            self.gui = gui
    
    def setGUI(self, gui):
        self.gui = gui
        for bullet in self.bulletList:
            bullet.setGUI(gui)
    def fire(self):
        if(self.bulletTicker > FIRE_DELAY):
            self.bulletList.append(Bullet(self.x, self.y, gui=self.gui))
            self.bulletTicker = 0


    def checkMove(self, ai=False):
        if(keyboard.is_pressed('w')):
            self.y -= PLAYER_SPEED
        elif(keyboard.is_pressed('s')):
            self.y += PLAYER_SPEED
        # X and Y are separated for diagonal movement
        if (keyboard.is_pressed('a')):
            self.x -= PLAYER_SPEED
        elif(keyboard.is_pressed('d')):
            self.x += PLAYER_SPEED
        if(keyboard.is_pressed(" ")):
            self.fire()

    def checkBounds(self):
        if(self.x <= 0):
            self.x = 0
        elif(self.x >= GAME_WIDTH - self.w):
            self.x = GAME_WIDTH - self.w
        
        if(self.y <= 0):
            self.y = 0
        elif(self.y >= GAME_HEIGHT - self.h):
            self.y = GAME_HEIGHT - self.h

    def update(self):
        self.checkMove()
        self.checkBounds()
        if(len(self.bulletList) > 0):
            for bullet in self.bulletList:
                bullet.update()
        self.bulletTicker += 1
        if(len(self.bulletList) != 0):
            if(self.bulletList[0].y + LASER_H/2 <= 0):
                del[self.bulletList[0]]

    def draw(self):
        if self.gui != -1:
            self.gui.blit(self.img, (self.x, self.y))

            if(len(self.bulletList) > 0):
                for bullet in self.bulletList:
                    bullet.draw()

class Bullet():
    def __init__(self, x, y, gui=None):
        self.x = x + (SHIP_W/2) #Bullet Fires from mid of Ship
        self.y = y
        self.gui = -1
        self.w = LASER_W
        self.h = LASER_H
        self.img = pygame.transform.scale(pygame.image.load('images/laser.png'), (self.w, self.h))
        self.speed = LASER_SPEED
        if gui != None:
            self.gui = gui
    def setGUI(self, gui):
        self.gui = gui
    def update(self):
        self.y -= self.speed
    def draw(self):
        self.gui.blit(self.img, (self.x, self.y))

class Enemy():
    def __init__(self, x, gui=None):
        self.gui = -1
        self.x = x
        self.y = 0
        self.w = ALIEN_W
        self.h = ALIEN_H
        self.passed = False
        self.img = pygame.transform.scale(pygame.image.load('images/alien.png'), (self.w, self.h))
        if gui != None:
            self.gui = gui
    def setGUI(self, gui):
        self.gui = gui
    def update(self):
        self.y += ALIEN_SPEED
    def draw(self):
        if self.gui != -1:
            self.gui.blit(self.img, (self.x, self.y))
            #pygame.draw.rect(self.gui, (0, 255, 0), [self.x, self.y, self.w, self.h])