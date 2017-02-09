import sys

# 1
print (512) # size of the input space 
# 2
print (155) # number of decimal digits in |C|
# 3
print (19684) # size of the hypothesis space

inputfile = sys.argv[1]
fo = open(inputfile, "r")
inputData = fo.readlines()
lInput = len(inputData)

trainingData = "9Cat-Train.labeled"
fo = open(trainingData, "r")
trainingData = fo.readlines()
lTrain = len(trainingData)

devData = "9Cat-Dev.labeled"
fo = open(devData, "r")
devData = fo.readlines()
lDev = len(devData)

# spliting data into list of attributes
def extract (d):
  newData = []
  l = len(d)
  for i in range(0, l):
    data = d[i]
    data = data.split()
    newData += [[data[1], data[3], data[5], data[7], 
                  data[9], data[11], data[13], data[15],
                  data[17], data[19]]]
  return (newData)

def printH(H):
  l = len(H)
  s = ""
  for i in range(0,9):
     s+=H[i]
     if i != 8:
       s+="\t"
  return (s)

def findS():
  f1=open('partA4.txt', 'w+')
  H = [0, 0,0,0,0,0,0,0,0]
  newTraining = extract(trainingData)
  for i in range (0, lTrain):
    example = newTraining[i]
    if example[9] == "high":
      for j in range (0, 9):
        example_attribute = example[j]
        hypothesis_attribute = H[j]
        if hypothesis_attribute == 0:
          hypothesis_attribute = example_attribute
        elif  hypothesis_attribute != example_attribute:
          hypothesis_attribute = "?"


        H[j] = hypothesis_attribute
    if ((i + 1) % 30 == 0):
      print >> f1, printH(H)
  return (H)


def missRate():
  H = findS()
  lables = []
  data = extract(devData)
  miss = 0
  for i in range (0, lDev):
    event = data[i]
    lables += [event[9]]
    for j in range (0, 9):
      if (H[j] != "?" and H[j] !=  event[j] and event[9] == "high"):
        miss += 1
      if (H[j] != "?" and H[j] ==  event[j] and event[9] == "low"):
        miss += 1
  total = len(lables)
  print(miss*1.0/total)

def applyH():
  inputCases = extract(inputData)
  H = findS() 
  for i in range (0, lInput):
    x = "high"
    for j in range (0, 9):
      if (H[j] != "?" and H[j] !=  inputCases[i][j]):
        x = "low"
    print (x)

      


findS()
missRate()
applyH()






