from graphs import Graph
from numpy import matrix
from random import random, sample

g = Graph(True)

l = [("A", ["E" , "F" , "I"]),
     ("B", ["A" , "C" , "F"]),
     ("C", ["B" , "D" , "E", "L"]),
     ("D", ["C" , "E" , "H", "I", "K"]),
     ("E", ["C" , "G" , "H", "I"]),
     ("F", ["B" , "G"]),
     ("G", ["E" , "F" , "H"]),
     ("H", ["D" , "G" , "I", "L"]),
     ("I", ["D" , "E" , "H", "J"]),
     ("J", ["I"]),
     ("K", ["D" , "I"]),
     ("L", ["A" , "H"])]

g.loadAdjacencyList(l)

d = 0.15

print("Random walk\n")

jumpCount = 1000000

vertexList = list(g.vertexIndex.values())
for vertex in vertexList:
    vertex.visitCount = 0
    vertex.outList = [edge.oppositeVertex(vertex) for edge in vertex.outEdges.values()]
   
currentVertex = sample(vertexList, 1)[0]
for i in range(jumpCount):
    currentVertex.visitCount += 1
    if random() <= d:
        currentVertex = sample(vertexList, 1)[0]
    else:
        currentVertex = sample(currentVertex.outList, 1)[0]
        
resultList = []
for vertex in vertexList:
    resultList.append((vertex.visitCount/jumpCount, vertex.label))
resultList.sort(reverse=True, key=lambda x: x[0])
for i, l in resultList:
    print(l, i)
    
print("\n\nMatrix method\n")   
adMat = g.createAdjacencyMatrix()
m = matrix(adMat[1])
n = len(g.vertexIndex)
for i in range(n):
    m[i, :] *= (1-d) / m[i, :].sum()
m += d/n

v = matrix([1/n] * n)

mp = m**1024
r = v*mp

resultList = []
for i, cell in enumerate(r.transpose()):
    d = cell[0,0]
    resultList.append((d, adMat[0][i]))
    
resultList.sort(reverse=True, key=lambda x: x[0])
for i, l in resultList:
    print(l, i)




