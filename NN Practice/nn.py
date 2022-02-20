import numpy as np
import matplotlib.pyplot as plt

class nn():
    def __init__(self, inps, outs):
        self.x = np.reshape(inps, (len(inps), 3))
        self.y = np.reshape(outs, (len(outs), 2))
        self.weights = []
        self.layers = [3, 8, 2]
        self.pltx = []
        self.plty = []
        self.learn = 1

        for i in range(len(self.layers) - 1):
            a = self.layers[i]
            b = self.layers[i + 1]
            self.weights.append(2 * np.random.random((a, b)) - 1)
    
    def reLU(self, x, nonlin=False):
        if nonlin:
            x[x<=0] = 0
            x[x>0] = 1
            return x
        return np.maximum(0, x)    
    def tanh(self, x, nonlin=False):
        if nonlin:
            t=(np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x))
            dt=1-t**2
            return dt
        return np.tanh(x)
    def sigmoid(self, x, nonlin=False):
        if nonlin:
            return x * (1 - x)
        return 1 / (1 + np.exp(-x))

    def forward(self):
        self.hidden = []
        for i in range(len(self.weights)):
            if i == 0:
                self.hidden.append(self.reLU(np.dot(self.x, self.weights[0])))
            elif i == len(self.weights) - 1:
                self.outputs = self.sigmoid(np.dot(self.hidden[-1], self.weights[-1]))
            else:
                self.hidden.append(self.reLU(np.dot(self.hidden[i - 1], self.weights[i])))
    def backprop(self):
        self.l3E = self.y - self.outputs
        self.l3A = self.l3E * self.learn * self.sigmoid(self.outputs, nonlin=True)

        self.l2E = self.l3A.dot(self.weights[1].T)
        self.l2A = self.l2E * self.learn * self.reLU(self.hidden[0], nonlin=True)


        self.weights[0] += np.dot(self.x.T, self.l2A)
        self.weights[1] += np.dot(self.hidden[0].T, self.l3A)
    
    def predict(self, x):
        x = np.reshape(x, (len(x), 3))
        self.hidden = []
        for i in range(len(self.weights)):
            if i == 0:                
                self.hidden.append(self.reLU(np.dot(x, self.weights[0])))
            elif i == len(self.weights) - 1:
                self.outputs = self.sigmoid(np.dot(self.hidden[-1], self.weights[-1]))
            else:
                self.hidden.append(self.reLU(np.dot(self.hidden[i - 1], self.weights[i])))

        print(self.outputs)
    def train(self, epoch=120000):
        for i in range(epoch):
            self.forward()
            self.backprop()
            self.pltx.append(i)
            self.plty.append(np.mean(self.l3E))

            if i % (epoch/10) == 0:
                print("Iter: " + str(i) + " Cost: " + str(np.mean(self.l3E)))

        plt.plot(self.pltx, self.plty)
        plt.show()                    
        