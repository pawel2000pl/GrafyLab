from graphs import Graph
import drawGraph

g = Graph(False)

g.addVertex("a")
g.addVertex("b")
g.addVertex("c")
g.addVertex("d")
g.addVertex("e")
g.addVertex("f")
g.addVertex("g")

g.addEdge("a", "g", weight=5)
g.addEdge("a", "b", weight=5)
g.addEdge("b", "g", weight=5)
g.addEdge("c", "b", weight=3)
g.addEdge("b", "d", weight=3)
g.addEdge("c", "d", weight=1)
g.addEdge("d", "e", weight=5)
g.addEdge("e", "f", weight=2)
g.addEdge("f", "d", weight=4)
g.addEdge("d", "g", weight=3)
g.addEdge("f", "g", weight=5)

print(str(g))
vertexList = ["a", "b", "c", "d", "e", "f", "g"]
for v in vertexList:
    print("\n", v, ": ", g.DijkstraDistance(v))
    for v2 in vertexList:
        way = g.getWayTo(v2)
        print([str(edge) for edge in way], " length = ", sum(edge.weight for edge in g.getWayTo(v2)))


print("\nSpanning tree")
print([str(edge) for edge in g.minimalSpanningTree("c")])

print("\n\n\n\n\n")

g = Graph(False)
for i in range(1, 7):
    g.addVertex()

g.addEdge("v1", "v4", weight=4)
g.addEdge("v1", "v3", weight=1)
g.addEdge("v1", "v5", weight=4)
g.addEdge("v1", "v6", weight=9)
g.addEdge("v2", "v3", weight=9)
g.addEdge("v2", "v6", weight=6)
g.addEdge("v3", "v5", weight=7)
g.addEdge("v4", "v5", weight=9)
g.addEdge("v4", "v6", weight=4)
g.addEdge("v5", "v6", weight=7)

vertexList = list(g.vertexIndex.keys())
for v in vertexList:
    print("\n", v, ": ", g.DijkstraDistance(v))
    for v2 in vertexList:
        way = g.getWayTo(v2)
        print([str(edge) for edge in way], " length = ", sum(edge.weight for edge in g.getWayTo(v2)))


print("\nSpanning tree")
print([str(edge) for edge in g.minimalSpanningTree()])

print("\n\n\n\n\n")

g = Graph(False)

for i in range(1, 13):
    g.addVertex()
    
g.addEdge("v1", "v2", weight=3)
g.addEdge("v4", "v2", weight=2)
g.addEdge("v4", "v7", weight=3)
g.addEdge("v7", "v10", weight=5)
g.addEdge("v1", "v5", weight=9)
g.addEdge("v5", "v2", weight=4)
g.addEdge("v5", "v7", weight=1)
g.addEdge("v5", "v8", weight=2)
g.addEdge("v8", "v10", weight=5)
g.addEdge("v12", "v8", weight=9)
g.addEdge("v1", "v3", weight=2)
g.addEdge("v3", "v5", weight=6)
g.addEdge("v3", "v6", weight=9)
g.addEdge("v6", "v8", weight=1)
g.addEdge("v6", "v9", weight=2)
g.addEdge("v9", "v11", weight=2)
g.addEdge("v11", "v12", weight=3)
g.addEdge("v8", "v11", weight=6)
print("\n\n\n")
print(str(g))
vertexList = list(g.vertexIndex.keys())
for v in vertexList:
    print("\n", v, ": ", g.DijkstraDistance(v))
    for v2 in vertexList:
        way = g.getWayTo(v2)
        print([str(edge) for edge in way], " length = ", sum(edge.weight for edge in g.getWayTo(v2)))


print("\nSpanning tree")
print([str(edge) for edge in g.minimalSpanningTree()])

