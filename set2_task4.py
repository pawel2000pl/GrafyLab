import collections
from random import randint, randrange, choice

from graphs import Graph, Edge, Vertex
import drawGraph

# Utility functions


def getNeighbors(here: Vertex):
    return {edge.oppositeVertex(here) for edge in here.allEdgesSet()}


def addVertices(graph: Graph, vertices: collections.abc.Iterable):
    for vertex in vertices:
        graph.addVertex(vertex.label if isinstance(vertex, Vertex) else vertex)


def addEdges(graph: Graph, edges: collections.abc.Iterable):
    for startVertex, endVertex, label, weight in edges:
        graph.addEdge(startVertex, endVertex, label, weight)

# Task-relevant functions


def isEulerian(graph: Graph):
    """
    Sprawdza czy podany graf jest eulerowski.
    """
    return all(vertex.degree % 2 == 0 for vertex in graph.vertexIndex.values())


def getOddDegreeVertices(graph: Graph):
    return [vertex for vertex in graph.vertexIndex.values() if vertex.degree % 2 != 0]


def connectedComponents(graph: Graph):
    """
    Zlicza spójne składowe grafu. Metoda wyszukiwania depth-first.
    """
    components: [[Vertex]] = []
    visited: {Vertex: bool} = {vertex: False for vertex in graph.vertexIndex.values()}

    def search(comp, v):
        visited.update({v: True})
        comp.append(v)
        for n in getNeighbors(v):
            if not visited[n]:
                comp = search(comp, n)
        return comp

    for v, isVisited in visited.items():
        if not isVisited:
            components.append(search([], v))

    return components


def countConnectedComponents(graph: Graph):
    return len(connectedComponents(graph))


def isBridge(edge: Edge):
    """
    Sprawdza czy krawędź jest mostem, tj. czy jej usunięcie powoduje utratę spójności
    """
    graph = edge.getGraph().copy()
    graph.removeEdge(edge.label)
    newCC = countConnectedComponents(graph)
    return newCC > 1


def generateRandomEulerGraph(n: int = 10, p: float = 0.15, attempts: int = 0):
    """
    Generuje graf eulerowski. Graf jest eulerowski jeśli:
    1. Jest to graf spójny
    2. Wszystkie wierzchołki są parzystego stopnia
    """
    # Start with random graph
    graph = Graph.generateRandomGraphProbability(n, p)
    drawGraph.drawMultiGraph(graph, 5, 'eulerGraph.png')
    # Ensure graph is connected
    components = connectedComponents(graph)
    if len(components) > 1:
        for a, b in zip(components[:-1], components[1:]):
            startVertex = a[randrange(0, len(a))]
            endVertex = b[randrange(0, len(b))]
            graph.addEdge(startVertex, endVertex)
    # Ensure all degrees are even
    outliers = getOddDegreeVertices(graph)
    if len(outliers) % 2 != 0:
        # Keep regenerating graph until the amount of outliers is correct
        return generateRandomEulerGraph(attempts=attempts + 1)
    else:
        # Connect outliers to each other pairwise
        print(attempts)
        for i in range(len(outliers)//2):
            graph.addEdge(outliers[i].label, outliers[len(outliers)-1-i].label)

    drawGraph.drawMultiGraph(graph, 5, 'eulerGraph2.png')
    return graph


def findEulerCycle(graph: Graph):
    """
    Znajduje cykl Eulera grafu eulerowskiego, jeśli takowy istnieje.
    Jeśli graf nie jest eulerowski, zwraca None.
    Korzysta z algorytmu Fleury'ego.
    """
    if not isEulerian(graph):
        return None
    drawGraph.drawMultiGraph(graph, 5, 'beforeFindingCycle.png')
    graph = graph.copy()
    start = graph.vertexIndex.get(choice(list(graph.vertexIndex)))
    for _, vertex in graph.vertexIndex.items():
        print(vertex)

    def traverse(vertex: Vertex, cycle=None):
        if cycle is None:
            cycle = []
        print(vertex)
        if len(graph.edgeIndex) == 0:
            return cycle
        for _, edge in vertex.inEdges.items():
            if not isBridge(edge):
                cycle.append(edge)
                graph.removeEdge(edge)
                if len(vertex.inEdges) == 0:
                    graph.removeVertex(vertex)
                return traverse(edge.oppositeVertex(vertex), cycle)
        # If we reach this point, all remaining edges are bridges
        # Pick one at random at keep going
        edge = vertex.inEdges.get(choice(list(vertex.inEdges)))
        cycle.append(edge)
        graph.removeEdge(edge)
        if len(vertex.inEdges) == 0:
            graph.removeVertex(vertex)
        return traverse(edge.oppositeVertex(vertex), cycle)

    print("Cycle:")
    result = traverse(start)
    return result

# Tests (not really iks de)


def testCountConnectedComponents():
    graph = Graph()
    addVertices(graph, ['v1', 'v2', 'v3', 'v4', 'v5', 'v6'])
    addEdges(graph, [('v1', 'v2', 'e1', 1.), ('v1', 'v2', 'e2', 1.), ('v2', 'v6', 'e3', 1.),
                     ('v3', 'v4', 'e4', 1.), ('v4', 'v5', 'e5', 1.), ('v4', 'v5', 'e6', 1.)])
    drawGraph.drawMultiGraph(graph,5,'testCountConnectedComponents.png')
    assert countConnectedComponents(graph) == 2


def testGenerateRandomEulerGraph():
    generateRandomEulerGraph()


def testMultiGraphDrawing():
    graph = Graph.generateRandomGraph(10,15)
    drawGraph.drawMultiGraph(graph,5,'testMultiGraph.png')


if __name__ == '__main__':
    findEulerCycle(generateRandomEulerGraph(8))
