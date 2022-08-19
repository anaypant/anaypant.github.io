import nn
import numpy as np

trainX = [[1, 1, 0],[0, 1, 1],[1, 1, 1],[1, 0, 1],[1, 0, 0],[1, 1, 0], [0, 1, 0]]
trainY = [[1, 0],[0, 1],[1, 0],[0, 1],[0, 1],[1, 0], [0, 1]]
testX = [[-1, 0, 1], [0, 1, -1], [-1, 0, -1]]
testY = [[0, 1],[0, 1],[1, 0]]
test = nn.nn(trainX, trainY)
test.train()
test.predict(testX)
print(np.reshape(testY, (len(testY), 2)))
