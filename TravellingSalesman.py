from math import sqrt
from graphs import Graph
from math import inf, exp
import random

def SaveToImage(fileName, graph):
        
    from PIL import Image, ImageDraw

    minX = min(point.x for point in graph.vertexIndex.values())
    maxX = max(point.x for point in graph.vertexIndex.values())
    minY = min(point.y for point in graph.vertexIndex.values())
    maxY = max(point.y for point in graph.vertexIndex.values())
    
    Width = 1000
    Height = round(Width / (maxX-minX) * (maxY-minY))
    
    image = Image.new("RGB", (Width, Height), "white")
    draw = ImageDraw.Draw(image)

    def ConvertCoordsX(d):
        nonlocal minX
        nonlocal maxX
        nonlocal Width    
        return round((d-minX)/(maxX-minX)*Width)

    def ConvertCoordsY(d):    
        nonlocal maxY
        nonlocal minY
        nonlocal Height    
        return round(Height-1-(d-minY)/(maxY-minY)*Height)

    for edge in graph.edgeIndex.values():
        draw.line([(ConvertCoordsX(edge.startVertex.x), ConvertCoordsY(edge.startVertex.y)), (ConvertCoordsX(edge.endVertex.x), ConvertCoordsY(edge.endVertex.y))], width=1, fill=(0), joint="curve")
            
    draw.text((1, 1), str(sum(edge.weight for edge in graph.edgeIndex.values())), fill="black")
    image.save(fileName)

def hypot(x, y):
    return sqrt(x*x+y*y)

def tryPutEdge(graph, edge, maxLen):
    startLabel = edge.startVertex.label
    endLabel = edge.endVertex.label
    if (graph.ShortestDistance(startLabel)[endLabel] == inf or len(graph.getWayTo(endLabel)) >= maxLen) and graph.getVertex(startLabel).degree < 2 and graph.getVertex(endLabel).degree < 2:
        graph.addEdge(startLabel, endLabel, weight=edge.weight)
        return True
    return False

def trySwitchEdges(graph, edgeA, edgeB, currentDistance, temp = 1.0, useTemp = True):
    if len(edgeA.verticlesSet().union(edgeB.verticlesSet())) < 4:
        return currentDistance
    
    dataA = (edgeA.startVertex, edgeA.endVertex, edgeA.weight, edgeA.label)
    dataB = (edgeB.startVertex, edgeB.endVertex, edgeB.weight, edgeB.label)
    
    edgeA.removeMe()
    edgeB.removeMe()    
    graph.ShortestDistance(dataA[0])
    if dataB[0].distance == inf:        
        newDataA = (edgeA.startVertex, edgeB.startVertex, hypot(edgeA.startVertex.x - edgeB.startVertex.x, edgeA.startVertex.y-edgeB.startVertex.y), edgeA.label)
        newDataB = (edgeB.endVertex, edgeA.endVertex, hypot(edgeB.endVertex.x - edgeA.endVertex.x, edgeB.endVertex.y-edgeA.endVertex.y), edgeB.label)
    else:
        newDataA = (edgeA.startVertex, edgeB.endVertex, hypot(edgeA.startVertex.x - edgeB.endVertex.x, edgeA.startVertex.y-edgeB.endVertex.y), edgeA.label)
        newDataB = (edgeB.startVertex, edgeA.endVertex, hypot(edgeB.startVertex.x - edgeA.endVertex.x, edgeB.startVertex.y-edgeA.endVertex.y), edgeB.label)
        
    if dataA[2]+dataB[2] >= newDataA[2]+newDataB[2] or (useTemp and random.random() < exp(-((newDataA[2]+newDataB[2]) - (dataA[2]+dataB[2]))/temp)):
        graph.addEdge(newDataA[0], newDataA[1], label=newDataA[3], weight=newDataA[2])
        graph.addEdge(newDataB[0], newDataB[1], label=newDataB[3], weight=newDataB[2])
        return currentDistance - (dataA[2]+dataB[2]) + (newDataA[2]+newDataB[2])
    
    graph.addEdge(dataA[0], dataA[1], label=dataA[3], weight=dataA[2])
    graph.addEdge(dataB[0], dataB[1], label=dataB[3], weight=dataB[2])
    return currentDistance
    
    
n = int(input())
g = Graph(False)

