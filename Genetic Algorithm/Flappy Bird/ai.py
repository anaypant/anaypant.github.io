import numpy as np
import random

class nn():
    def __init__(self, weights=None):
        
        self.weights = []
        self.weights.append(2 * np.random.random((3, 6)) - 1)
        self.weights.append(2 * np.random.random((6, 1)) - 1)
        self.hidden = []

        #if there are weights
        if weights != None:
            self.weights = weights
            for i in range(len(self.weights)):
                    self.weights[i] = np.array(self.weights[i])
        
        #For the Genetic Algorithm
        self.dead = False
        self.score = 0
        self.velocity = 0
        self.is_jumping = False
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    def sigmoid_deriv(self, x):
        return x * (1 - x)
    def ReLU(self, x):
        return np.tanh(x)
    def reluDerivative(self, x):
        x[x<=0] = 0
        x[x>0] = 1
        return x

    def forward(self, x):
        self.hidden = []
        self.x = x
        self.hidden = self.ReLU(np.dot(self.x, self.weights[0]))
        self.outputs = self.sigmoid(np.dot(self.hidden, self.weights[1]))    

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
        #2nd set of snakes

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

if __name__ == "__main__":
    np.random.seed(1)
    test = nn()
    test.forward()
