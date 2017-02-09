import sys

# 1
print (16) # size of the input space 
# 2
print (65536)



inputfile = sys.argv[1]
fo = open(inputfile, "r")
inputData = fo.readlines()
lInput = len(inputData)

#3

trainingData = "4Cat-Train.labeled"
fo = open(trainingData, "r")
trainingData = fo.readlines()
lTrain = len(trainingData)

def extract (d):
  newData = []
  l = len(d)
  for i in range(0, l):
    data = d[i]
    data = data.split()
    newData += [[data[1], data[3], data[5], data[7], 
                  data[9]]]
  return (newData)

def atrrToInd(example):
  s = ""
  for i in range (0, 4):
    atrr = example[i]
    if (atrr == "Male" or atrr == "Young" or atrr == "Yes" or atrr == "Yes"):
      s += "1"
    else:
      s +="0"
  return int(s, 2)

def versionSpace():
  H = [2,2,2,2,2,2,2,2,
       2,2,2,2,2,2,2,2]
  data = extract(trainingData)
  for i in range(0, lTrain):
    example = data[i]
    ind = atrrToInd(example)
    if data[i][4] == "high":
      res = 1
    else:
      res = 0

    if H[ind] == 2:
      H[ind] = res
    elif H[ind] != res:
      H[ind] = 2

  result = 1
  for j in range (0, 16):
    if H[j] == 2:
      result = result * 2
  return (H, result)


(arg1, arg2) = versionSpace()
print arg2


def vote():
  H, res = versionSpace()
  data = extract(inputData)
  for i in range (0, lInput):
    example = data[i]
    ind = atrrToInd(example)
    if H[ind] == 2:
      print (str(res/2) + " " + str(res/2))
    elif H[ind] == 1:
      print("here")
      print (str(res) + " " + str(0))
    elif H[ind] == 0:
      print(str(0) + " " + str(res))

vote()















