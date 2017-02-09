import numpy as np 
from logsum import log_sum
import sys

devfile = open(sys.argv[1], "r")
devfile = devfile.readlines()
devfile = map(lambda s: s.strip(), devfile)

transfile = open(sys.argv[2], "r")
transfile = transfile.readlines()
transfile = map(lambda s: s.strip(), transfile)

emitfile = open(sys.argv[3], "r")
emitfile = emitfile.readlines()
emitfile = map(lambda s: s.strip(), emitfile)

priorfile = open(sys.argv[4], "r")
priorfile = priorfile.readlines()
priorfile = map(lambda s: s.strip(), priorfile)

def transMatrix():
	trans = []
	for line in transfile:
		t = []
		line  = line.split(" ")
		#print line
		for i in range(1, len(line)):
			prob = line[i].split(":")[1]
			t.append(float(prob))
		trans.append(t)
	return np.array(trans)

def priorMatrix():
	prior = []
	for line in priorfile:
		line = line.split(" ")
		prior.append(float(line[1]))
	return np.array(prior).reshape(8,1)

def emitMatrix():
	d = {}
	for i in range(0, len(emitfile)):
		line = emitfile[i]
		line  = line.split(" ")
		#print line[791].split(":")[1]
		for j in range(1, len(line)):
			if i == 0:
				d[line[j].split(":")[0]] = []
			prob = line[j].split(":")[1]
			d[line[j].split(":")[0]].append(float(prob))
	return d

def backward():
  emit = emitMatrix()
  trans = transMatrix()
  prior = priorMatrix()
  for line in devfile:
    line = line.split(" ")
    o = line[0]
    probMatrix = np.log(np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]).reshape(8,1))
    # loop throgh words in line
    for z  in range(len(line) - 2, -1,-1):
      o = line[z + 1]
      emitprob = np.array(emit[o]).reshape(8,1)
      # loop through each t+1 state
      m = []
      for j in range (0, 8):
        temp = np.log(trans[j,:].reshape(8,1)) + (probMatrix) + np.log(emitprob)

        sum = temp[0]
        for k in range(1, 8):
          sum = log_sum(sum, temp[k])
        m.append(sum)
      probMatrix = np.array(m).reshape(8,1)

    probMatrix = probMatrix + np.log(prior)

    emitprob = np.log(np.array(emit[line[0]]).reshape(8,1))
    probMatrix = probMatrix + emitprob
    total = probMatrix[0]
    for h in range(1, 8):
      total = log_sum(total, probMatrix[h])
    
    print total[0]

backward()



















