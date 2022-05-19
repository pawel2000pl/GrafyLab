# ------------------------------------------------------------------------------
# PROJ 3 TASK 1
# ------------------------------------------------------------------------------
import random

from set2_task4 import connectedComponents
from drawGraph import drawGraphWithWeights
from graphs import Graph


def addWeights(graph, minWeight=1, maxWeight=10):
        for label, edge in graph.edgeIndex.items():
            edge.weight = int(random.choice(range(minWeight, maxWeight)))


def connectDanglingVertexes(graph):
    components = connectedComponents(graph)
    if len(components) > 1:
        for a, b in zip(components[:-1], components[1:]):
            startVertex = a[random.randrange(0, len(a))]
            endVertex = b[random.randrange(0, len(b))]
            graph.addEdge(startVertex, endVertex)

if __name__ == "__main__":
    g2 = Graph.generateRandomGraphProbability(10, 0.2, directed=False)
    connectDanglingVertexes(g2)
    addWeights(g2)
    drawGraphWithWeights(g2, 4, "test.png")