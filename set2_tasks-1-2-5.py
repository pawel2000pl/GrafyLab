import random
from graphes import Vertex
from graphes import Edge
from graphes import Graph
from drawGraph import drawVertexes

def canGraphBeCreatedFrom(sequence):
    """
    Sprawdza czy mozna stworzyc graf z podanej listy stopni wierzcholkow
    na podstawie algorytmu Havel'a-Hakimi'ego
    """
    if sum(sequence) % 2 == 1:
        return False
    
    while True:
        sequence = sorted(sequence, reverse = True)

        if sequence[0] == 0 and sequence[len(sequence) - 1] == 0:
            return True
        
        v = sequence[0]
        sequence = sequence[1:]
        
        if v>len(sequence):
            return False

        for i in range(v):
            sequence[i] -= 1

            if sequence[i] < 0:
                return False


def createGraphFromSequence(sequence):
    """
    Tworzy graf z podanej listy stopni wierzcholkow
    jesli to niemozliwe zwraca None
    """
    if not canGraphBeCreatedFrom(sequence):
        return None

    graph = Graph(False)

    vertexesAndSequenceCombined = []
    GET_VERTEX = 0
    GET_SEQUENCE = 1
    for i in range(len(sequence)):
        vertexesAndSequenceCombined.append([graph.addVertex(), sequence[i]])

    while True:
        vertexesAndSequenceCombined = sorted(vertexesAndSequenceCombined, reverse = True, key = lambda a: a[GET_SEQUENCE])

        if vertexesAndSequenceCombined[0][GET_SEQUENCE] == 0 and vertexesAndSequenceCombined[len(vertexesAndSequenceCombined) - 1][GET_SEQUENCE] == 0:
            return graph

        maximum = vertexesAndSequenceCombined[0][GET_SEQUENCE]

        for endVertex in range(1, 1 + maximum):
            graph.addEdge(vertexesAndSequenceCombined[0][GET_VERTEX], vertexesAndSequenceCombined[endVertex][GET_VERTEX])
            vertexesAndSequenceCombined[endVertex][GET_SEQUENCE] -= 1

        vertexesAndSequenceCombined = vertexesAndSequenceCombined[1:]

    
def canEdgesBeSwapped(graph : Graph, edge1 : Edge, edge2 : Edge):
    """
    Sprawdza czy mozna zamienic pare krawedzi (ab, cd) na pare (ad, bc) bez zmieniania stopni wierzcholkow grafu
    """
    if edge1.equals(edge2):
        return False
    
    aVertex = edge1.startVertex
    bVertex = edge1.endVertex

    cVertex = edge2.startVertex
    dVertex = edge2.endVertex

    if  aVertex.equals(dVertex) or bVertex.equals(cVertex)\
        or  graph.findEdges(aVertex, dVertex) != None    or  graph.findEdges(dVertex, aVertex) != None\
        or  graph.findEdges(bVertex, cVertex) != None    or  graph.findEdges(cVertex, bVertex) != None:
        return False
    
    return True

def randomizeNotDirectedGraphWithoutChangingDegrees(graph : Graph, count: int = 10):
    """
    Gdy to mozliwe, zamienia losowe krawedzie w grafie bez zmieniania stopni wierzcholkow i zwraca nowy graf
    """
    newGraph = graph.copy()
    loopCount = 0
    MAX_LOOP = 1000
    for i in range(count):
        if loopCount > MAX_LOOP:
            return newGraph
    
        while True:
            if loopCount > MAX_LOOP:
                return newGraph
            loopCount += 1

            edgeLabel1, edge1 = random.choice(list(newGraph.edgeIndex.items()))
            edgeLabel2, edge2 = random.choice(list(newGraph.edgeIndex.items()))

            if canEdgesBeSwapped(graph, edge1, edge2):
                break

        aVertex = edge1.startVertex
        bVertex = edge1.endVertex

        cVertex = edge2.startVertex
        dVertex = edge2.endVertex 
        
        edge1.removeMe()
        edge2.removeMe()

        newGraph.addEdge(aVertex, dVertex, edgeLabel1)
        newGraph.addEdge(bVertex, cVertex, edgeLabel2)


    return newGraph


def createK_RegularGraph(k : int, size : int = -1):
    if size == -1:
        size = random.randint(3,8) * 2
    sequence = [k for i in range(size)]
    if not canGraphBeCreatedFrom(sequence):
        return None

    graph = createGraphFromSequence(sequence)
    return randomizeNotDirectedGraphWithoutChangingDegrees(graph)



#######
#
# Tests
#
#######

def testSequence():
    print('\nStarting testing creating from sequence\n')

    sequence = [7,7,5,4,4,4,3,3,2,1]
    assert canGraphBeCreatedFrom(sequence) == True
    graph = createGraphFromSequence(sequence)
    assert graph != None
    print('First graph:\n',graph,'\n')

    sum = 0
    for i in range(100):
        secondGraph = randomizeNotDirectedGraphWithoutChangingDegrees(graph)
        thirdGraph = randomizeNotDirectedGraphWithoutChangingDegrees(secondGraph)
        sum += 0 if graph.equals(secondGraph) else 1
        sum += 0 if secondGraph.equals(thirdGraph) else 1
    assert sum >= 198

    print('Second graph:\n',secondGraph,'\n')

    sequence = [8,4,6,5,2,1,2,3,4,4,2,1]

    assert canGraphBeCreatedFrom(sequence) == True
    graph = createGraphFromSequence(sequence)
    assert graph != None

    sequence = [10, 2, 3, 6, 3, 7, 9]
    assert canGraphBeCreatedFrom(sequence) == False
    graph = createGraphFromSequence(sequence)
    assert graph == None

    print('\nFinished\n')


def testK_Regular():
    print('\nStarting testing k regular graphs\n')
    graph = createK_RegularGraph(3, 6)
    secondGraph = createK_RegularGraph(3, 6)
    print('First graph:\n',graph,'\n')
    print('Second graph:\n',secondGraph,'\n')
    print('\nFinished\n')

if __name__ == "__main__":
    testSequence()
    testK_Regular()