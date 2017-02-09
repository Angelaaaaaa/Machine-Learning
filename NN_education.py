import sys
import math
import numpy as np 
import random

train = sys.argv[1]
fo = open(train, "r")
trainData = fo.readlines()
attr = trainData[0].split(",")
lTrain = len(trainData)
trainData = trainData[1:lTrain]
lTrain -= 1

test = sys.argv[2]
fo = open(test, "r")
testData = fo.readlines()
lTest = len(testData)
testData = testData[1:lTest]
lTest = len(testData)

def randW():
	a = random.random()
	b = random.random()
	return a * b

def inputMatrix(data, length):
  inputM = []
  target = []
  for i in range(0 , length):
    i = data[i]
    row = []
    #row.append(1.0) # bias node
    info = i.split(",")
    for j in range (0, len(attr) - 1):
      s = info[j]
      row.append(float(s)/100.0)
    inputM.append(row)
    lable = info[len(attr) - 1]
    target.append(float(lable))
  #print inputM
  return np.matrix(inputM), np.matrix(target)

# print (inputMatrix(trainData, lTrain)[1])


def createW1(n):
  return np.random.random(size=(len(attr) - 1, n))/10

def createW2(n):
  return np.random.random(size=(n, 1))/10


class NN:
  def __init__(self, n = 50):
    self.w1 = createW1(n) # weight for input 
    self.w2 = createW2(n) # weight for output
    (self.z1, self.target) = inputMatrix(trainData, lTrain) # input and target 
    self.target = self.target / 100.0
    self.d3 = np.empty((lTrain, 1))
    self.d2 = np.empty((lTrain, 1))
    self.N = 0.001

  

  def sigM(self,matrix):
    return 1.0 / (1.0 + np.exp(- matrix))

  def Dsig(self, matrix):
    return np.multiply(self.sigM(matrix), (1 - self.sigM(matrix)))

  
  def back(self):
    self.z2 = np.dot(self.z1, self.w1)  
    self.a2 = self.sigM(self.z2) # sigmoid hidden layer
    self.z3 = np.dot(self.a2, self.w2) # input for output
    self.a3 = self.sigM(self.z3) # sigmoid output

    self.error = self.a3 - self.target.T # error

    # modify w2
    self.d3 = np.mat(self.d3)
    self.d3 = np.multiply(self.Dsig(self.z3), self.error)
    self.dw2 = np.dot(self.a2.T, self.d3)
    

    # modify w1
    self.d2 = np.dot(self.d3, self.w2.T)
    self.d2 = np.multiply(self.d2, self.Dsig(self.z2))
    self.dw1 = np.dot(self.z1.T, self.d2)

    self.w1 = self.w1 - self.N * self.dw1
    self.w2 = self.w2 - self.dw2 * self.N
    
 
def readDev():
  inputM = []
  for i in range(0 , lTest):
    i = testData[i]
    row = []
    info = i.split(",")
    for j in range (0, 5):
      s = info[j]
      row.append(float(s)/100.0)
    inputM.append(row)
  return np.matrix(inputM)

def run():
  nn = NN()

  k = 100
  count = 0 
  for i in range (0, 10000):
    nn.back()
    error = np.sum(np.square(nn.error))
    #if error < k:
    print (error)

  print ("TRAINING COMPLETED! NOW PREDICTING.")
  w1 = nn.w1
  w2 = nn.w2
  x = readDev()
  o = np.dot(x, w1)
  o = nn.sigM(o)
  o = np.dot(o, w2)
  o = nn.sigM(o) 
  
  for i in range (0, lTest):
    print o.item(i) * 100

  print nn.d3

run()













      
