import sys
from collections import Counter
import math
import operator

train = sys.argv[1]
fo = open(train, "r")
docs = fo.readlines()
docs = map(lambda s: s.strip(), docs)

test = sys.argv[2]
fo = open(test, "r")
test = fo.readlines()
test = map(lambda s: s.strip(), test)

N = int(sys.argv[3])

# train Vnb
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

  vocab = dict(Counter(Tl + Tc))
  

  counterL = 0
  counterC = 0
  for i in range (0, N):
    k = max(vocab.iteritems(), key=operator.itemgetter(1))[0]
    del vocab[k]
    if k in Pc:
      counterC += Pc[k]
      del Pc[k]
    if k in Pl:
      counterL += Pl[k]
      del Pl[k]
  lv = len(vocab)

  for i in vocab:
    if i in Pl:
      Pl[i] = ((Pl[i] + 1.0) / (lv + (nl - counterL)))
    else:
      Pl[i] = ((1.0) / (lv + (nl - counterL)))
    if i in Pc:
      Pc[i] = ((Pc[i] + 1.0) / (lv + (nc - counterC)))
    else:
      Pc[i] = ((1.0) / (lv + (nc - counterC)))

  return (Pl, Pc,Pv, lv, (nl), (nc),vocab)



def testRes():
  (Pl, Pc,Pv, lv, nl, nc,vocab) = Vnb()
  error = 0
  for i in test:
    if i[0] == "c":
      lable = "C"
    else:
      lable = "L"
    fo = open(i, "r")
    testData = fo.readlines()
    testData = map(lambda s: s.strip(), testData)
    testData = map(lambda s: s.lower(), testData)   
    pl = 0
    pc = 0
    for j in testData:
      if j in vocab:
        pc += math.log(Pc[j])  
   
        pl += math.log(Pl[j])

        
    pc = pc + math.log(Pv["C"])
    pl = pl + math.log(Pv["L"])


    if pl > pc:
      res = "L"
    else:
      res = "C"
    if res != lable:
      error += 1
    print (res)

  print "Accuracy: " + str("%.4f" % ((len(test) - error) * 1.0/len(test)))


testRes()





















