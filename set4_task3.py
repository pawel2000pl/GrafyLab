import drawGraph
from graphs import Graph, Edge, Vertex
from random import uniform, random, choice
from math import inf

def generateStronglyConnectedDigraph(n: int, p: float):
    g = Graph(directed=True)
    # Add vertices
    for _ in range(n):
        g.addVertex()
    # Create basic cycle
    vertices = list(g.vertexIndex.values())
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


def detect_cycle(l) -> bool:
    hare = 0
    tortoise = 0
    for i in range(len(l)):
        hare += 2
        tortoise += 1
        if hare >= len(l) or tortoise >= len(l):
            return False
        if l[hare] is l[tortoise]:
            return True

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
    """
    for edge in edges:
        u, w = (edge.startVertex, edge.endVertex)
        if v[u][0] + edge.weight < v[w][0]:
            negative_loop = [w, u]
            for i in range(v_mod-1):
                u = negative_loop[0]
                for e in edges:
                    u, w = (edge.startVertex, edge.endVertex)
                    if v[u][0] + e.weight < v[w][0]:
                        negative_loop.insert(0, w)
            if detect_cycle(negative_loop):
                print(negative_loop)
                raise Exception('Graf zawiera pętlę o ujemnej wadze')
    """
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


if __name__ == "__main__":
    g = generateStronglyConnectedDigraph(10, 0.5)
    g = testGraph()
    drawGraph.drawDirectedGraphWithWeights(g, 5, 'test.png', True)
    print(g.Kosaraju())
    print(bellman_ford(g, choice(list(g.vertexIndex.values()))))
