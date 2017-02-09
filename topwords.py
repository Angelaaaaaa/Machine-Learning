import sys
from collections import Counter
import math
import operator

train = sys.argv[1]
fo = open(train, "r")
docs = fo.readlines()
docs = map(lambda s: s.strip(), docs)

def Vnb():
  libL = []
  conL = []
  # split C and L txt file
  for txt in docs:
    if txt[0] == "l":
      libL.append(txt)
    else:
      conL.append(txt)
  ll = len(libL)
  lc = len(conL)
  Pv = dict()

  # P(v)
  Pv["L"] = ll * 1.0/(lc + ll)
  Pv["C"] = lc * 1.0/(lc + ll)

  #creat text containing all menber of docj
  Tl = []
  Tc = []
  for i in libL:
    fo = open(i, "r")
    trainData = fo.readlines()
    trainData = map(lambda s: s.strip(), trainData)
    trainData = map(lambda s: s.lower(), trainData)
    Tl += (trainData)

  for j in conL:
    fo = open(j, "r")
    trainData = fo.readlines()
    trainData = map(lambda s: s.strip(), trainData)
    trainData = map(lambda s: s.lower(), trainData)
    Tc += (trainData)
  # count of uniqe words in 
  nl = len((Tl))
  nc = len((Tc))
  
  
  Pl = dict(Counter(Tl))
  Pc = dict(Counter(Tc))

  vocab = set(Tc + Tl)
  lv = len(vocab)

  for i in Pl:
    Pl[i] = ((Pl[i] + 1.0) / (lv + nl))
    
  for i in Pc:
    Pc[i] = ((Pc[i] + 1.0) / (lv + nc))
  MaxPc = []
  Mc = []
  MaxPl = []
  Ml = []
  for i in range (0, 20):
  	kl = max(Pl.iteritems(), key=operator.itemgetter(1))[0]
  	kc = max(Pc.iteritems(), key=operator.itemgetter(1))[0]
  	MaxPl.append(kl)
  	MaxPc.append(kc)
  	Ml.append(Pl[kl])
  	Mc.append(Pc[kc])

  	del Pl[kl]
  	del Pc[kc]
  for k in range(0,20):
  	print MaxPl[k], str("%.4f" % Ml[k])
  print 
  for k in range(0,20):
  	print MaxPc[k], str("%.4f" % Mc[k])


Vnb()





















