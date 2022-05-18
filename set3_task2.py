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

