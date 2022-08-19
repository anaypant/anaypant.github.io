import math
from math import nan
from random import triangular
import seaborn as sns
import pandas as pd
import numpy as np

def create_data():
    Olddf = sns.load_dataset('titanic').values.tolist()
    Y = []
    X = []
    df = []
    for x in Olddf:
        if x[0] is nan or x[1] is nan or x[2] is nan or math.isnan(x[3]) or x[14] is nan:    
            continue
        else:
            df.append(x)
    maxAge = max(l[3] for l in df)
    for i in range(len(df)):
        Y.append([df[i][0]])
        X.append([])

        # Class

        if df[i][1] == 1:
            X[i].append(1)
            X[i].append(0)
            X[i].append(0)
        elif df[i][1] == 2:
            X[i].append(0)
            X[i].append(1)
            X[i].append(0)
        elif df[i][1] == 3:
            X[i].append(0)
            X[i].append(0)
            X[i].append(1)

        # Man or Woman
        if df[i][2] == 'male':
            X[i].append(1)
            X[i].append(0)
        elif df[i][2] == 'female':
            X[i].append(0)
            X[i].append(1)

        # Age
        X[i].append(df[i][3] / maxAge)

        if df[i][14] == False:
            X[i].append(0)
        else:
            X[i].append(1)
    return X, Y

# Data
# One Hot Encode Class, One Hot Encode Sex, Age, Alone



class NeuralNetwork:
    def __init__(self, x, y):
        self.x = np.reshape(x, (len(x), len(x[0])))
        self.y = np.reshape(y, (len(y), len(y[0])))

        self.weights = []
        self.learn = 1
        self.terminateEarlyThreshmmark=7e-4
        self.l3E =[1]
        LAYERS = [len(self.x[0]), 6, 4, len(self.y[0])]
        for z in range(len(LAYERS) - 1):
            a = LAYERS[z]
            b = LAYERS[z + 1]
            self.weights.append(2 * np.random.random((a, b)) - 1)
    def reset(self):
        self.weights = []
        LAYERS = [len(self.x[0]), 6, 4, len(self.y[0])]
        for z in range(len(LAYERS) - 1):
            a = LAYERS[z]
            b = LAYERS[z + 1]
            self.weights.append(2 * np.random.random((a, b)) - 1)

    def get_model_prediction(self,input, model):
        hidden = []
        hidden.append(self.tanh(np.dot(input, model[0])))
        hidden.append(self.tanh(np.dot(hidden[0], model[1])))
        outputs = self.sigmoid(np.dot(hidden[1], model[2]))
        return outputs
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    def sigmoidDeriv(self, x):
        return x * (1 - x)
    def relu(self, x):
        return np.maximum(0, x)
    def reluDeriv(self, x):
        x[x<=0] = 0
        x[x>0] = 1
        return x
    def tanh(self, x):
        return np.tanh(x)
    def tanhDeriv(self, x):
        return 1 - (x**2)
    def forward(self):
        self.hidden = []
        self.hidden.append(self.tanh(np.dot(self.x, self.weights[0])))
        self.hidden.append(self.tanh(np.dot(self.hidden[0], self.weights[1])))
        self.outputs = self.sigmoid(np.dot(self.hidden[1], self.weights[2]))
    def backprop(self):
        self.l3E = self.y - self.outputs
        self.l3A = self.l3E * self.learn * self.sigmoidDeriv(self.outputs)

        self.l2E = self.l3A.dot(self.weights[2].T)
        self.l2A = self.l2E * self.learn * self.tanhDeriv(self.hidden[1])
        
        self.l1E = self.l2A.dot(self.weights[1].T)
        self.l1A = self.l1E * self.learn * self.tanhDeriv(self.hidden[0])

        self.weights[0] += np.dot(self.x.T, self.l1A)
        self.weights[1] += np.dot(self.hidden[0].T, self.l2A)
        self.weights[2] += np.dot(self.hidden[1].T, self.l3A)

    def train(self,iters=20000,learn=0.03,batches=128,inpX=[],inpY=[]):
        bestError=1
        bestModel=[]
        bestBatch=-1
        
        self.learn = learn
        for batch in range(batches):
            self.reset()
            print('\n')
            print('----- Starting Batch  ' + str(batch) + ' -----\n')
            counter = 0
            self.l3E = [1]

            while abs(np.mean(self.l3E))>=self.terminateEarlyThreshmmark and counter <= iters:
                self.forward()
                self.backprop()
                if counter % (iters/25) == 0:
                    print("Batch " + str(batch) + ":   Iter " + str(counter) + ": " + str(np.mean(self.l3E)))
                    print("\n")
                counter+=1
            if self.getTestScore(inpX, inpY, self.weights) < bestError:
                bestBatch = batch
                bestModel = self.weights[:]
                bestError = abs(np.mean(self.l3E))
        print("Best batch: " + str(bestBatch))
        print("Best Error: " + str(bestError))
        print("Best Model Test:\n")
        print(self.getTestScore(inpX,inpY,bestModel))
        f = open("models.txt", 'a')
        f.write(str(bestModel))
        f.close()
    def getTestScore(self,inputX, inputY, w):
        numCorrect=0
        numTotal = len(inputX)
        X = inputX
        Y = inputY
        weights = w
        for z in range(len(X)):
            hidden = []

            hidden.append(self.tanh(np.dot(X[z], weights[0])))
            hidden.append(self.tanh(np.dot(hidden[0], weights[1])))
            outputs = self.sigmoid(np.dot(hidden[1], weights[2]))
            outputs[0] = round(outputs[0])
            if Y[z][0] == outputs[0]:
                numCorrect += 1
        return numCorrect/numTotal

