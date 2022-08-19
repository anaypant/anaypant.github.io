import numpy as np
from settings import *
import random

class blockNN():
    def __init__(self, weights=None):
        self.weights = []
        self.layers = LAYERS
        self.score = 0
        self.dead = False
        for i in range(len(self.layers) - 1):
            a = self.layers[i]
            b = self.layers[i + 1]
            self.weights.append(2 * np.random.random((a, b)) - 1)
        
        if weights != None:
            self.weights = weights
            for i in range(len(self.weights)):
                    self.weights[i] = np.array(self.weights[i])

    def relu(self, x):
        return np.tanh(x)
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def forward(self, inputs):
        self.hidden = []
        self.outputs = []
        for i in range(len(self.weights)):
            if i == 0:
                self.hidden.append(self.relu(np.dot(inputs, self.weights[0])))
            elif i == len(self.weights) - 1:
                self.outputs = self.sigmoid(np.dot(self.hidden[i - 1], self.weights[i]))
            else:
                self.hidden.append(self.relu(np.dot(self.hidden[i - 1], self.weights[i])))
        self.key = 0
        for i in range(len(self.outputs)):
            if self.outputs[i] >= self.outputs[self.key]:
                self.key = i

def genInputs(playerCoords, closestEnemCoords):
    retInps = []
    retInps.append(closestEnemCoords[1] - playerCoords[1])
    retInps.append(closestEnemCoords[0] - playerCoords[0])
    return retInps

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