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
	l = []
	for i in range(0, len(emitfile)):
		line = emitfile[i]
		line  = line.split(" ")
		#print line[791].split(":")[1]
		l.append(line[0])
		for j in range(1, len(line)):
			if i == 0:
				d[line[j].split(":")[0]] = []
			prob = line[j].split(":")[1]
			d[line[j].split(":")[0]].append(float(prob))
	return d, l

def viterbi():
  emit, l = emitMatrix()
  trans = transMatrix()
  prior = priorMatrix()

  res = []
  for line in devfile:

    line = line.split(" ")
    o = line[0]
    probMatrix = np.log(prior) + np.log(np.array(emit[o]).reshape(8,1))
    Q = [[0],[1],[2],[3],[4],[5],[6],[7]]

    # loop throgh words in line
    for z  in range(1, len(line)):
      newQ = []
      o = line[z]
      emitprob = np.array(emit[o]).reshape(8,1)

      # loop through each t+1 state
      m = []
      for j in range (0, 8):
        temp = np.log(trans[:,j].reshape(8,1)) + (probMatrix) + np.log(emitprob[j])

        max = temp[0]
        index = 0
        # sum up probs
        for k in range(1, 8):
          if max < temp[k]:
            #print max, temp[k],k
            max = temp[k]
            index = k
        #sys.exit()
        prob = max
        m.append(prob[0])
        newQ.append(Q[index] + [j])
      Q = newQ
      
      probMatrix = np.array(m).reshape(8,1)
    #print Q
      maxi = probMatrix[0][0]
      ind = 0
      for h in range (0, 8):
        if probMatrix[h][0] > maxi:
          maxi = probMatrix[h][0]
          ind = h

    path = Q[ind]
    s = ""
    for z in range(0, len(line)):
      n = path[z]
      #print line[z], l[n]
      s = s + line[z] + "_" + l[n] + " "
    print s[:len(s) - 1]

    #sys.exit()












viterbi()