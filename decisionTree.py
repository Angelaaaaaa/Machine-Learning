import sys
import math
import operator

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



def entropy (D):
  E = 0
  total = sum(D.values())
  for key in D:
    p = D[key] * 1.0 / (total)
    E += p * math.log(1.0 / (p * 1.0), 2)
  return (E)

def mutrual (E, plus, minus):
  EP = entropy(plus)
  EM = entropy(minus)
  Psum = sum(plus.values())
  Msum = sum(minus.values())
  P = Psum * 1.0 / (Psum + Msum)
  M = Msum * 1.0 / (Psum + Msum)
  result = E - (P * EP + M * EM)
  return result


def fintRoot():
  roots = {}
  l =len(attr)
  L = {}
  for i in trainData:
    info = i.split(",")
    if info[l - 1] in L.keys():
      L[info[l - 1]] += 1
    else:
      L[info[l - 1]] = 1
  E = entropy(L)

  for i in range(0, l - 1):
    D = {}
    for j in range(0, lTrain):
      info = trainData[j].split(",")
      label = info[l - 1]
      if info[i] in D.keys():
        if label in D[info[i]].keys():
          D[info[i]][label] += 1
        else:
          D[info[i]][label] = 1
      else:
        D[info[i]] = {label: 1}
    mutrualE = mutrual(E, D[D.keys()[0]], D[D.keys()[1]])
    roots[attr[i]] = mutrualE
  
  maxKey = max(roots.iteritems(), key = operator.itemgetter(1))[0]
  #print ("Label", L, "root", maxKey)
  return (L, maxKey)



def findNode(data, length):
  Node = {}
  (L, root) = fintRoot()
  i = attr.index(root)
  D = {}
  l = len(attr)
  # create root distionary
  for j in range(0, length):
    info = data[j].split(",")
    label = info[l - 1]
    if info[i] in D.keys():
      if label in D[info[i]].keys():
        D[info[i]][label] += 1
      else:
        D[info[i]][label] = 1
    else:
      D[info[i]] = {label: 1}
  #print ("level 1:", D)
  
  
  r = {}
  for rootKey in D.keys():
    Set = {}
    N = [] # to decide which node to choose
    if entropy(D[rootKey]) >= 0.1:
      # loop through attributes
      for k in range (0, l - 1):
        if i != k:

          R = {}
          E = entropy(D[rootKey])
          # loop through y or n of root
          #for rootLable in D[rootKey].keys():
          #print (rootLable)
          # loop through data
          for j in range (0, length):
            info = data[j].split(",")
            label = info[l - 1]
            if info[i] == rootKey:
              if info[k] in R.keys():
                if label in R[info[k]].keys():
                  R[info[k]][label] += 1
                else:
                  R[info[k]][label] = 1
              else:
                R[info[k]] = {label: 1}
        #print(D)
          #print (D[rootKey])
          #print ("R:", R, E)
          mutrualE = mutrual(E, R[R.keys()[0]], R[R.keys()[1]])
          if mutrualE >= 0.1:
            N.append({attr[k]: mutrualE})
          #print ("R", R)
          Set[attr[k]] = R
          #print (rootKey)
          #print("set:",Set,N)
    if N != []:
      [maxi] = [0]
      for nodes in N:
        if nodes.values() > [maxi]:
          [maxi] = nodes.values()
          [node] = nodes.keys()
      if maxi >= 0.1:
        Node[rootKey] = node
      #print ("change r")
      for n in Node.keys():
        if n == rootKey:
          r[n] = Set[Node[n]]
        #print (r)


  #print (D, L, root, Node, r)
  return (D, L, root, Node, r)
        

    #max MI

def error(data, length):
  (D, L, root, Node, r) = findNode(trainData, lTrain)
  #(D, L, root, Node, r) = findNode(data, length)

  #print ("root:", root)
  #print ("Label", L)
  #print ("best nodes:",Node)
  #print ("level 2", r)
  #print ("level 1:", D)
  
  rootIndex = attr.index(root)
  #print(rootIndex)
  #print("root index", rootIndex)
  errorCount = 0
  for j in range(0, length):
    info = data[j].split(",")
    label = info[len(info) - 1]
    level1 = info[rootIndex]
    #print (Node, info[rootIndex])
    if info[rootIndex] in Node.keys():
      #print("in")
      node = Node[info[rootIndex]]
      #print (node)
      nodeIndex = attr.index(node)
      #print(nodeIndex)
      level2 = info[nodeIndex]
      possible = r[level1][level2]
      #print(level2)
    else:
      #print("out")
      #print ("r[level1]", r, level1)
      possible = D[level1]
      guess = max(possible.iteritems(), key = operator.itemgetter(1))[0]
    guess = max(possible.iteritems(), key = operator.itemgetter(1))[0]
    #print ("guess:", guess, label)

    if (guess.replace("\r", "")).replace("\n", "") != (label.replace("\r", "")).replace("\n", ""):
      #print(j,info, guess.replace("\r\n", ""), (label.replace("\r\n", "")).replace("\n", ""))
      errorCount += 1
      #print ("counter:", errorCount)
    #print (node)

  return (errorCount * 1.0 / length)   


trainError = "error(train): %f" % (error(trainData, lTrain))
testError = "error(test): %f" % (error(testData, lTest))



def printTree():
  positives = ["democrat\r\n", "A\r\n", "yes\r\n"]
  (D, L, root, Node, r) = findNode(trainData, lTrain)
  label = L.keys()[0]
  for l in positives:
    if l in L.keys():
      label = l

    '''  
  print ("root:", root)
  print ("Label", L)
  print ("best nodes:",Node)
  print ("level 2", r)
  print ("level 1:", D)
'''
  #print label
  if label in L.keys():
    positive = L[label]
  else:
    positive = 0
  negative = sum(L.values()) - positive
  s = "[%d+/%d-]" %(positive, negative)
  print(s)
  #print root
  for rootlevel in D.keys():
    if label in D[rootlevel].keys():
      positive = D[rootlevel][label]
    else:
      positive = 0
    negative = sum(D[rootlevel].values()) - positive
    s = "%s = %s: [%d+/%d-]" % (root, rootlevel, positive, negative)
    print (s)
    if rootlevel in r.keys():
      for nodelevel in r[rootlevel].keys():
        if label in r[rootlevel][nodelevel].keys():
          positive = r[rootlevel][nodelevel][label]
        else:
          positive = 0
        negative = sum(r[rootlevel][nodelevel].values()) - positive
        s = "| %s = %s: [%d+/%d-]" % (Node[rootlevel], nodelevel, positive, negative)
        print (s)


  print (trainError)
  print (testError)





printTree()