points = []
for i in range(n):
    line = input()
    elements = line.split(" ")
    vertex = g.addVertex()
    vertex.x = float(elements[0])
    vertex.y = float(elements[1])
    points.append(vertex)
    
g2 = g.copy()
for k, v in g.vertexIndex.items():
    vertex = g2.getVertex(k)
    vertex.x = v.x
    vertex.y = v.y
    
edges = []
for i, pointA in enumerate(points):
    for j, pointB in enumerate(points):
        if i <= j:
            break
        edge = g.addEdge(pointA, pointB, weight = hypot(pointA.x - pointB.x, pointA.y-pointB.y))
        edges.append(edge)
        
for point in points:
    point.sortedEdges = list(point.allEdgesSet())
    point.sortedEdges.sort(key = lambda edge: edge.weight)
                
weightSortedEdges = edges.copy()
weightSortedEdges.sort(key = lambda edge: edge.weight)
maxWeight = weightSortedEdges[-1].weight + 1
edges.sort(key = lambda edge: min(edge.startVertex.sortedEdges.index(edge), edge.endVertex.sortedEdges.index(edge))+edge.weight/maxWeight)

minDifference = min(weightSortedEdges[i+1].weight-weightSortedEdges[i].weight for i in range(len(weightSortedEdges)-1) if weightSortedEdges[i+1].weight != weightSortedEdges[i].weight)
minDistance = inf


for edge in list(g2.edgeIndex.values()):
    edge.removeMe()
    
distance = 0.0
edgeCount = 0

for edge in edges:
    if tryPutEdge(g2, edge, edgeCount):
        distance += edge.weight
        edgeCount += 1
        if edgeCount == n:
            break
                
labelList = list(g2.edgeIndex.keys())
changes = True

while changes:
    changes = False
    for e1 in labelList:
        for e2 in labelList:
            prevDistance = distance
            distance = trySwitchEdges(g2, g2.edgeIndex[e1], g2.edgeIndex[e2], distance, useTemp=False)
            if distance < prevDistance:
                changes = True
                print(distance)
                if distance < minDistance:
                    minDistance = distance
                
print(minDistance)
SaveToImage("TravellingResults.png", g2)                

borderWeight = edges[edgeCount-1].weight + edges[edgeCount-2].weight
usableEdges = [edge for edge in edges if edge.weight < borderWeight]

from sys import platform
from os import system as shell
makeVideo = platform == "linux" or platform == "linux2"
if makeVideo:
    shell("rm -f /dev/shm/TravellingResults*.png")

def calc(i):
    random.seed(round(random.random()*(2**31)) + i)
    temp = 15.0
    it = 0
    same = 0
    bestGraph = g2.copy()
    distance = sum(edge.weight for  edge in g2.edgeIndex.values())
    minDistance = distance
    while temp > 2.71/n and same <= 6:
        it += 1
        prevDistance = distance
        for it2 in range(n*n):
            valueList = list(g2.edgeIndex.values())
            distance = trySwitchEdges(g2, random.choice(valueList), random.choice(valueList), distance, temp=temp)
            
        print(it, distance, temp)
        if distance >= prevDistance:        
            temp *= 0.96
            if distance == prevDistance:
                same += 1
            else:
                same = 0
        
        if makeVideo:
            SaveToImage("/dev/shm/TravellingResults"+str(i)+"-"+str(it)+".png", g2)
        
        if distance < minDistance:
            minDistance = distance;
            bestGraph = g2.copy()
            SaveToImage("TravellingResults.png", g2)
        
    if makeVideo:
        shell("ffmpeg -r 5 -i \"/dev/shm/TravellingResults"+str(i)+"-%d.png\" -r 5 video-"+str(i)+".mp4 -y")
        
    return (bestGraph.createAdjacencyMatrix(), minDistance, i)
            
from multiprocessing import Pool
from os import cpu_count

count = cpu_count()
with Pool(count) as p:
    results = p.map(calc, [i for i in range(count)])
    
results.sort(key=lambda x: x[1])
print(results[0][1], " from thread: ", results[0][2])
graph = Graph(False)
graph.loadAdjacencyMatrix(results[0][0])

for k, v in g.vertexIndex.items():
    vertex = graph.getVertex(k)
    vertex.x = v.x
    vertex.y = v.y
    
SaveToImage("TravellingResults.png", graph)

if makeVideo:
    shell("rm -f /dev/shm/TravellingResults*.png")
