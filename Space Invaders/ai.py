import numpy as np
import random
from settings import *
import pygame

class ShipAI():
    def __init__(self, weights=None):
        self.weights = []
        self.layers = LAYERS
        for i in range(len(self.layers) - 1):
            a = self.layers[i]
            b = self.layers[i + 1]
            self.weights.append(2 * np.random.random((a, b)) - 1)
        self.hidden = []
        self.outputs = []

        self.dead = False
        self.score = 0
    def resetScore(self):
        self.score = 0
    def tanh(self, x):
        return np.tanh(x)
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    def forward(self, inputs):
        self.hidden = []
        for i in range(len(self.weights)):
            if i == 0:
                self.hidden.append(self.tanh(np.dot(inputs, self.weights[0])))
            elif i == len(self.weights) - 1:
                self.outputs = self.sigmoid(np.dot(self.hidden[-1], self.weights[-1]))
            else:
                self.hidden.append(self.tanh(np.dot(self.hidden[i - 1], self.weights[i])))
        
def genInputs(player, enemyList):
    playerInps = []
    if(len(enemyList) == 0):
        return [-1, -1, -1, -1]
    elif len(enemyList) == 1:
        playerInps.append(player.x - enemyList[0].x)
        playerInps.append(player.y - enemyList[0].y)
        playerInps.append(-1)
        playerInps.append(-1)
    else:
        playerInps.append(player.x - enemyList[0].x)
        playerInps.append(player.y - enemyList[0].y)
        playerInps.append(player.x - enemyList[1].x)
        playerInps.append(player.y - enemyList[1].y)
    return playerInps
def getPixelColor(display):
    pixelList = []
    
    for x in range(GAME_WIDTH):
        for y in range(GAME_HEIGHT):
            a, b, c, d = display.get_at((x, y))
            pixelList.append((a + b + c) / 3)
    return pixelList
def crossover_weights(weight1, weight2, mutation=False, mutate_rate=None):
    crossed_weights = []
    for i in range(len(weight1)):
        crossed_weights.append([])
        #1st set of weights
        for j in range(len(weight1[i])):
            random_split_spot = random.randint(1, len(weight1[i][j]))
            first_cross_part = weight1[i][j][:len(weight1[i][j]) - random_split_spot][:]
            second_cross_part = weight2[i][j][len(weight2[i][j]) - random_split_spot:][:]
            crossed_weights[i].append([])
            for k in range(len(first_cross_part)):
                crossed_weights[i][j].append(first_cross_part[k])
                if mutation == True:
                    if random.uniform(0.0, 1.0) <= mutate_rate:
                        crossed_weights[i][j][k] = random.uniform(-1.0, 1.0)
            for k in range(len(second_cross_part)):
                crossed_weights[i][j].append(second_cross_part[k])
                if mutation == True:
                    if random.uniform(0.0, 1.0) <= mutate_rate:
                            crossed_weights[i][j][k] = random.uniform(-1.0, 1.0)
    return crossed_weights