from graphs import Graph, Edge, Vertex
from set5_task1 import createRandomFlowNetwork

from random import sample, choice, randint, shuffle, random
from itertools import combinations
from collections import deque

import drawGraph

# region <Helper functions>
# # # Helper functions # # #


def is_source(v: Vertex):
    return len(v.inEdges) == 0


def is_sink(v: Vertex):
    return len(v.outEdges) == 0


def adjacent_vertices(v: Vertex):
    return [e.oppositeVertex(v) for e in v.outEdges.values()]


def subgraph_from(g: Graph, vs: {Vertex}):
    ret = g.copy()
    for v in set(g.vertexIndex.values())-vs:
        ret.removeVertex(v.label)
    return ret


def findEdges(g: Graph, startVertex: Vertex, endVertex: Vertex) -> [Edge]:
    """
    Znajduje wszystkie krawędzie pomiędzy dwoma wierzchołkami, ale bez zamiany wyniku na listę etykiet i spowrotem???????
    Zwraca listę
    """
    if isinstance(startVertex, str):
        startVertex = g.getVertex(startVertex)
    if isinstance(endVertex, str):
        endVertex = g.getVertex(endVertex)
    if startVertex is None or endVertex is None:
        raise Exception("Vertex not found", startVertex, endVertex)
    edges = set(startVertex.outEdges.values()).intersection(set(endVertex.inEdges.values()))
    res = ([e for e in edges if e.startVertex is startVertex and e.endVertex is endVertex] if g.isDirected()
           else [e for e in edges if (
            e.startVertex is startVertex and e.endVertex is endVertex)
            or (e.startVertex is endVertex and e.endVertex is startVertex)
                 ]
           )
    return res


def mergeEdges(g: Graph, v: Vertex, u: Vertex, edges: [Edge] = None) -> Edge:
    """
    Łączy krawędzie pomiędzy dwoma wierzchołkami. Nowa krawędź będzie mieć wagę równą sumie wag usuniętych krawędzi.
    Zwraca nową krawędź.
    """
    if edges is None:
        edges = findEdges(g, v, u)
    weight = sum(edge.weight for edge in edges)
    for edge in edges:
        edge.removeMe()
    return g.addEdge(v, u, weight=weight)


def reverseEdge(e: Edge) -> Edge:
    """
    Zwraca odwróconą krawędź bez modyfikacji grafu.
    """
    res = Edge.bareEdge(e.endVertex, e.startVertex, f'r{e.label}', weight=e.weight)
    return res

# endregion

# region <Task-critical functions>
# # # Task-critical functions # # #


def flow_subgraph(s: Vertex, t: Vertex) -> Graph:
    """
    Znajduje podgraf digrafu do którego należą wierzchołki,
    taki którego każdy element leży na ścieżce z s do t.
    """
    if s.graph is not t.graph:
        return False

    subgraph = set()

    def DFS(v: Vertex):
        subgraph.add(v)
        if v is t:
            return
        for u in adjacent_vertices(v):
            if u not in subgraph:
                DFS(u)

    DFS(s)
    if t not in subgraph:
        raise Exception('Nie ma ścieżki pomiędzy źródłem a ujściem')
    return subgraph_from(s.graph, subgraph)


def ford_fulkerson(g: Graph, s: Vertex, t: Vertex) -> float:
    """
    Znajduje maksymalny przepływ sieci przepływowej g ze źródła s do ujścia t.
    Wykorzystuje algorytm przeszukiwania wszerz Edmondsa-Karpa.
    Przepustowość krawędzi sieci powinna być zakodowana jako ich waga.
    """
    print(f'Source: {s}\n Sink: {t}\n')
    # # CLEAN-UP
    # Find all paths between source and target
    subgraph = flow_subgraph(s, t)
    s = subgraph.getVertex(s.label)
    t = subgraph.getVertex(t.label)
    # Collapse multiple edges in subgraph
    for pair in combinations(subgraph.vertexIndex.values(), 2):
        edges = findEdges(subgraph, pair[0], pair[1])
        if len(edges) > 1:
            mergeEdges(subgraph, pair[0], pair[1], edges=edges)
    # # SOLVE PROBLEM
    flow = 0
    edges = list(subgraph.edgeIndex.values())
    flows = {edge.label: 0 for edge in [*edges, *[reverseEdge(e) for e in edges]]}
    pred = {}
    first_iteration = True
    while pred.get(t) is not None or first_iteration:
        q = deque([s])
        pred = {vertex: None for vertex in subgraph.vertexIndex.values()}
        first_iteration = False
        while len(q) > 0:
            cur = q.pop()
            for edge in cur.outEdges.values():
                if pred[edge.endVertex] is None and edge.endVertex is not s and edge.weight > flows[edge.label]:
                    pred[edge.endVertex] = edge
                    q.append(edge.endVertex)
        if pred[t] is not None:
            df = float("Inf")
            e = pred[t]
            while e is not None:
                df = min(df, e.weight - flows[e.label])
                e = pred[e.startVertex]
            e = pred[t]
            while e is not None:
                flows[e.label] = flows[e.label] + df
                flows[reverseEdge(e).label] = flows[reverseEdge(e).label] - df
                e = pred[e.startVertex]
            flow = flow + df
    print(flows)
    return flow


