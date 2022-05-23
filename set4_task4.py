from graphs import Graph, Vertex, Edge
from set4_task3 import generateStronglyConnectedDigraph
from drawGraph import *


def johnsonAlgorithm(graph: Graph):
    copyGraph = graph.copy()
    
    v0 = copyGraph.addVertex("v0")

    for vertex in copyGraph.vertexIndex.values():
        if not v0.equals(vertex):
            copyGraph.addEdge(v0, vertex, weight=0)
    
    bellDist = copyGraph.ShortestDistance(v0)

    for vertex in copyGraph.vertexIndex.values():
        for edge in vertex.getOutEdges().values():
            oppositeVertex = edge.endVertex
            weight = edge.weight
            edge.weight = weight + bellDist[vertex.label] - bellDist[oppositeVertex.label]

    v0.removeMe()

    distance = {}

    for vertex in copyGraph.vertexIndex.values():
        distance[vertex] = copyGraph.DijkstraDistance(vertex)


    for vertex in copyGraph.vertexIndex.values():
        for secondVertex in copyGraph.vertexIndex.values():
            distance[vertex][secondVertex.label] += bellDist[secondVertex.label] - bellDist[vertex.label]


    return distance

def printDistanceDictionary(distance, startString):
    if not startString == None:
        print(startString)
    for vertex in distance:
        for d in distance[vertex]:
            distance[vertex][d] = round(distance[vertex][d], 2)
        print(vertex.label, distance[vertex])

def testJohnsonAlgorithm():
    case = 1
    if case == 1:
        a = generateStronglyConnectedDigraph(7, 0.4)
    else:
        a = Graph.generateRandomGraph(6, 6, directed=True)
        a.edgeIndex['e1'].weight = -2
        
    a.removeDuplicatedEdges()

    drawDirectedGraphWithWeights(a, 20, "johnsonGraph.png")
    print("stworzony graf: ", a)
    try:
        distance = johnsonAlgorithm(a)
        print()
        print()
        printDistanceDictionary(distance, "shortest paths: ")
    except:
        print('Ujemny cykl')


if __name__ == "__main__":
    testJohnsonAlgorithm()