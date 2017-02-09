import sys
from collections import Counter
import math

train = sys.argv[1]
fo = open(train, "r")
docs = fo.readlines()
docs = map(lambda s: s.strip(), docs)

test = sys.argv[2]
fo = open(test, "r")
test = fo.readlines()
test = map(lambda s: s.strip(), test)

n = len(docs[0].replace(" ", "")) - 1

# train Vnb
def Vnb():
  libL = []
  conL = []
  # split C and L txt file
  for i in range (0, len(docs)):
    t = docs[i]
    t = t.replace(" ", "")
    if t[n] == "1":
      libL.append(t[0:n])
    else:
      conL.append(t[0:n])
  ll = len(libL)
  lc = len(conL)
  Pv = dict()
  Pv["1"] = ll*1.0/(ll + lc)
  Pv["0"] = lc*1.0/(ll + lc)
  

  Pl = {}
  Pc = {}
  for i in range (0, n):
    Pl[i] = 0
    Pc[i] = 0
  for i in libL:
    for j in range (0,n):
      if i[j] == "1":
        Pl[j] += 1
  for i in conL:
    for j in range (0,n):
      if i[j] == "1":
        Pc[j] += 1
  #print Pc
  for i in Pl:
    Pl[i] = Pl[i] * 1.0 / ll
  for i in Pc:
    Pc[i] = Pc[i] * 1.0 / lc
  return (Pv, Pl, Pc)


def testRes():
  (Pv, Pl, Pc) = Vnb()
  error = 0
  for i in test:
    t = i.replace(" ", "")
    lable = t[n]
    pl = 1
    pc = 1
    #print t
    for j in range(0,n):
      if int(t[j]) == 1:
        #print j
        pl *= Pl[j]
        pc *= Pc[j]
      else:
        pl *= (1.0-Pl[j])
        pc *= (1.0-Pc[j])
      
    pl*=Pv["1"]
    pc*=Pv["0"]
    print pl/(pl + pc)





testRes()






