from graphs import Graph, graphCenterFromDistanceMatrix, graphMiniMaxCenterFromDistanceMatrix
import drawGraph
from set3_task1 import connectDanglingVertexes, addWeights

g = Graph(False)

for i in range(12):
    g.addVertex(str(i + 1))

g.addEdge("1", "2", weight=3)
g.addEdge("1", "3", weight=2)
g.addEdge("1", "5", weight=9)
g.addEdge("2", "4", weight=2)
g.addEdge("2", "5", weight=4)
g.addEdge("3", "5", weight=6)
g.addEdge("3", "6", weight=9)
g.addEdge("4", "7", weight=3)
g.addEdge("5", "7", weight=1)
g.addEdge("5", "8", weight=2)
g.addEdge("6", "8", weight=1)
g.addEdge("6", "9", weight=2)
g.addEdge("9", "11", weight=2)
g.addEdge("8", "11", weight=6)
g.addEdge("7", "10", weight=5)
g.addEdge("8", "10", weight=5)
g.addEdge("8", "12", weight=9)
g.addEdge("11", "12", weight=3)
g.addEdge("10", "12", weight=5)

print("Macierz odleglosci:\n")
distanceMatrix = g.distanceMatrix()
drawGraph.drawGraphWithWeights(g, 2, "graf1.png")
print(*distanceMatrix, sep="\n")

print("Macierz odleglosci:\n")
g2 = Graph.generateRandomGraphProbability(10, 0.2, directed=False)
connectDanglingVertexes(g2)
addWeights(g2)
distanceMatrix2 = g2.distanceMatrix()
drawGraph.drawGraphWithWeights(g2, 2, "graf2.png")
print(*distanceMatrix, sep="\n")


print("\nzad 4:\n")

center = graphCenterFromDistanceMatrix(distanceMatrix)
miniMaxCenter = graphMiniMaxCenterFromDistanceMatrix(distanceMatrix)
print("centrum:")
print("\tśrodek: ", *center.keys(), ", odległośc:", *center.values())
print("centrum minimax:")
print("\tśrodek: ", *miniMaxCenter.keys(), ", odległośc:", *miniMaxCenter.values())
print("")

center2 = graphCenterFromDistanceMatrix(distanceMatrix2)
miniMaxCenter2 = graphMiniMaxCenterFromDistanceMatrix(distanceMatrix2)
print("centrum:")
print("\tśrodek: ", *center2.keys(), ", odległośc:", *center2.values())
print("centrum minimax:")
print("\tśrodek: ", *miniMaxCenter2.keys(), ", odległośc:", *miniMaxCenter2.values())
