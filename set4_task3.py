import drawGraph
from graphs import Graph, Edge, Vertex
from random import uniform, random, choice, shuffle
from math import inf


def modifiedRepr(self):
    return self.label


Vertex.__repr__ = modifiedRepr


def generateStronglyConnectedDigraph(n: int, p: float):
    g = Graph(directed=True)
    # Add vertices
    for _ in range(n):
        g.addVertex()
    # Create basic cycle
    vertices = list(g.vertexIndex.values())
    shuffle(vertices)
    g.addEdge(vertices[-1], vertices[0])
    for a, b in zip(vertices[:-1], vertices[1:]):
        g.addEdge(a, b, None, round(uniform(-5, 10), 2))
    # Add random edges
    vertexList = g.vertexIndex.values()
    vertexLabelList = [vertex.label for vertex in vertexList]

    for _ in range(n):
        currentVertex = vertexLabelList.pop(0)
        for label in vertexLabelList:
            if random() < p:
                g.addEdge(currentVertex, label, None, round(uniform(-5, 10), 2))

    return g


def bellman_ford(g: Graph, source: Vertex):
    print(f'Source is {source}')
    v = list(g.vertexIndex.values())
    v = {vi: [inf, None] for vi in v}  # (Vertex, Distance, Predecessor)
    edges = list(g.edgeIndex.values())
    v_mod = len(v)

    v.update([(source, [0, source])])

    # Relaxation
    for i in range(v_mod-1):
        for edge in edges:
            u, w = (edge.startVertex, edge.endVertex)
            if v[u][0] + edge.weight < v[w][0]:
                v[w][0] = v[u][0] + edge.weight
                v[w][1] = u

    print(v)

    # Check for negative weight cycles
    for edge in edges:
        u, w = (edge.startVertex, edge.endVertex)
        if v[u][0] + edge.weight < v[w][0]:
            raise Exception('Graf zawiera pętlę o ujemnej wadze')

    return v


def testGraph():
    g = Graph()
    for _ in range(5):
        g.addVertex()
    g.addEdge('v1', 'v2', None, -1)
    g.addEdge('v1', 'v3', None, 4)
    g.addEdge('v2', 'v3', None, 3)
    g.addEdge('v2', 'v4', None, 2)
    g.addEdge('v2', 'v5', None, 2)
    g.addEdge('v4', 'v3', None, 5)
    g.addEdge('v4', 'v2', None, 1)
    g.addEdge('v5', 'v4', None, -3)
    return g


def testGraph2():
    g = Graph(True)
    g.addVertex('1')
    g.addVertex('2')
    g.addVertex('3')
    g.addVertex('4')
    g.addVertex('5')
    g.addVertex('6')
    g.addEdge('1', '3', None, 1)
    g.addEdge('1', '5', None, 4)
    g.addEdge('1', '4', None, 4)
    g.addEdge('1', '6', None, 9)
    g.addEdge('2', '3', None, 9)
    g.addEdge('3', '5', None, 7)
    g.addEdge('4', '5', None, 9)
    g.addEdge('4', '6', None, 4)
    g.addEdge('5', '6', None, 7)
    return g


if __name__ == "__main__":
    g = generateStronglyConnectedDigraph(10, 0.1)
    drawGraph.drawDirectedGraphWithWeights(g, 5, 'bellmankhyuFord.png', True)
    print(g.Kosaraju())
    print(bellman_ford(g, choice(list(g.vertexIndex.values()))))
    # Rozwiązanie dla grafu na obrazie bellmanFord.png
    # {
    # v1: [2.5399999999999996, v9],
    # v2: [17.119999999999997, v8],
    # v3: [4.93, v10],
    # v4: [-2.4500000000000006, v1],
    # v5: [26.769999999999996, v2],
    # v6: [0, v6],
    # v7: [2.28, v6],
    # v8: [10.7, v7],
    # v9: [-2.1600000000000006, v7],
    # v10: [3.9299999999999993, v4]
    # }