def edmonds_karp(g: Graph, s: Vertex, t: Vertex) -> float:
    return ford_fulkerson(g, s, t)

# endregion

# region <Test graphs>


def testGraph1() -> Graph:
    g = Graph(True)
    for i in range(1, 6):
        g.addVertex(f'{i}')
    g.addEdge('1', '3')
    g.addEdge('2', '1')
    g.addEdge('3', '2')
    g.addEdge('3', '4')
    g.addEdge('5', '1')
    g.addEdge('5', '4')
    return g


def testGraph2() -> Graph:
    g = Graph(True)
    for i in range(1, 4):
        g.addVertex(f'{i}')
    g.addEdge('1', '2', weight=2)
    g.addEdge('1', '2', weight=3)
    g.addEdge('1', '2', weight=1)
    g.addEdge('2', '3', weight=2)
    g.addEdge('3', '1', weight=1)
    return g


def testGraphWikipedia() -> Graph:
    g = Graph(True)
    g.addVertex('A')
    g.addVertex('B')
    g.addVertex('C')
    g.addVertex('D')
    g.addVertex('E')
    g.addVertex('F')
    g.addVertex('G')
    g.addEdge('A', 'B', weight=3)
    g.addEdge('A', 'D', weight=3)

    g.addEdge('B', 'C', weight=4)

    g.addEdge('C', 'A', weight=3)
    g.addEdge('C', 'D', weight=1)
    g.addEdge('C', 'E', weight=2)

    g.addEdge('D', 'E', weight=2)
    g.addEdge('D', 'F', weight=6)

    g.addEdge('E', 'B', weight=1)
    g.addEdge('E', 'G', weight=1)

    g.addEdge('F', 'G', weight=9)
    return g


def testGraphHackerEarth() -> Graph:
    g = Graph(True)
    g.addVertex('S')
    g.addVertex('T')
    g.addVertex('A')
    g.addVertex('B')
    g.addVertex('C')
    g.addVertex('D')
    g.addEdge('S', 'A', weight=10)
    g.addEdge('S', 'C', weight=8)

    g.addEdge('A', 'B', weight=5)
    g.addEdge('A', 'C', weight=2)

    g.addEdge('B', 'T', weight=7)

    g.addEdge('C', 'D', weight=10)

    g.addEdge('D', 'B', weight=8)
    g.addEdge('D', 'T', weight=10)

    return g


def testGraphG4G() -> Graph:
    g = Graph(True)
    g.addVertex('0')
    g.addVertex('1')
    g.addVertex('2')
    g.addVertex('3')
    g.addVertex('4')
    g.addVertex('5')

    g.addEdge('0', '1', weight=16)
    g.addEdge('0', '2', weight=13)

    g.addEdge('1', '2', weight=10)
    g.addEdge('1', '3', weight=12)

    g.addEdge('2', '1', weight=4)
    g.addEdge('2', '4', weight=14)

    g.addEdge('3', '5', weight=20)
    g.addEdge('3', '2', weight=9)

    g.addEdge('4', '3', weight=7)
    g.addEdge('4', '5', weight=4)

    return g

# endregion


def main():
    graphGenerators = [testGraphWikipedia, testGraphHackerEarth, testGraphG4G, lambda: createRandomFlowNetwork(2)]
    source_sinks = [('A', 'G'), ('S', 'T'), ('0', '5'), ('s', 't')]
    i = 3
    g = graphGenerators[i]()
    source, sink = source_sinks[i]
    drawGraph.drawDirectedGraphWithWeights(g, 5, 'flownetwork.png', True)
    print(f'Graf:\n{g}')
    print(f'Maksymalny przepływ jest równy: {ford_fulkerson(g, g.getVertex(source), g.getVertex(sink))}')


if __name__ == "__main__":
    main()

