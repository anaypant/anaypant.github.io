import numpy as np
import settings
import math
import random

class snakeNN():
    def __init__(self, weights=None):
        self.layers = settings.WEIGHTS
        self.weights = []
        for i in range(len(self.layers) - 1):
            a = self.layers[i]
            b = self.layers[i + 1]
            self.weights.append(2 * np.random.random((a, b)) - 1)
        if (weights != None):
            self.weights = weights
            for i in range(len(self.weights)):
                self.weights[i] = np.reshape(self.weights[i], (self.layers[i], self.layers[i + 1]))
        self.score = 0
        self.dead = False
        self.steps = settings.STEPS
        self.length = 1
    def tanH(self, x):
        return np.tanh(x)
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    def FF(self, inputs):
        self.hidden = []
        for i in range(len(self.weights) - 1):
            if i == 0:
                self.hidden.append(self.tanH(np.dot(inputs, self.weights[0])))
            else:
                self.hidden.append(self.tanH(np.dot(self.hidden[i - 1], self.weights[i])))
        self.outputs = self.sigmoid(np.dot(self.hidden[-1], self.weights[-1]))
        self.key = 0
        for i in range(len(self.outputs)):
            if(self.outputs[i] > self.outputs[self.key]):
                self.key = i

def calculateDistance(x, y):
    a = x[0] - y[0]
    b = x[1] - y[1]
    return (math.sqrt((a ** 2) + (b ** 2)))/settings.CANV_WIDTH
def genInputs(snake, apple, snake_dir):
    snakeInputs = []
    directions = [[-1, -1],[0, -1],[1, -1],[1, 0],[1, 1],[0, 1],[-1, 1],[-1, 0]]
    
    for direction in directions:
        snake_head = snake[-1][:]
        isApple = False
        isBody = False
        appDist = 0
        bodDist = 0
        while(0 <= snake_head[0] <= (settings.CANV_WIDTH - settings.SNAKE_WIDTH) and 0 <= snake_head[1] <= (settings.CANV_HEIGHT - settings.SNAKE_WIDTH)):
            if(snake_head == apple):
                isApple = True
                appDist = calculateDistance(snake[-1], snake_head)
            else:
                if len(snake) > 1:
                    for i in range(len(snake) - 1):
                        if snake[i] == snake_head:
                            isBody = True
                            bodDist = calculateDistance(snake[-1], snake_head)
            snake_head[0] += direction[0] * settings.SNAKE_WIDTH
            snake_head[1] += direction[1] * settings.SNAKE_WIDTH
        wallDist = calculateDistance([snake_head[0] - direction[0] * settings.SNAKE_WIDTH, snake_head[1] - direction[1] * settings.SNAKE_WIDTH], snake[-1])
        if(isApple):
            snakeInputs.append(1)
        else:
            snakeInputs.append(0)
        if(isBody):
            snakeInputs.append(1)
        else:
            snakeInputs.append(0)
        if isApple:
            snakeInputs.append(appDist)
        elif isBody:
            snakeInputs.append(bodDist)
        else:
            snakeInputs.append(wallDist)
    if (snake_dir == [0, -1]):
        snakeInputs.append(1)
        snakeInputs.append(0)
        snakeInputs.append(0)
        snakeInputs.append(0)
    elif (snake_dir == [-1, 0]):
        snakeInputs.append(0)
        snakeInputs.append(1)
        snakeInputs.append(0)
        snakeInputs.append(0)
    elif (snake_dir == [0, 1]):
        snakeInputs.append(0)
        snakeInputs.append(0)
        snakeInputs.append(1)
        snakeInputs.append(0)
    elif (snake_dir == [1, 0]):
        snakeInputs.append(0)
        snakeInputs.append(0)
        snakeInputs.append(0)
        snakeInputs.append(1)
    return snakeInputs
def getLeftCoord(direction):
    if direction == [0, -1]:

        return [-1, 0]
    elif direction == [-1, 0]:

        return [0, 1]
    elif direction == [0, 1]:

        return [1, 0]
    elif direction == [1, 0]:

        return [0, -1]

def getRightCoord(direction):
    if direction == [0, -1]:

        return [1, 0]
    elif direction == [1, 0]:

        return [0, 1]
    elif direction == [0, 1]:

        return [-1, 0]
    elif direction == [-1, 0]:

        return [0, -1]

def crossoverWeights(parent1, parent2, mutations=False, mutateRate = 0):
    crossedWeights = []
    for i in range(len(parent1)):
        splitSpot =  random.randint(1, len(parent1[i]) - 2)#random index
        crossedChrome = parent1[i][:splitSpot] + parent2[i][-(len(parent2[i]) - splitSpot):]
        crossedWeights.append(crossedChrome)
    if mutations:
        if (random.uniform(0, 1.0) <= mutateRate):
            randomWeights = []
            for i in range(len(parent1)):
                randomWeights.append([])
                for j in range(len(parent1[i])):
                    randomWeights[i].append(random.random())
            return randomWeights
    return crossedWeights

if __name__ == "__main__":
    test_inps = genInputs([[260, 300],[280, 300],[settings.SNAKE_WIDTH * ((settings.COLUMNS + 1) / 2), settings.SNAKE_WIDTH * ((settings.ROWS + 1) / 2)]], [0, 0], [1, 0])
    print(test_inps)
    test = snakeNN()
    test.FF(test_inps)
    print(test.outputs)