if __name__ == "__main__":
    tX, tY = create_data()
    length = len(tX)
    trainLength = round(0.8 * length)
    trainX = tX[0:trainLength][:]
    trainY = tY[0:trainLength][:]
    testX = tX[trainLength:length][:]
    testY = tY[trainLength:length][:]
    goodModel = [np.array([[-0.65921617,  0.10793684, -0.86164627,  0.26639959, -0.93802423,
        -0.561753  ],
       [-0.42296884, -0.43409512,  0.92517293,  0.96940479, -0.94841225,
         0.15141532],
       [-0.62688867, -0.19181019,  0.33539211, -0.39765122,  0.35442679,
        -0.0034334 ],
       [-0.64774444,  0.26825455,  0.43308026, -0.61876538,  0.06748953,
         0.50384032],
       [ 0.01149958, -0.90051436, -0.05990583, -0.20984681, -0.38332415,
        -0.52687887],
       [ 0.5820349 ,  0.9638631 , -0.97898107, -0.78279105, -0.46856769,
        -0.99921735],
       [-0.89437471,  0.72244132, -0.02824702,  0.47126191,  0.21642018,
        -0.84291585]]), np.array([[ 0.94347516, -0.82131193, -1.26767742,  0.11079761],
       [-0.87945305,  0.74107271,  0.09302073,  1.13797806],
       [-0.77113458, -0.84818224, -0.30475238,  0.16355453],
       [ 0.97609024, -0.79737155,  0.44012363, -0.64927368],
       [-0.93979954,  0.82577978,  0.10391649, -0.13579469],
       [ 0.43688737, -0.16767991,  0.04765298, -0.48471601]]), np.array([[ 4.40861977],
       [ 3.61451468],
       [ 4.41548913],
       [-4.53223089]])]
    testNN = NeuralNetwork(tX, tY)
    #testNN.train(batches=16,inpX=testX,inpY=testY)

    while True:
        inputX = []
        cl = input("Enter 1, 2, or 3 for class type: ")
        age = None
        gender =''
        alone = None

        while cl != '1' and cl != '2' and cl != '3':
            cl = input("Enter 1, 2, or 3 for class type: ")
        while gender != 'male' and gender != 'female':
            gender = input("Type 'male' or 'female' for gender (match case): ")
        while age is None:
            age = input("Enter age - must be a number: ")
            age = float(age)/80
        while alone is  None:
            alone = input("Enter 'A' for alone and 'N' not alone: ")
        
        if cl == '1':
            inputX.append(1)
            inputX.append(0)
            inputX.append(0)
        elif cl == '2':
            inputX.append(0)
            inputX.append(1)
            inputX.append(0)
        elif cl == '3':
            inputX.append(0)
            inputX.append(0)
            inputX.append(1)
        if gender == 'male':
            inputX.append(1)
            inputX.append(0)
        else:
            inputX.append(0)
            inputX.append(1)
        inputX.append(age)
        if alone == 'A':
            inputX.append(1)
        else:
            inputX.append(0)
        print("\n")
        print("AI says there is a " + str(round(100 * testNN.get_model_prediction(inputX, goodModel)[0], 4)) + " percent chance you will survive the Titanic!\n")

    